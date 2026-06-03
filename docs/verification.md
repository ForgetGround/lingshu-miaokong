# 验证说明

本文档说明拉取仓库后的基础验证路径。验证目标是确认代码链路可运行，不用于证明真实硬件性能或模型准确率。

## 环境

- Python 3.10 或更新版本
- `numpy`
- `pandas`
- `torch`

安装：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 生成样例数据

```bash
python scripts/make_sample_dataset.py --output emg_hand_gestures.csv --samples-per-class 24
```

该脚本生成合成数据，仅用于验证数据读取、测试和训练流程。

## 运行测试

```bash
python -m unittest discover -s tests
```

测试覆盖：

- CSV 数据读取
- 分层训练/验证/测试集划分
- 特征张量形状
- 1D ResNet18 前向传播输出形状

## 训练冒烟测试

```bash
python train.py --epochs 1 --batch-size 16 --csv-path emg_hand_gestures.csv --save-path /tmp/lingshu_smoke_model.pth
```

该命令只验证训练流程可以执行。合成数据上的准确率不应作为真实性能指标。

## 硬件资料复核

硬件参考资料位于 `hardware/`：

- `hardware/README.md`
- `hardware/bom.csv`
- `hardware/pinout.csv`
- `hardware/connections.csv`
- `hardware/adc-amplifier.md`
- `hardware/reference-schematic.md`
- `hardware/safety-notes.md`
- `hardware/mechanical/mounting-plate.svg`

硬件资料按 `ESP32-S3-WROOM-1-N16R8` 原型方案整理。实际打样或对外发布硬件文件前，需要完成原理图源文件复核、ERC、PCB DRC、BOM 替代料评估、模拟前端安全验证和输出驱动负载验证。
