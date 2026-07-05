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

## 📷 Screenshots

![Main Interface](https://github.com/Platotel3s/service-tui/blob/main/image.png)
![Search & Manage](https://github.com/Platotel3s/service-tui/blob/main/ex2.png)

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

## 🚀 Installation & Setup

Ikuti langkah-langkah berikut untuk memasang dan menjalankan `service-tui` di sistem Linux kamu.

### 1. Clone the Repository

Clone repository ini ke komputer lokal kamu dan masuk ke foldernya:

```bash
git clone git@github.com:Platotel3s/service-tui.git
cd service-tui
```

### 2. Grant Executable Permission

Sebelum membuat tautan global, berikan izin eksekusi (executable permission) ke file script utamanya:

```bash
chmod +x service-tui.py
```

### 3. Create a Global Symlink

Agar tool ini bisa dipanggil langsung dari direktori mana pun tanpa mengetik `python3`, buat symbolic link ke direktori binary lokal sistem kamu:

```bash
sudo ln -s $(pwd)/service-tui.py /usr/local/bin/service-tui
```

### 4. Run the TUI

Sekarang kamu bisa langsung menjalankan aplikasi ini cukup dengan mengetik perintah berikut di terminal:

```bash
service-tui
```

> **Note:** Beberapa aksi seperti Start, Stop, dan Restart service memerlukan hak akses root. Jika prompt meminta password saat menjalankan aksi tersebut, itu adalah hal yang wajar.

---

## ⌨️ Controls

| Key         | Action                    |
|-------------|---------------------------|
| ↑ / ↓       | Move cursor up / down     |
| PgUp / PgDn | Scroll faster              |
| /           | Search services by name   |
| s           | Start selected service    |
| t           | Stop selected service     |
| r           | Restart selected service  |
| q           | Quit application           |

---

## 🐍 Notes for Python Users

Python doesn't require compile steps like Rust or Go. However, if you want to distribute this, you can convert it into a standalone binary using:

### ❗ Option A — Using PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile service-tui.py
```

Your binary will be inside:

```
dist/service-tui
```

Users on any distro can run it without Python installed.

---

## 📦 Packaging for Other Linux Users

If you upload this to GitHub, no extra configuration is needed — except if you want others to install it more easily. You can add optional packages:

* ✅ **RPM** (Fedora, RHEL, CentOS) — use `rpmbuild`
* ✅ **DEB** (Ubuntu, Debian) — use `dpkg-deb`
* ✅ **AppImage** (universal) — works on ALL distros

> If you prefer Rust-style simplicity: Rust has `cargo build --release`, which generates a portable static binary. Python doesn't do that by default — but a PyInstaller binary is the closest equivalent.

---

## 🛠 Development

Run directly for development/testing:

```bash
python3 service-tui.py
```

### Directory Structure

```
service-tui/
├── service-tui.py
├── README.md
├── LICENSE
└── *.png
```

---

## 🤝 Contributing

PRs and improvements are welcome! Especially features like:

* Enabling service masks
* Viewing logs (`journalctl` integration)
* Sorting by active/inactive status
* Mouse support

---

## 📝 License

MIT License — feel free to modify and use.

---

## ⭐ Support

If you find this tool useful, please give this repository a star! ⭐

Thanks for using TUI System Service Manager!
