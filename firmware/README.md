# 固件参考

`esp32_reference/` 提供 ESP32-S3 参考固件骨架，用于说明硬件采集端如何以串口输出固定长度 EMG 窗口。

该固件是参考实现，默认读取 `EMG_ADC_PIN` 并输出 CSV 行：

```text
signal_0,signal_1,...,signal_199
```

实际项目可在此基础上加入：

- BLE HID 或 BLE UART
- 采样率配置
- 滤波
- 电池电量上报
- 与上位机的命令协议
