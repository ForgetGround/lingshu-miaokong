# 固件参考

`esp32_reference/` 提供 `ESP32-S3-WROOM-1-N16R8` 参考固件骨架，用于说明硬件采集端如何以串口输出固定长度 EMG 窗口。

该固件是参考实现，默认按 8 路 EMG 输入组织数据，并输出 CSV 行：

```text
emg1_0,emg2_0,...,emg8_0,emg1_1,...,emg8_199
```

`include/config.h` 中的 GPIO 号需要按 EasyEDA netlist 做最终确认。

实际项目可在此基础上加入：

- BLE HID 或 BLE UART
- 采样率配置
- 滤波
- 电池电量上报
- 与上位机的命令协议
