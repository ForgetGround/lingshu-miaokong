from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class EMGHandGestureDataset(Dataset):
    def __init__(
        self,
        features: np.ndarray,
        labels: np.ndarray,
        mean: Optional[np.ndarray] = None,
        std: Optional[np.ndarray] = None,
    ) -> None:
        if mean is not None and std is not None:
            features = (features - mean) / std

        self.features = torch.as_tensor(features, dtype=torch.float32).unsqueeze(1)
        self.labels = torch.as_tensor(labels, dtype=torch.long)

    def __len__(self) -> int:
        return self.labels.numel()

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.features[index], self.labels[index]


def _feature_columns(columns: Sequence[str]) -> List[str]:
    signal_columns = [col for col in columns if col.startswith("signal_")]
    return sorted(signal_columns, key=lambda name: int(name.split("_", 1)[1]))


def _stratified_split_indices(
    labels: np.ndarray,
    valid_ratio: float,
    test_ratio: float,
    seed: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if valid_ratio < 0 or test_ratio < 0 or valid_ratio + test_ratio >= 1:
        raise ValueError("valid_ratio and test_ratio must be non-negative and sum to less than 1.")

    rng = np.random.default_rng(seed)
    train_parts: List[np.ndarray] = []
    valid_parts: List[np.ndarray] = []
    test_parts: List[np.ndarray] = []

    for label in np.unique(labels):
        label_indices = np.flatnonzero(labels == label)
        rng.shuffle(label_indices)

        n_total = len(label_indices)
        n_test = int(round(n_total * test_ratio))
        n_valid = int(round(n_total * valid_ratio))

        test_parts.append(label_indices[:n_test])
        valid_parts.append(label_indices[n_test : n_test + n_valid])
        train_parts.append(label_indices[n_test + n_valid :])

    train_indices = np.concatenate(train_parts)
    valid_indices = np.concatenate(valid_parts)
    test_indices = np.concatenate(test_parts)

    rng.shuffle(train_indices)
    rng.shuffle(valid_indices)
    rng.shuffle(test_indices)

    return train_indices, valid_indices, test_indices


def create_datasets(
    csv_path: str | Path,
    valid_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
    label_col: str = "label",
    action_col: str = "action",
    standardize: bool = True,
) -> Tuple[EMGHandGestureDataset, EMGHandGestureDataset, EMGHandGestureDataset, Dict[int, str]]:
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path)

    feature_cols = _feature_columns(df.columns)
    if not feature_cols:
        raise ValueError(f"No signal_* feature columns found in {csv_path}.")
    if label_col not in df.columns:
        raise ValueError(f"No label column {label_col!r} found in {csv_path}.")

    features = df[feature_cols].to_numpy(dtype=np.float32)
    raw_labels = df[label_col].to_numpy(dtype=np.int64)

    original_labels = sorted(int(label) for label in np.unique(raw_labels))
    label_to_index = {label: index for index, label in enumerate(original_labels)}
    labels = np.asarray([label_to_index[int(label)] for label in raw_labels], dtype=np.int64)

    train_idx, valid_idx, test_idx = _stratified_split_indices(
        labels=labels,
        valid_ratio=valid_ratio,
        test_ratio=test_ratio,
        seed=seed,
    )

    mean = std = None
    if standardize:
        mean = features[train_idx].mean(axis=0, keepdims=True)
        std = features[train_idx].std(axis=0, keepdims=True)
        std = np.where(std < 1e-6, 1.0, std)

    label_to_action: Dict[int, str] = {}
    if action_col in df.columns:
        raw_label_to_action = {
            int(label): str(action)
            for label, action in df[[label_col, action_col]].drop_duplicates().itertuples(index=False)
        }
        label_to_action = {
            label_to_index[raw_label]: raw_label_to_action.get(raw_label, str(raw_label))
            for raw_label in original_labels
        }
    else:
        label_to_action = {index: str(raw_label) for raw_label, index in label_to_index.items()}

    train_dataset = EMGHandGestureDataset(features[train_idx], labels[train_idx], mean, std)
    valid_dataset = EMGHandGestureDataset(features[valid_idx], labels[valid_idx], mean, std)
    test_dataset = EMGHandGestureDataset(features[test_idx], labels[test_idx], mean, std)

    return train_dataset, valid_dataset, test_dataset, label_to_action
