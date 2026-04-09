```markdown
# 自己在家测视力 (HomeVision-Toolkit)

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

这是一个基于 Python Tkinter 开发的居家视力自测工具。通过精确的物理像素校准，将国家标准视力表搬到你的电脑屏幕上，足不出户即可完成初步的视力筛查。

## 🌟 功能亮点
* **精准校准**：内置物理尺子校准功能，消除不同屏幕分辨率带来的误差。
* **国标标准**：严格遵循 GB 11533-2011 视力表标准设计。
* **功能全面**：
  * 标准对数视力表 (E字表)
  * 散光钟形图
  * 红绿平衡对比测试
  * 蜂窝图检测
  * 交叉十字线
  * Worth四点图 (双眼视功能检查)
* **交互友好**：支持全键盘快捷键操作，方便远距离测试。

## 🚀 快速开始

### 方式一：直接运行 (推荐)
1. 前往本仓库的 [Releases](https://github.com/LunaSpica/SelfSight-Checker/releases) 页面。
2. 下载最新的压缩包，解压后双击运行 `.exe` 文件即可。

### 方式二：源码运行
如果你想学习或修改代码，请确保已安装 Python 环境：
```bash
# 克隆仓库
git clone [https://github.com/LunaSpica/SelfSight-Checker.git](https://github.com/LunaSpica/SelfSight-Checker.git)
cd SelfSight-Checker

# 安装依赖
pip install -r requirements.txt

# 运行程序
python src/main.py
```

## 🎮 使用说明
1. **屏幕校准**：启动后，请使用直尺测量屏幕上蓝色方块的实际高度（单位：mm），并输入系统。
2. **测试距离**：请确保眼睛距离屏幕 **5米** 远。
3. **快捷键操作**：
   - `1 - 7`：快速切换不同的检测模式。
   - `方向键 ← / →`：循环切换模式。
   - `方向键 ↑ / ↓`：视力表模式下切换行；其他模式下进行画面缩放。

## 📂 项目结构
```text
.
├── src/                # 源代码及图片资源
│   ├── main.py         # 主程序入口
│   └── *.png           # 视力检测相关图表
├── .gitignore          # Git 忽略配置
└── README.md           # 项目说明文档
```

## 🛠️ 技术栈
- **Language**: Python
- **GUI Framework**: Tkinter
- **Image Processing**: Pillow (PIL)
- **Packaging**: PyInstaller

## ⚠️ 免责声明
本软件仅作为居家视力筛查参考，测试结果不具有医学诊断效力。如需准确的验光数据，请前往正规医院或眼科机构。
```