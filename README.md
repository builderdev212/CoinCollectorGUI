# CoinCollectorGUI
**A simple gui designed to interact with a database. The goal of the database
is to make keeping track of collected coins simple.**

The GUI consists of 5 tabs:
- Login
- Overview
- View All
- Add/Remove Coin
- Search Coins

You can view examples of these tabs in the gui_examples folder.

Please make sure you are running python 3.8 or below, as mysql doesn't
work on python 3.9. Make sure you have installed mariadb and created an
account to access the database. Also, make sure mysql.connector and
tkinter are installed.

## Setting up a virtual environment
```bash
python3 -m venv .venv --prompt ccgui-venv
source .venv/bin/activate
pip3 install -r requierments.txt
```
