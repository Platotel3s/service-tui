Markdown# TUI System Service Manager

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
🚀 Installation & SetupIkuti langkah-langkah berikut untuk memasang dan menjalankan service-tui di sistem Linux kamu.1. Clone the RepositoryClone repository ini ke komputer lokal kamu dan masuk ke foldernya:Bashgit clone git@github.com:Platotel3s/service-tui.git
cd service-tui
2. Grant Executable PermissionSebelum membuat tautan global, berikan izin eksekusi (executable permission) ke file script utamanya:Bashchmod +x service-tui.py
3. Create a Global SymlinkAgar tool ini bisa dipanggil langsung dari direktori mana pun tanpa mengetik python3, buat symbolic link ke direktori binary lokal sistem Anda:Bashsudo ln -s $(pwd)/service-tui.py /usr/local/bin/service-tui
4. Run the TUISekarang kamu bisa langsung menjalankan aplikasi ini cukup dengan mengetik perintah berikut di terminal:Bashservice-tui
Note: Beberapa aksi seperti Start, Stop, dan Restart service memerlukan hak akses root. Jika prompt meminta password saat menjalankan aksi tersebut, itu adalah hal yang wajar.⌨️ ControlsKeyAction↑ / ↓Move cursor up / downPgUp / PgDnScroll faster/Search services by namesStart selected servicetStop selected servicerRestart selected serviceqQuit application🐍 Notes for Python UsersPython doesn’t require compile steps like Rust or Go.However, if you want to distribute this, you can convert it into a standalone binary using:  ❗ Option A — Using PyInstallerBashpip install pyinstaller
pyinstaller --onefile service-tui.py
Your binary will be inside:  dist/service-tui
Users on any distro can run it without Python.📦 Packaging for Other Linux UsersIf you upload this to GitHub, no extra configuration is needed except if you want others to install it easily.  You can add optional packages:  ✅ RPM (Fedora, RHEL, CentOS)Use rpmbuild.  ✅ DEB (Ubuntu, Debian)Use dpkg-deb.  ✅ AppImage (universal)Works on ALL distros.  If you prefer Rust-style simplicityRust has cargo build --release which generates a portable static binary.Python doesn't do that by default — but PyInstaller binary is closest equivalent.  🛠 DevelopmentRun with auto-reload (developer mode)Bashpython3 service-tui.py
Directory structureservice-tui/
├── service-tui.py
├── README.md
├── LICENSE
└── *.png
🤝 ContributingPRs and improvements are welcome!Especially features like:Enabling service masksViewing logs (journalctl integration)Sorting by active/inactive statusMouse support📝 LicenseMIT License — feel free to modify and use.⭐ SupportIf you find this tool useful, please give this repository a star! ⭐Thanks for using TUI System Service Manager!
