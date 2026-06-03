# 灵枢秒控

灵枢秒控是一个面向肌电（EMG）手势识别原型的开源参考项目。仓库包含 PyTorch 训练代码、合成样例数据生成脚本、基础测试、ESP32-S3 参考固件骨架和硬件参考资料。

当前训练代码实现的是单通道、长度为 200 的 1D EMG 窗口分类，默认识别三类手势：`fist`、`relax`、`open`。

## 项目状态

本仓库适用于代码链路验证、硬件方案复核和原型开发参考。硬件资料为参考设计整理，不包含生产验证、医疗器械认证或电气安全认证结论。合成样例数据仅用于 smoke test，不代表真实 EMG 数据质量或模型准确率。详细范围见 [docs/project-status.md](docs/project-status.md)。

当前限制：

- 训练脚本消费 `signal_0` 到 `signal_199` 的单通道窗口。
- 参考固件按 8 路 EMG 采集框架组织，输出格式需要在接入训练前转换为训练 CSV 格式。
- 硬件 GPIO 映射仍需依据 EasyEDA 原理图源文件或 netlist 复核。
- ADC/EMG 放大器使用 `+9V/-9V` 模拟电源，接入 ESP32-S3 ADC 前必须完成电平转换、限流和钳位保护验证。

## 仓库结构

```text
.
├── dataset.py        # CSV 读取、分层划分、标准化和 Dataset 封装
├── model.py          # 1D ResNet18 EMG 分类模型
├── train.py          # 训练、验证、测试和 checkpoint 保存入口
├── scripts/          # 样例数据生成脚本
├── tests/            # 基础单元测试
├── docs/             # 架构、数据格式、验证和项目状态说明
├── hardware/         # 硬件参考资料、BOM、连接关系和安全说明
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
python train.py --epochs 1 --batch-size 16 --csv-path emg_hand_gestures.csv --save-path /tmp/lingshu_smoke_model.pth
```

完整验证流程见 [docs/verification.md](docs/verification.md)。

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

详细说明见 [docs/data-format.md](docs/data-format.md)。

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

Checkpoint 默认保存为 `best_model_dict.pth`，包含 `model_state_dict`、`num_classes`、`label_to_action`、`epoch`、`valid_acc`、`valid_loss` 和训练参数。

## 硬件

当前硬件参考方案使用 `ESP32-S3-WROOM-1-N16R8` 模块，包含 8 路 EMG/FPC 输入、AD8226 + TL084 ADC/EMG 放大器、USB-C、电池充电/供电和 5 指关节驱动输出说明。

硬件资料入口：

- [hardware/README.md](hardware/README.md)
- [hardware/reference-schematic.md](hardware/reference-schematic.md)
- [hardware/adc-amplifier.md](hardware/adc-amplifier.md)
- [hardware/safety-notes.md](hardware/safety-notes.md)

## 参与贡献

提交问题或改动前请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。硬件相关改动应尽量附带原理图源文件、netlist、BOM 依据或实测记录。

## 许可证

本项目基于 MIT License 开源。
