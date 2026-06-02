# 灵枢秒控

基于 PyTorch 的 1D ResNet18 EMG 手势分类训练项目。训练目标是将长度为 200 的肌电信号分类为三种手势：`fist`、`relax`、`open`。

## 项目结构

```text
.
├── dataset.py        # 读取 CSV、分层划分训练/验证/测试集、标准化特征
├── model.py          # 1D ResNet18 手势分类模型
├── train.py          # 模型训练入口
├── requirements.txt  # Python 依赖
└── README.md
```

## 数据格式

训练脚本默认读取根目录下的 `emg_hand_gestures.csv`。CSV 需要包含：

- `signal_0` 到 `signal_199`：长度为 200 的 EMG 信号特征列
- `label`：类别标签
- `action`：可选的手势名称列

当前类别映射：

| label | action |
| --- | --- |
| 0 | `fist` |
| 1 | `relax` |
| 2 | `open` |

## 安装依赖

建议使用 Python 3.10 或更新版本。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

如果需要 CUDA 版本的 PyTorch，请根据本机 CUDA 环境选择对应的 `torch` 安装方式。

## 训练

```bash
python train.py
```

常用参数：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--csv-path` | `emg_hand_gestures.csv` | 训练数据 CSV 路径 |
| `--save-path` | `best_model_dict.pth` | 最佳模型保存路径 |
| `--epochs` | `50` | 训练轮数 |
| `--batch-size` | `64` | batch size |
| `--lr` | `1e-3` | 学习率 |
| `--weight-decay` | `1e-4` | AdamW 权重衰减 |
| `--valid-ratio` | `0.15` | 验证集比例 |
| `--test-ratio` | `0.15` | 测试集比例 |
| `--dropout` | `0.1` | 全连接层前的 dropout |
| `--seed` | `42` | 随机种子 |
| `--num-workers` | `0` | DataLoader worker 数量 |
| `--device` | 自动选择 `cuda` 或 `cpu` | 训练设备 |

示例：

```bash
python train.py --epochs 10 --batch-size 64 --lr 0.001
```

## Checkpoint

默认保存路径：

```text
best_model_dict.pth
```

保存的 checkpoint 包含：

- `model_state_dict`
- `num_classes`
- `label_to_action`
- `epoch`
- `valid_acc`
- `valid_loss`
- `args`

## 许可证

本项目基于 MIT License 开源。
