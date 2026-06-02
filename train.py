import argparse
import random
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from dataset import create_datasets
from model import create_model


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(description="Train a ResNet18 classifier for EMG hand gestures.")
    parser.add_argument("--csv-path", type=Path, default=base_dir / "emg_hand_gestures.csv")
    parser.add_argument("--save-path", type=Path, default=base_dir / "best_model_dict.pth")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--valid-ratio", type=float, default=0.15)
    parser.add_argument("--test-ratio", type=float, default=0.15)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def run_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    optimizer: torch.optim.Optimizer | None = None,
) -> Tuple[float, float]:
    is_train = optimizer is not None
    model.train(is_train)

    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    context = torch.enable_grad() if is_train else torch.no_grad()
    with context:
        for features, labels in loader:
            features = features.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            if is_train:
                optimizer.zero_grad(set_to_none=True)

            logits = model(features)
            loss = criterion(logits, labels)

            if is_train:
                loss.backward()
                optimizer.step()

            batch_size = labels.size(0)
            total_loss += loss.item() * batch_size
            total_correct += (logits.argmax(dim=1) == labels).sum().item()
            total_samples += batch_size

    return total_loss / total_samples, total_correct / total_samples


def build_loaders(args: argparse.Namespace) -> Tuple[DataLoader, DataLoader, DataLoader, Dict[int, str]]:
    train_dataset, valid_dataset, test_dataset, label_to_action = create_datasets(
        csv_path=args.csv_path,
        valid_ratio=args.valid_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed,
    )

    pin_memory = str(args.device).startswith("cuda")
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=pin_memory,
    )
    valid_loader = DataLoader(
        valid_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=pin_memory,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=pin_memory,
    )
    return train_loader, valid_loader, test_loader, label_to_action


def serializable_args(args: argparse.Namespace) -> Dict[str, object]:
    values = vars(args).copy()
    for key, value in values.items():
        if isinstance(value, Path):
            values[key] = str(value)
    return values


def main() -> None:
    args = parse_args()
    set_seed(args.seed)

    device = torch.device(args.device)
    train_loader, valid_loader, test_loader, label_to_action = build_loaders(args)
    num_classes = max(label_to_action.keys()) + 1

    model = create_model(num_classes=num_classes, dropout=args.dropout).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    best_acc = -1.0
    best_loss = float("inf")
    args.save_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"device: {device}")
    print(
        f"samples: train={len(train_loader.dataset)}, "
        f"valid={len(valid_loader.dataset)}, test={len(test_loader.dataset)}"
    )
    print(f"classes: {num_classes} {label_to_action}")

    for epoch in range(1, args.epochs + 1):
        train_loss, train_acc = run_one_epoch(model, train_loader, criterion, device, optimizer)
        valid_loss, valid_acc = run_one_epoch(model, valid_loader, criterion, device)
        scheduler.step()

        is_best = valid_acc > best_acc or (valid_acc == best_acc and valid_loss < best_loss)
        if is_best:
            best_acc = valid_acc
            best_loss = valid_loss
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "num_classes": num_classes,
                    "label_to_action": label_to_action,
                    "epoch": epoch,
                    "valid_acc": valid_acc,
                    "valid_loss": valid_loss,
                    "args": serializable_args(args),
                },
                args.save_path,
            )

        print(
            f"epoch {epoch:03d}/{args.epochs} "
            f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} "
            f"valid_loss={valid_loss:.4f} valid_acc={valid_acc:.4f}"
            f"{' saved' if is_best else ''}"
        )

    checkpoint = torch.load(args.save_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    test_loss, test_acc = run_one_epoch(model, test_loader, criterion, device)
    print(
        f"best epoch={checkpoint['epoch']} valid_acc={checkpoint['valid_acc']:.4f} "
        f"test_loss={test_loss:.4f} test_acc={test_acc:.4f}"
    )
    print(f"saved best model dict to: {args.save_path}")


if __name__ == "__main__":
    main()
