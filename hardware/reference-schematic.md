# 参考原理图说明

当前硬件选型按用户提供的原理图截图整理，主控为 `ESP32-S3-WROOM-1-N16R8` 模块。截图中的工程标题为“核心板 / 灵枢秒控”，日期信息显示为 2026-04-27 创建、2026-06-03 更新。

## 功能分区

```text
USB Type-C
  -> VBUS charger / power path
  -> ESP32-S3 native USB D+/D-

Li-ion/LiPo battery
  -> charger/protection
  -> power switch
  -> 3V3 regulator
  -> ESP32-S3-WROOM-1-N16R8

FPC connector
  -> GND
  -> EMG1..EMG8 analog inputs
  -> +5V harness rail

ADC / EMG amplifier
  -> electrode differential input
  -> AD8226 instrumentation amplifier
  -> TL084 active filtering / limiting / output conditioning
  -> OUT to MCU ADC after 0-3.3 V protection

ESP32-S3 GPIO nets
  -> IO1_1..IO5_3
  -> five-channel finger joint driver logic
  -> OUT1_1..OUT5_3 switched outputs
```

## 主控

- 模块：`ESP32-S3-WROOM-1-N16R8`
- Flash：16 MB
- PSRAM：8 MB
- 接口：原生 USB、ADC 输入、GPIO 输出、BOOT/RESET

## EMG 接口

截图右侧 FPC 连接器可见 `EMG1` 到 `EMG8`、`GND` 和 `+5V` 网络。仓库文档按 8 路 EMG 输入整理。

用户补充的 ADC 放大器原理图显示，EMG/ADC 前端由 `AD8226ARZ-R7` 仪表放大器和 `TL084CDT` 四运放构成，使用 `+9V`、`-9V` 双电源，末端输出网络名为 `OUT`。详见 `hardware/adc-amplifier.md`。

量产或打样前需要从 EasyEDA 源文件导出 netlist，确认每个 `EMGx` 连接到 ESP32-S3 的具体 ADC GPIO，并补充输入保护、RC 滤波和前端输出电压范围。由于放大器运行在 `±9V` 供电下，进入 ESP32-S3 ADC 前必须确认信号已经转换并限制在 MCU 允许的 ADC 电压范围内。

## 5 通道关节驱动

截图上方为“5通道关节驱动”，按 `Finger1` 到 `Finger5` 分组。每个 finger 下有 3 个输出级，网络命名呈现为：

- `OUT1_1`、`OUT1_2`、`OUT1_3`
- `OUT2_1`、`OUT2_2`、`OUT2_3`
- `OUT3_1`、`OUT3_2`、`OUT3_3`
- `OUT4_1`、`OUT4_2`、`OUT4_3`
- `OUT5_1`、`OUT5_2`、`OUT5_3`

控制侧对应 `IO1_1` 到 `IO5_3`。截图中每个输出级包含开关器件、SS34 二极管、LED 指示和 3.3 kOhm 电阻。

## 电源

截图中包含：

- USB Type-C 入口
- 充电/电源管理模块
- 电池 `BAT` 网络
- 电源开关
- 3V3 系统电源

人体接触 EMG 原型测试建议优先使用电池供电，并在确认隔离、保护和漏电风险前避免把人体接触前端接到不安全电源路径。

## 仍需补充

- EasyEDA 原理图源文件或 PDF 导出件
- PCB layout、Gerber、BOM 采购链接
- ERC/DRC 报告
- `EMG1..EMG8` 到具体 GPIO 的 netlist
- `IO1_1..IO5_3` 到具体 GPIO 的 netlist
- ADC 放大器 `OUT` 到 ESP32-S3 ADC 前的电平转换/保护电路
- 输出级负载类型、额定电流、发热和保护验证
