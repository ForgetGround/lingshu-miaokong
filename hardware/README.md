# 硬件参考资料

本目录提供灵枢秒控的硬件参考包，用于说明验证者可以如何搭建 EMG 采集链路。

## 文件

| 文件 | 说明 |
| --- | --- |
| `bom.csv` | 参考物料清单 |
| `pinout.csv` | MCU 引脚分配 |
| `connections.csv` | 模块连接关系 |
| `reference-schematic.md` | 文本版参考原理图 |
| `safety-notes.md` | 佩戴和采集安全注意事项 |
| `mechanical/mounting-plate.svg` | 参考安装板 2D 图 |

## 状态说明

这些文件用于开源验证和原型搭建。正式硬件发布前仍需补充：

- 完整 EDA 原理图和 PCB layout
- ERC/DRC 报告
- 真实 BOM 采购链接和替代料评估
- 模拟前端噪声、滤波、ESD 和隔离验证
- 佩戴安全和电气安全验证
