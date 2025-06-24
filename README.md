# Sleep Fix for Lenovo Yoga 

## Overview

A lightweight PyQt6 system tray application to quickly **enable** or **disable** all Linux sleep modes (suspend, hibernate, hybrid) and handle lid-close behavior on Lenovo Yoga laptops. This addresses known issues with **Modern Standby (S0ix/s2idle)** on Lenovo hardware.

## Background & Issues

1. **No S3 Sleep Support**: Lenovo Yoga Slim 7 firmware does not support traditional S3 (deep) sleep, only Modern Standby (`s2idle`).
2. **Slow Resume**: Linux resume from Modern Standby takes **15–20 seconds**, significantly longer than traditional S3 sleep.
3. **Forced Suspend on Lid Close**: Firmware ignores OS-level settings (`logind.conf`), forcing suspend on lid close even when disabled in systemd.

## Root Cause

* Firmware and ACPI quirks on Lenovo override Linux `HandleLidSwitch` settings.
* Modern Standby implementation in Linux combined with NVMe/graphics delays can prolong wake time.

## Solution

1. **Mask All Sleep Targets**: Prevent system suspend, hibernate, hybrid-sleep via `systemctl mask`.
2. **Tray App Toggle**: Use a PyQt6 tray icon (green/red) to mask or unmask sleep targets with one click.
3. **Custom Lid Handler**: Poll `/proc/acpi/button/lid/LID0/state` in Python; if sleep is disabled and lid closes, **lock the screen** instead of suspending.

## Features

* **Enable/Disable Sleep**: Toggle all sleep modes at once.
* **Visual Indicator**: Green circle = sleep enabled; Red circle = sleep disabled.
* **Automatic Lock**: When sleep is disabled, closing the lid automatically locks the session (via `loginctl lock-session`).
* **Wayland & GNOME Compatible**: Uses PyQt6, works under Wayland with GNOME AppIndicator extension.

## Installation

1. **Dependencies**:

   ```bash
   sudo dnf install python3-qt6 pkexec libappindicator-gtk3
   pip install PyQt6
   ```
2. **Clone & Run**:

   ```bash
   git clone https://github.com/devansharora18/lenovo-yoga-sleep-fix.git
   cd lenovo-yoga-sleep-fix
   chmod +x sleep_toggle.py
   ./sleep_toggle.py
   ```
3. **Sudo Without Password** (optional):

   ```bash
   sudo visudo
   # add:
   youruser ALL=(ALL) NOPASSWD: /bin/systemctl mask *, /bin/systemctl unmask *, /usr/bin/loginctl
   ```

## Usage

* **Left-click** tray icon to toggle sleep modes.
* **Close lid** when sleep is disabled to auto-lock session.

## Autostart

To launch the tray app automatically when you log in:

1. Create an autostart directory if it doesn't exist:

   ```bash
   mkdir -p ~/.config/autostart
   ```
2. Create a `.desktop` file:

   ```bash
   cat << 'EOF' > ~/.config/autostart/sleep-toggle.desktop
   [Desktop Entry]
   Type=Application
   Name=Sleep Toggle
   Exec=/usr/bin/env python3 /home/yourusername/lenovo-yoga-sleep-fix/sleep_toggle.py
   X-GNOME-Autostart-enabled=true
   Comment=Toggle Linux sleep modes from system tray
   EOF

   ```
3. Make sure the script is executable:

   ```bash
   chmod +x /home/youruser/lenovo-yoga-sleep-fix/sleep_toggle.py
   ```

Replace `/home/youruser/lenovo-yoga-sleep-fix/` with the actual path to your script.

## File Structure

```
├── sleep_toggle.py   # Main PyQt6 tray app
└── README.md             # This documentation
```

## Contributing

Feel free to use and modify this code for personal use. Contributions and improvements are welcome! If you find bugs or have feature requests, please open an issue on the GitHub repository.
