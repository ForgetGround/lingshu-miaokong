# 硬件参考资料

本目录提供灵枢秒控的硬件参考资料，用于说明当前原型方案的主要模块、接口和待验证项。

当前主控选型：`ESP32-S3-WROOM-1-N16R8`。

## 文件

| 文件 | 说明 |
| --- | --- |
| `bom.csv` | 参考物料清单 |
| `pinout.csv` | MCU 网络/引脚分配待复核表 |
| `connections.csv` | 模块连接关系 |
| `adc-amplifier.md` | AD8226 + TL084 ADC/EMG 放大器说明 |
| `reference-schematic.md` | 文本版参考原理图 |
| `safety-notes.md` | 佩戴和采集安全注意事项 |
| `mechanical/mounting-plate.svg` | 参考安装板 2D 图 |

## 状态说明

这些文件根据当前原理图设计整理，用于开源验证和原型搭建。硬件打样或发布前仍需补充：

- 完整 EasyEDA 原理图源文件、PDF 导出件和 PCB layout
- ERC/DRC 报告
- 真实 BOM 采购链接和替代料评估
- 模拟前端噪声、滤波、ESD 和隔离验证
- ADC 放大器输出到 ESP32-S3 ADC 之间的电平转换和保护验证
- 佩戴安全和电气安全验证
