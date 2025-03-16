# Hackaday2025_badge - *the MacGyver Hack*

This repository documents what has been done with the Hackaday Europe 2025 badge during the event and how.

It is loosely based on the [2024 Supercon 8 Add-On Badge](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge).

![Hackaday 2025 badge](img/badge_1.png)

## Features

- Extended firmware of the **Bendy Add-on** to enable remote control via I2C:
  - Firmware repository: [hackaday2025_bsao_addon](https://github.com/bastlirna/hackaday2025_bsao_addon)
  - MicroPython class: [bendy.py](https://github.com/bastlirna/hackaday2025_badge/blob/main/filesystem/bendy.py)
  - Change blinking modes using buttons on the badge.
- Using SoftI2C for the **Etch sAo Sketch** add-on.
- Reading accelerometer data from the **Etch sAo Sketch** add-on.
- Drawing QR codes on the display of the **Etch sAo Sketch** add-on.
- Changing displayed content when flipping the board (detected via accelerometer data).

Check [commit messages](https://github.com/bastlirna/hackaday2025_badge/commits/main/) for more details.

## Notes

- The **Etch sAo Sketch** needs to be connected to port 6.
- The **Bendy SAO** should be connected to port 3 and flashed with firmware from the [hackaday2025_bsao_addon](https://github.com/bastlirna/hackaday2025_bsao_addon) repository.
- The Petal and Touch Wheel SAOs (if used) should be connected to I2C bus 0 (ports 1 and 2; order doesn't matter).