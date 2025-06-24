#!/usr/bin/env python3

import sys
import subprocess
import threading
import time
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

def is_sleep_masked():
    result = subprocess.run(["systemctl", "is-enabled", "sleep.target"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return b"masked" in result.stdout or b"masked" in result.stderr

def mask_sleep():
    subprocess.run(["pkexec", "systemctl", "mask",
                    "sleep.target", "suspend.target", "hibernate.target", "hybrid-sleep.target"])

def unmask_sleep():
    subprocess.run(["pkexec", "systemctl", "unmask",
                    "sleep.target", "suspend.target", "hibernate.target", "hybrid-sleep.target"])

def create_circle_icon(color: str) -> QIcon:
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setBrush(QColor(color))
    painter.setPen(QColor("black"))
    painter.drawEllipse(8, 8, 48, 48)
    painter.end()
    return QIcon(pixmap)

def monitor_lid():
    lid_path = "/proc/acpi/button/lid/LID0/state"
    last_state = "open"

    while True:
        try:
            with open(lid_path, "r") as f:
                state = f.read().strip().lower()
            is_closed = "closed" in state
        except:
            is_closed = False

        if is_closed and last_state != "closed" and is_sleep_masked():
            subprocess.run(["loginctl", "lock-session"])
        last_state = "closed" if is_closed else "open"
        time.sleep(1)

class SleepTrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray = QSystemTrayIcon()

        self.menu = QMenu()
        self.toggle_action = QAction("")
        self.toggle_action.triggered.connect(self.toggle_sleep)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.app.quit)

        self.menu.addAction(self.toggle_action)
        self.menu.addSeparator()
        self.menu.addAction(quit_action)

        self.tray.setContextMenu(self.menu)
        self.tray.setToolTip("Toggle Sleep/Suspend")
        self.update_icon()
        self.tray.setVisible(True)

        # Start lid monitoring thread
        threading.Thread(target=monitor_lid, daemon=True).start()

        sys.exit(self.app.exec())

    def toggle_sleep(self):
        if is_sleep_masked():
            unmask_sleep()
        else:
            mask_sleep()
        self.update_icon()

    def update_icon(self):
        if is_sleep_masked():
            self.tray.setIcon(create_circle_icon("red"))
            self.toggle_action.setText("Enable Sleep")
        else:
            self.tray.setIcon(create_circle_icon("green"))
            self.toggle_action.setText("Disable Sleep")

if __name__ == "__main__":
    SleepTrayApp()
