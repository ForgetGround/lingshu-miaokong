# 固件参考

`esp32_reference/` 提供 `ESP32-S3-WROOM-1-N16R8` 参考固件骨架，用于说明硬件采集端如何组织 8 路 EMG 采样和串口输出。

该固件是参考实现，默认按 8 路 EMG 输入组织数据，并输出一行交错排列的 CSV 数据：

```text
emg1_0,emg2_0,...,emg8_0,emg1_1,...,emg8_199
```

`include/config.h` 中的 GPIO 号需要按 EasyEDA netlist 做最终确认。

注意：当前 Python 训练脚本消费的是单通道 `signal_0...signal_199` 训练窗口。固件输出接入训练前，需要先转换为训练 CSV 格式，或扩展训练代码支持多通道输入。

实际项目可在此基础上加入：

- BLE HID 或 BLE UART
- 采样率配置
- 滤波
- 电池电量上报
- 与上位机的命令协议
