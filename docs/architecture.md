# 架构说明

灵枢秒控的参考流程由三部分组成：

```text
EMG electrodes
  -> analog front-end / EMG sensor
  -> MCU or USB serial collector
  -> CSV windows with signal_0...signal_199
  -> PyTorch 1D ResNet18 classifier
  -> gesture label
```

## 软件

- `dataset.py` 负责读取 CSV、分层划分数据集、标准化特征。
- `model.py` 定义 1D ResNet18 分类器。
- `train.py` 负责训练、验证、测试和保存 checkpoint。
- `scripts/make_sample_dataset.py` 生成合成样例数据，用于 smoke test。

## 硬件参考

硬件目录提供一个基于 ESP32-S3 与模拟 EMG 输入模块的参考连接方案。该方案用于说明采集链路和接口，不等同于已完成量产的 PCB 设计。
