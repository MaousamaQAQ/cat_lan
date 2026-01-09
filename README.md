# 🐾 CAT 助手 | CAT Converter

## English

A lightweight floating CAT language encoding tool based on PyQt6. It converts plain text into "CAT language" (Meow, Woof, Mi, Ao) and provides convenient global hotkey and clipboard interaction.

### ✨ Features

* **CAT Encoding/Decoding**: One-click conversion between plain text and CAT language.
* **Minimalist Floating Window**:
* **Smart Interaction**: Shows a semi-transparent drag area when the mouse is near; hidden otherwise.
* **Always on Top**: The window stays above all other applications.
* **Built-in Clear Button**: A dynamic "✕" button inside the input field that appears only when text is present.


* **Global Hotkey**: Press `Alt + F1` to toggle the input window anytime.
* **System Tray**: Supports tray icon, bubble notifications, and quick exit.
* **Auto Positioning**: Automatically detects the taskbar and snaps to the bottom-right corner.

### 🛠️ Prerequisites

Before running or developing, ensure you have the following libraries installed:

```powershell
pip install pyperclip pystray keyboard Pillow PyQt6 pyinstaller

```

### 🚀 Quick Start

1. **Prepare Icon**: Name your icon file `cat.png` and place it in the project root.
2. **Run**:
```powershell
python cat_lan.py

```


3. **Usage**:
* Type text and press **Enter** or click **▶** to encode and copy to clipboard.
* Paste CAT language and click **◀** to decode and copy to clipboard.
* Use `Alt + F1` to toggle visibility.
* Right-click the tray icon for more options.



### 📦 Build Guide (EXE)

To package the program into a standalone `.exe` file:

```powershell
pyinstaller --noconsole --onefile --add-data "cat.png;." --icon="cat.png" cat_lan.py

```

---

## 中文

一个基于 PyQt6 的轻量级悬浮猫语编码工具。它可以将普通文本转换为“猫语”编码（喵呜咪嗷），并提供便捷的全局唤起和剪贴板交互功能。

### ✨ 功能特性

* **猫语编码/解码**：支持将文本一键转为猫语或还原为原始文本。
* **极简悬浮窗**：
* **智能交互**：鼠标靠近时显示半透明拖拽区，平时自动隐藏。
* **置顶显示**：窗口始终悬浮在所有应用最上层。
* **内置清除**：输入框内置动态“✕”号按钮，有文字时自动显示。


* **全局快捷键**：按下 `Alt + F1` 随时从系统后台唤起或隐藏输入框。
* **系统托盘**：支持托盘图标显示、气泡通知以及快速退出。
* **自动定位**：启动时自动识别任务栏位置，精准吸附于屏幕右下角。

### 🛠️ 环境准备

在运行或开发之前，请确保你的 Python 环境中已安装以下库：

```powershell
pip install pyperclip pystray keyboard Pillow PyQt6 pyinstaller

```

### 🚀 快速开始

1. **准备图标**：将你的图标文件命名为 `cat.png` 并放在项目根目录下。
2. **直接运行**：
```powershell
python cat_lan.py

```


3. **使用说明**：
* 在输入框输入文字，按回车或点击 **▶** 编码为猫语并自动复制到剪贴板。
* 将猫语粘贴进输入框，点击 **◀** 还原为原文并自动复制到剪贴板。
* 使用 `Alt + F1` 快速隐藏或显示工具条。
* 右键托盘图标可呼出菜单进行更多操作。



### 📦 打包指南 (EXE)

使用以下命令将程序打包为独立的 `.exe` 文件：

```powershell
pyinstaller --noconsole --onefile --add-data "cat.png;." --icon="cat.png" cat_lan.py

```

---

## 📂 Project Structure / 项目结构

```text
cat_lan/
├── cat_lan.py    # Main Code / 主程序代码
├── cat.png       # Icon / 程序图标
└── README.md     # Documentation / 项目说明文档

```

## ⚖️ License / 协议

This project is licensed under **CC BY-NC-SA 4.0**.
本项目采用 **CC BY-NC-SA 4.0** 协议授权。

[MaousamaQAQ © 2026]