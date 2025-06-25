#!/bin/bash

APP_PATH="/home/devansharora18/Documents/lenovo-yoga-sleep-fix/sleep_toggle.py"
LID_STATE="/proc/acpi/button/lid/LID0/state"


# Disable radios
rfkill block bluetooth
nmcli radio wifi off

# Stop background services
systemctl --user stop tracker-miner-fs-3.service 2>/dev/null
systemctl --user stop tracker-extract-3.service 2>/dev/null
systemctl --user stop evolution-calendar-factory.service 2>/dev/null

# Pause background apps
pkill -STOP chrome
pkill -STOP code
pkill -STOP gnome-shell
pkill -STOP spotify



# Wait until lid is opened (script continues once thawed)
while grep -i closed "$LID_STATE" > /dev/null; do
    sleep 1
done


# Re-enable radios
rfkill unblock bluetooth
nmcli radio wifi on

# Restart background services
systemctl --user start tracker-miner-fs-3.service 2>/dev/null
systemctl --user start tracker-extract-3.service 2>/dev/null
systemctl --user start evolution-calendar-factory.service 2>/dev/null

# Resume background apps
pkill -CONT chrome
pkill -CONT code
pkill -CONT gnome-shell
pkill -CONT spotify

# Relaunch tray app
python3 "$APP_PATH" &

exit 0
