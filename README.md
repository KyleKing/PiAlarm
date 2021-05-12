**Archived**: started refactoring for better architecture, full test coverage, and improving the mechanical and electrical design. However, I can't quite make a polished exterior that I am happy with. For now, I've decided to archive this project with the hope that I might revisit it in the future

---

# PiAlarm

Raspberry Pi Smart Alarm Clock. RGB light strip, buzzer, character LCD display, and web app

## Tech

- Integrations
  - Plotly/Dash application to handle UI, basic HTML authentication, and managing a TInyDB instance
  - If This Then That (IFTTT)/generic HTML requests to toggle alarm on/off. Allows me to modify the alarm when not home and will automatically disable the alarm if I leave the general vicinity of my home until I return
- Electronics
  - RGB Light Strip
  - Buzzer
  - 7-Segment Display for time
  - Character LCD - shows weather and other quick information
  - (Used to also have a motorized bed shaker, but that got banned, haha)
- Box
  - Pretty janky, but easy to open and work on as a prototype. Will probably try to make something that looks nicer down the road

## Photos

<p align="center">
  <img width="550" height=auto src="./.readme/prototype.jpg" alt="above view">
</p>
<p align="center">Initial Prototype</p>

<p align="center">
  <img width="550" height=auto src="./.readme/TODO: Photo of box" alt="above view">
</p>
<p align="center">Prototype v2 with Box</p>

## Local Development

![Commits Since last Release](https://img.shields.io/github/commits-since/KyleKing/pialarm/latest) ![Last Commit Badge](https://img.shields.io/github/last-commit/kyleking/pialarm)

> FIXME: Update documentation for quick start. This is probably ~32% right

```sh
git clone https://github.com/KyleKing/pialarm.git
cd pialarm
poetry install
poetry shell
python pialarm.py
```

First, check the pins.ini file in the Python/ directory, then proceed the test of each hardware before booting the web application for the first time.

### Initialization

You will need a secret.ini file in the Python/ directory:

```ini
[IFTTT]
key = <>

[WU]
info = Weather Underground API
apikey = <>
lat = <>
lon = <>
```

Python packages and other libraries installed, see the script `./Python/requirements.sh`

There are likely other bugs, so open an issue if you run into any trouble. This app really isn't built for distribution and is only a personal side-project.

### Hardware Test: TM1637 7-Digit Display

```
cd PiAlarm/Python
python .archive-python/modules/TM1637.py
# There should be a few statements printed and you can press enter to confirm each test
```
