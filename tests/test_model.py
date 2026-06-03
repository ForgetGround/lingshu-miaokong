import unittest

import torch

from model import create_model


class ModelTest(unittest.TestCase):
    def test_forward_shape(self) -> None:
        model = create_model(num_classes=3, dropout=0.1)
        model.eval()

        with torch.no_grad():
            logits = model(torch.randn(4, 1, 200))

        self.assertEqual(tuple(logits.shape), (4, 3))


if __name__ == "__main__":
    unittest.main()
