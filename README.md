
# TUI System Service Manager

A simple **Terminal User Interface (TUI)** tool to help you **start, stop, restart, search, and manage systemd services** without needing to type long commands or remember service names.

This tool works on **any Linux distribution** that uses **systemd**, such as:

* Fedora
* Ubuntu
* Debian
* Arch Linux / Manjaro
* openSUSE
* Pop!_OS
* Linux Mint
* EndeavourOS

> Built using **Python + curses** to keep it simple and lightweight.

---

## ✨ Features

* View all systemd services
* Scroll up & down smoothly
* Start / Stop / Restart services
* Real-time service status indicator
* Search services by name
* Auto-refresh list
* Keyboard-friendly navigation

---

## 📦 Requirements

This app requires:

* Python **3.8+**
* systemd (default on most modern Linux distros)
* A terminal supporting ncurses

You can check your Python version with:

```bash
python3 --version
```

---

## 🚀 Install & Run (ANY Linux Distro)

### **1. Clone the repository**

```bash
git clone https://github.com/USERNAME/tui-system-service.git
cd tui-system-service
```

Replace `USERNAME` with your GitHub username.

### **2. (Optional) Create virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Run the app**

```bash
python3 service-tui.py
```

That's it.

---

## ⌨️ Controls

| Key         | Action                   |
| ----------- | ------------------------ |
| ↑ / ↓       | Move cursor              |
| PgUp / PgDn | Scroll faster            |
| `/`         | Search services          |
| `s`         | Start selected service   |
| `t`         | Stop selected service    |
| `r`         | Restart selected service |
| `q`         | Quit                     |

---

## 🔧 Optional: Make it runnable globally

If you want to run the TUI from anywhere:

### 1. Create symlink

```bash
sudo ln -s $(pwd)/service-tui.py /usr/local/bin/service-tui
```

### 2. Run it:

```bash
service-tui
```

---

## 🐍 Notes for Python Users

Python doesn’t require compile steps like Rust or Go.
However, if you want to distribute this, you can convert it into a **standalone binary** using:

### ❗ Option A — Using PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile service-tui.py
```

Your binary will be inside:

```
dist/service-tui
```

Users on any distro can run it without Python.

---

## 📦 Packaging for Other Linux Users

If you upload this to GitHub, no extra configuration is needed *except* if you want others to install it easily.

You can add optional packages:

### ✅ RPM (Fedora, RHEL, CentOS)

Use `rpmbuild`.

### ✅ DEB (Ubuntu, Debian)

Use `dpkg-deb`.

### ✅ AppImage (universal)

Works on ALL distros.

### If you prefer Rust-style simplicity

Rust has `cargo build --release` which generates a portable static binary.
Python doesn't do that by default — **but PyInstaller binary is closest equivalent**.

---

## 🛠 Development

### Run with auto-reload (developer mode)

```bash
python3 service-tui.py
```

### Directory structure

```
tui-system-service/
├── service-tui.py
├── README.md
└── LICENSE
```

---

## 🤝 Contributing

PRs and improvements are welcome!
Especially features like:

* Enabling service masks
* Viewing logs (journalctl integration)
* Sorting by active/inactive
* Mouse support

---

## 📝 License

MIT License — feel free to modify and use.

---

## ⭐ Support

If you find this useful, give the repo a star!

Thanks for using TUI System Service Manager!
# service tui

## 📷 Documentation  

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/e2dfb980-8a30-44f3-aa69-3900c0dbddb4" />
![alt text](https://github.com/Platotel3s/service-tui/blob/main/ex2.png) 
