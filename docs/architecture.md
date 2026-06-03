# 架构说明

灵枢秒控当前以“数据采集参考 + 单通道模型训练”为主线组织：

```text
EMG electrodes
  -> AD8226 + TL084 analog front-end
  -> ESP32-S3-WROOM-1-N16R8 sampling firmware
  -> data conversion / windowing
  -> CSV windows with signal_0...signal_199
  -> PyTorch 1D ResNet18 classifier
  -> gesture label
```

## 软件

- `dataset.py` 负责读取 CSV、分层划分数据集、标准化特征。
- `model.py` 定义 1D ResNet18 分类器。
- `train.py` 负责训练、验证、测试和保存 checkpoint。
- `scripts/make_sample_dataset.py` 生成合成样例数据，用于 smoke test。

当前模型输入为单通道 200 点窗口。8 路 EMG 的通道选择、通道融合或多通道模型结构尚未在训练代码中实现。

## 固件

`firmware/esp32_reference/` 是 ESP32-S3 参考固件骨架，用于展示 8 路 EMG 采样和串口输出组织方式。GPIO 映射为占位配置，硬件调试前需要依据原理图 netlist 更新。

## 硬件

硬件目录提供基于 `ESP32-S3-WROOM-1-N16R8` 的原型参考资料。当前硬件资料覆盖：

- 8 路 EMG/FPC 输入
- AD8226 + TL084 ADC/EMG 放大器
- USB-C 和电池供电/充电
- 电源开关和 3V3 系统电源
- 5 指、每指 3 路的关节驱动输出

这些资料用于方案复核和原型开发参考，不等同于已完成生产验证的硬件发布包。
