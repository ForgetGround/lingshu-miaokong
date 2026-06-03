import tempfile
import unittest
from pathlib import Path

from dataset import create_datasets
from scripts.make_sample_dataset import LABEL_TO_ACTION, make_signal


class DatasetTest(unittest.TestCase):
    def test_create_datasets_from_csv(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "sample.csv"
            self._write_sample_csv(csv_path)

            train_dataset, valid_dataset, test_dataset, label_to_action = create_datasets(
                csv_path=csv_path,
                valid_ratio=0.2,
                test_ratio=0.2,
                seed=7,
            )

            self.assertEqual(label_to_action, LABEL_TO_ACTION)
            self.assertGreater(len(train_dataset), len(valid_dataset))
            self.assertGreater(len(train_dataset), len(test_dataset))
            features, label = train_dataset[0]
            self.assertEqual(tuple(features.shape), (1, 200))
            self.assertGreaterEqual(int(label), 0)

    @staticmethod
    def _write_sample_csv(csv_path: Path) -> None:
        import csv
        import numpy as np

        rng = np.random.default_rng(123)
        fieldnames = [f"signal_{index}" for index in range(200)] + ["label", "action"]
        with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for label, action in LABEL_TO_ACTION.items():
                for _ in range(10):
                    signal = make_signal(label=label, length=200, rng=rng)
                    row = {f"signal_{index}": value for index, value in enumerate(signal)}
                    row["label"] = label
                    row["action"] = action
                    writer.writerow(row)


if __name__ == "__main__":
    unittest.main()
