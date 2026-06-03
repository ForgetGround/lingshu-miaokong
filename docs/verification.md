# 验证说明

本文档用于说明拉取仓库后的基础验证路径。

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

该脚本生成的是合成数据，仅用于验证代码链路，不代表真实 EMG 采集质量。

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
python train.py --epochs 1 --batch-size 16 --csv-path emg_hand_gestures.csv
```

该命令只验证训练流程可以执行，不用于证明模型真实准确率。

## 硬件资料验证

硬件参考资料位于 `hardware/`：

- `hardware/bom.csv`
- `hardware/pinout.csv`
- `hardware/connections.csv`
- `hardware/reference-schematic.md`
- `hardware/mechanical/mounting-plate.svg`

硬件资料描述参考连接关系和结构尺寸，实际打样前需要完成原理图 ERC、PCB DRC、安规和抗干扰验证。
