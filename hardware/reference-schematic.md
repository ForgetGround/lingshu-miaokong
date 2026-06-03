# 参考原理图

```text
        Ag/AgCl electrodes
     E1      E2      E3(ref)
      |       |        |
      +-------+--------+
              |
       Analog EMG sensor
      +-----------------+
      | IN+ IN- REF     |
      | OUT VCC GND     |
      +--|---|---|------+
         |   |   |
         |   |   +---------------- ESP32-S3 GND
         |   +-------------------- ESP32-S3 3V3
         +------------------------ ESP32-S3 GPIO4 / ADC

  LiPo battery -> charger/protection -> power switch -> ESP32-S3 power input
  ESP32-S3 USB-C -> host computer for firmware upload and serial streaming
```

## 模拟输入

- `GPIO4` 仅作为参考 ADC 引脚，实际开发板应按可用 ADC 通道调整。
- 模拟前端输出必须限制在 MCU ADC 允许电压范围内。
- 推荐使用电池供电做人体接触测试，避免不安全的电源路径。

## 后续 PCB 化建议

- 模拟前端与数字射频区域分区布局。
- 参考地线靠近模拟前端回流。
- 电极输入加入 ESD 保护和限流。
- 为模拟输入预留 RC 低通滤波焊盘。
- 完成 ERC、DRC 和实测噪声评估后再发布 Gerber。
