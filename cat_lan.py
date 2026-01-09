import sys, re, pyperclip, pystray, keyboard, os
from PIL import Image
from threading import Thread
from pystray import MenuItem as item
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt, pyqtSignal


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# --- 核心 CAT 编码逻辑 ---
TRANS_TABLE = str.maketrans("0123喵呜咪嗷", "喵呜咪嗷0123")

def to_cat(text):
    if not text: return ""
    try:
        raw_bytes = text.encode("utf-8-sig")
        base4_str = "".join(f"{(b >> i) & 3}" for b in raw_bytes for i in (6, 4, 2, 0))
        return re.sub(r'(\d)\1\1', r'\1~', base4_str).translate(TRANS_TABLE)
    except Exception as e:
        return f"[编码错误: {e}]"


def from_cat(cat_str):
    if not cat_str: return ""
    try:
        s = re.sub(r'(\d)~', r'\1\1\1', cat_str.translate(TRANS_TABLE))
        byte_list = [int(s[i:i + 4], 4) for i in range(0, len(s), 4) if len(s[i:i + 4]) == 4]
        return bytes(byte_list).decode("utf-8-sig")
    except Exception as e:
        return f"[解码错误: {e}]"


class FloatingInputWindow(QWidget):
    toggle_signal = pyqtSignal()

    def __init__(self, tray_app):
        super().__init__()
        self.tray_app, self.m_drag = tray_app, False
        self.toggle_signal.connect(self.toggle_visibility)
        self.init_ui()
        self.setup_global_hotkey()

    def init_ui(self):
        # 强制置顶并设为工具窗口
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.bg_frame = QFrame(self)
        self.bg_frame.setObjectName("bgFrame")
        self.update_bg_style(active=False)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.addWidget(self.bg_frame)

        content_layout = QHBoxLayout(self.bg_frame)
        content_layout.setContentsMargins(10, 5, 10, 5)
        content_layout.setSpacing(10)

        base_btn_style = """
            QPushButton { 
                background-color: #FFB6C1; color: white; border-radius: 20px; 
                font-size: 22px; font-family: 'Segoe UI Symbol';
            } 
            QPushButton:hover { background-color: #FF69B4; }
        """

        self.rev_btn = QPushButton("◀", clicked=lambda: self.process_text(from_cat, "已还原喵！"))
        self.rev_btn.setFixedSize(40, 40)
        self.rev_btn.setStyleSheet(base_btn_style + "QPushButton { padding-right: 4px; }")

        # --- 输入框 ---
        self.input_field = QLineEdit(placeholderText="输入文字...")
        self.input_field.setFixedSize(260, 40)
        self.input_field.setTextMargins(0, 0, 30, 0)
        self.input_field.setStyleSheet("""
            QLineEdit { background: white; border: 2px solid #FFB6C1; 
                        border-radius: 20px; padding: 0 15px; font-size: 14px; color: #333; }
        """)

        # --- 叉叉按钮 (默认隐藏) ---
        self.clear_btn = QPushButton("✕", self.input_field)
        self.clear_btn.setFixedSize(30, 30)
        self.clear_btn.move(260 - 35, 5)
        self.clear_btn.setVisible(False)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setStyleSheet(
            "QPushButton { background:none; border:none; color:#ccc; font-size:16px; } QPushButton:hover { color:#f44336; }")

        # 交互逻辑：文字变动显示/隐藏叉叉
        self.input_field.textChanged.connect(self.update_clear_btn)
        self.clear_btn.clicked.connect(self.input_field.clear)
        self.input_field.returnPressed.connect(lambda: self.process_text(to_cat, "已转为猫语喵！"))

        self.send_btn = QPushButton("▶", clicked=lambda: self.process_text(to_cat, "已转为猫语喵！"))
        self.send_btn.setFixedSize(40, 40)
        self.send_btn.setStyleSheet(base_btn_style + "QPushButton { padding-left: 4px; }")

        content_layout.addWidget(self.rev_btn)
        content_layout.addWidget(self.input_field)
        content_layout.addWidget(self.send_btn)

        # --- 初始位置定位在右下角 ---
        self.setFixedSize(430, 80)
        self.move_to_corner()

    def update_clear_btn(self, text):
        self.clear_btn.setVisible(len(text) > 0)

    def move_to_corner(self):
        # 获取屏幕可用区域（排除任务栏）
        screen_geo = QApplication.primaryScreen().availableGeometry()
        x = screen_geo.width() - self.width() - 20  # 距离右边 20px
        y = screen_geo.height() - self.height() - 20  # 距离任务栏上方 20px
        self.move(x, y)

    def update_bg_style(self, active):
        color = "rgba(100, 100, 100, 40)" if active else "transparent"
        self.bg_frame.setStyleSheet(f"#bgFrame {{ background-color: {color}; border-radius: 30px; }}")

    def enterEvent(self, event):
        self.update_bg_style(active=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update_bg_style(active=False)
        super().leaveEvent(event)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.m_drag = True
            self.m_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.m_drag: self.move(e.globalPosition().toPoint() - self.m_pos)

    def mouseReleaseEvent(self, e):
        self.m_drag = False

    def setup_global_hotkey(self):
        try:
            keyboard.add_hotkey('alt+f1', lambda: self.toggle_signal.emit())
        except:
            pass

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
            self.input_field.setFocus()

    def process_text(self, func, msg):
        if text := self.input_field.text().strip():
            pyperclip.copy(func(text))
            self.input_field.clear()
            if self.tray_app.icon: self.tray_app.icon.notify(msg, "CAT助手")


class CatTrayApp:
    def __init__(self):
        self.icon, self.window = None, None

    def run_gui(self):
        app = QApplication(sys.argv)
        self.window = FloatingInputWindow(self)
        self.window.show()
        Thread(target=self.setup_tray, daemon=True).start()
        sys.exit(app.exec())

    def setup_tray(self):
        cat_icon_path = get_resource_path("cat.png")
        try:
            img = Image.open(cat_icon_path)
        except:
            img = Image.new('RGB', (64, 64), (255, 182, 193))

        self.icon = pystray.Icon("cat_converter", img, "CAT 助手", pystray.Menu(
            item('显示/隐藏 (Alt+F1)', lambda: self.window.toggle_signal.emit()),
            item('退出', lambda icon: [icon.stop(), QApplication.quit()])
        ))
        self.icon.run()


if __name__ == "__main__":
    CatTrayApp().run_gui()