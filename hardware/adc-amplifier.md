# ADC / EMG 放大器

本文件根据 ADC 放大器原理图设计整理。该前端用于把电极/传感器差分信号放大、滤波、限幅并输出到后级 ADC 采样链路。

## 信号链

```text
Differential electrode input
  -> input clamp / protection diodes
  -> AD8226 instrumentation amplifier
  -> AC coupling
  -> TL084 active stage
  -> diode limiter / rectifier network
  -> TL084 active filter stage
  -> TL084 final output stage
  -> OUT
  -> ADC input conditioning
  -> ESP32-S3 ADC
```

## 主要器件

| Reference | Part | Description |
| --- | --- | --- |
| `U1` | `AD8226ARZ-R7` | 仪表放大器，差分输入一级 |
| `U3.1`..`U3.4` | `TL084CDT` | 四运放，用于后级滤波、限幅和输出调理 |
| `R2` | `240R` | AD8226 增益电阻 |
| `R10/R8/R7/R6/R9` | `150k` | TL084 级间电阻网络 |
| `R4/R5` | `80.6k` | 有源滤波网络电阻 |
| `R1` | `10k` | 末级反馈电阻 |
| `R3` | `1k` | 末级输入电阻 |
| `C4` | `10nF` | 级间耦合/滤波电容 |
| `C1/C2/C3` | `1uF` | 电源去耦和滤波电容 |
| `D1/D2/D3/D17` | TBD | 输入/级间保护、限幅或整形二极管，需以 EasyEDA 源文件确认型号 |

## 电源

原理图中放大器使用双电源：

- `+9V`
- `-9V`
- `GND`

`C1` 和 `C2` 位于 `+9V`、`-9V` 与 `GND` 附近，作为模拟电源去耦。

## ADC 接口注意事项

ESP32-S3 ADC 输入不能直接承受负电压或高于芯片允许范围的电压。由于该放大器以 `±9V` 供电，`OUT` 接入 ESP32-S3 前必须完成以下验证：

- `OUT` 的静态偏置是否位于 ADC 可采样范围内。
- 最大手势信号、断线、饱和和上电瞬间是否会超过 ADC 允许电压。
- 是否已有分压、偏置、钳位、限流和 RC 滤波。
- 是否需要把双极性信号平移为 `0-3.3V` 单端信号。
- ADC 采样源阻抗是否满足 ESP32-S3 ADC 采样要求。

## 需要从源文件复核

- 二极管 `D1/D2/D3/D17` 的具体型号和方向。
- `OUT` 到主控板 `EMGx` 的连接关系。
- 每一路 EMG 是否共用相同放大器拓扑。
- `+9V/-9V` 电源产生方式、纹波和噪声。
- 输入端人体接触安全、限流、ESD 和隔离措施。
