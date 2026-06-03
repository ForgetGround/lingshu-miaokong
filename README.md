# 灵枢秒控

基于 PyTorch 的 1D ResNet18 EMG 手势分类训练项目。训练目标是将长度为 200 的肌电信号分类为三种手势：`fist`、`relax`、`open`。

> 当前仓库提供训练代码、数据格式、验证脚本和硬件参考资料。硬件部分是参考设计文件，尚未声明为已量产或已完成全套电气认证。

## 项目结构

```text
.
├── dataset.py        # 读取 CSV、分层划分训练/验证/测试集、标准化特征
├── model.py          # 1D ResNet18 手势分类模型
├── train.py          # 模型训练入口
├── scripts/          # 样例数据生成脚本
├── tests/            # 基础验证测试
├── docs/             # 架构、数据格式和验证说明
├── hardware/         # 硬件参考资料、BOM、接线和结构文件
├── firmware/         # ESP32-S3-WROOM-1-N16R8 参考固件骨架
├── requirements.txt  # Python 依赖
└── README.md
```

## 快速验证

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/make_sample_dataset.py --output emg_hand_gestures.csv --samples-per-class 24
python -m unittest discover -s tests
python train.py --epochs 1 --batch-size 16 --csv-path emg_hand_gestures.csv
```

完整验证说明见 [docs/verification.md](docs/verification.md)。

## 硬件

当前硬件主控选型为 `ESP32-S3-WROOM-1-N16R8`。硬件资料按当前原理图设计整理，包含 8 路 EMG/FPC 输入、AD8226 + TL084 ADC/EMG 放大器、USB-C、电池充电/供电和 5 指关节驱动输出说明。

详见 [hardware/README.md](hardware/README.md) 和 [hardware/reference-schematic.md](hardware/reference-schematic.md)。

## 数据格式

训练脚本默认读取根目录下的 `emg_hand_gestures.csv`。CSV 需要包含：

- `signal_0` 到 `signal_199`：长度为 200 的 EMG 信号特征列
- `label`：类别标签
- `action`：可选的手势名称列

数据格式细节见 [docs/data-format.md](docs/data-format.md)。

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
