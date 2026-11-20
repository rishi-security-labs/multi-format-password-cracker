<h1 align="center">🔓 Multi-Format Password Cracker</h1>

<p align="center">
  <b>A powerful, multi-threaded dictionary attack tool for recovering passwords from ZIP, RAR, and TAR archives — built for Termux, Linux & Windows.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Windows-2ea44f?style=for-the-badge&logo=linux&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/Threading-Multi--Threaded-orange?style=for-the-badge" alt="Multi-threaded">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" alt="Status">
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-license">License</a>
</p>

---

## 📖 Overview

**Multi-Format Password Cracker** is a lightweight, high-performance CLI toolkit designed to recover lost or forgotten passwords from password-protected archives. It performs **dictionary-based attacks** using multi-threaded workers to maximize speed while supporting multiple archive formats in a single, unified interface.

The toolkit includes a **built-in Indian Password Generator** that intelligently produces highly realistic wordlists based on common Indian naming conventions, birth years, cities, pet names, and patterns — dramatically increasing recovery success rates for real-world archives.

Originally built for **Termux on Android**, it also works seamlessly on **Linux** and **Windows**.

> ⚠️ **Disclaimer:** This tool is intended **strictly for educational purposes and authorized security research** on archives you own or have explicit permission to test. Unauthorized access to protected files is illegal. The author assumes no liability for misuse.

---

## ✨ Key Features

### 🔓 Multi-Format Cracking Engine
- **ZIP** (ZipCrypto + AES)
- **RAR** (via `unrar` backend)
- **TAR.GZ**, **TAR.BZ2**, **TAR.XZ**, **TAR**
- **Magic-byte detection** — auto-detects archive type even if extension is misleading
- Multi-threaded dictionary attack (1–32 threads, configurable)
- Real-time progress reporting (tried count, elapsed time, speed/sec)

### 📁 Smart File Browser
- Interactive directory navigation (folders + files with sizes)
- Automatic format labeling per file
- **Smart path resolution** — type just a filename and it searches common Termux/Android paths (`/sdcard/Download`, `~/`, etc.)
- Manual path entry + parent folder navigation

### 🇮🇳 Indian Password Generator
- **20+ real-world password patterns** including:
  - `name + year`, `name + lastname + 123`
  - `name + city`, `name + 786`, `name + @ + year`
  - `petname + number`, `city + birth_year`, `name + 2024`
- Curated lists: 60+ first names, 30+ surnames, 20+ Indian cities, birth years 1970–2009
- Duplicate-free output using set generation
- Saves to `/sdcard/Download/password.txt` on Termux

### 🛠️ Developer-Friendly
- Zero-config — pick file, pick wordlist, done
- Color-coded terminal UI (green = success, red = error, yellow = warning)
- Graceful Ctrl+C handling
- Detailed library status check on startup (shows which modules are available)

---

## 📁 Project Folder Structure

```
multi-format-password-cracker/
│
├── multi_cracker.py         # Main entry — supports ZIP, RAR, TAR.GZ, TAR.XZ, TAR.BZ2
├── zip_cracker.py           # Dedicated ZIP cracker (legacy / lightweight)
├── password_generator.py    # Indian password wordlist generator (20+ patterns)
│
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
├── .gitignore               # Ignored files
│
└── wordlists/               # (Optional) place custom wordlists here
    └── README.md
```

---

## ⚙️ Installation

### 📱 Termux (Android) — Recommended

```bash
# 1. Update packages
pkg update -y && pkg upgrade -y

# 2. Install Python and storage access
pkg install python -y
termux-setup-storage    # Grant storage permission

# 3. Install RAR support (optional, only if cracking .rar)
pkg install unrar -y

# 4. Clone the repo
git clone https://github.com/rishi-security-labs/multi-format-password-cracker.git
cd multi-format-password-cracker

# 5. Install Python dependencies
pip install -r requirements.txt
```

### 🐧 Linux

```bash
sudo apt update
sudo apt install python3 python3-pip unrar -y
git clone https://github.com/rishi-security-labs/multi-format-password-cracker.git
cd multi-format-password-cracker
pip3 install -r requirements.txt
```

### 🪟 Windows

```powershell
# Install Python 3.7+ from python.org
git clone https://github.com/rishi-security-labs/multi-format-password-cracker.git
cd multi-format-password-cracker
pip install -r requirements.txt

# Download unrar.exe from https://www.rarlab.com/rar_add.htm
# and add it to PATH (only needed for RAR archives)
```

---

## 🚀 Usage

### 1️⃣ Generate a Wordlist (Optional — for Indian password patterns)

```bash
python password_generator.py
```

- Enter how many passwords to generate (e.g., `10000`)
- Output saved to `/sdcard/Download/password.txt` (Termux) or current dir
- Use this file as the wordlist in the next step

### 2️⃣ Crack an Archive (Multi-Format — Recommended)

```bash
python multi_cracker.py
```

**Flow:**
1. **STEP 1** — Select encrypted archive (browse or type path)
2. **STEP 2** — Select wordlist file (`.txt` / `.lst` / `.wordlist`)
3. **STEP 3** — Set thread count (default `4`, max `32`)
4. Watch progress → get password or "not found"

### 3️⃣ Crack a ZIP Only (Lightweight)

```bash
python zip_cracker.py
```

Same interactive flow, but ZIP-only. Use if you don't need RAR/TAR support.

### 💡 Example Session

```
➤ Choice: 1

═══ STEP 1: Encrypted file select karo ═══
📂 File path (path ya Enter = browse): secret.zip
[✓] File: /sdcard/Download/secret.zip
[✓] Format: ZIP

═══ STEP 2: Wordlist select karo ═══
📂 Wordlist path (path ya Enter = browse): password.txt
[✓] Wordlist: /sdcard/Download/password.txt

⚙️  Threads (default 4): 8

═══ STEP 3: Cracking ═══
[*] Format detected: ZIP
[*] Loading wordlist...
[*] Total passwords: 10000
[*] Threads: 8
[*] Starting crack...

[✓] PASSWORD FOUND: rahul@1998

[*] Elapsed: 2.13s | Speed: 4694/sec
```

---

## 🔧 Configuration & Environment

This tool requires **no environment variables** or API keys. All configuration is interactive via CLI prompts.

### Runtime Defaults

| Setting | Default | Editable |
|---|---|---|
| Thread count | `4` | Via prompt (1–32) |
| Wordlist filter | `.txt`, `.lst`, `.wordlist` | Edit `file_filter` in code |
| Start directory (Termux) | `/sdcard/Download` | Falls back to `~` |
| Output path (generator) | `/sdcard/Download/password.txt` | Edit in `password_generator.py` |

### Required Python Modules

| Module | Purpose | Install |
|---|---|---|
| `zipfile` | ZIP cracking | Built-in ✅ |
| `tarfile` | TAR cracking | Built-in ✅ |
| `rarfile` | RAR cracking | `pip install rarfile` |
| `unrar` | RAR backend (binary) | `pkg install unrar` (Termux) / `apt install unrar` (Linux) |

### `requirements.txt`

```txt
rarfile>=4.0
```

> ⚠️ RAR cracking additionally requires the **`unrar` binary** to be installed on your system (see Installation).

---

## ⚠️ Limitations & Notes

- **TAR archives do not support built-in encryption** — the tool will detect TAR files but cannot crack them (they're typically compressed, not encrypted).
- **AES-encrypted ZIP** cracking may fail on some Windows-built zips due to `zipfile` limitations — use [7-Zip](https://7-zip.org/) in that case.
- **Speed depends heavily on wordlist quality** and thread count. Use the included `password_generator.py` for realistic Indian password patterns.
- **Always test on archives you created** before relying on it for recovery.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs via [Issues](https://github.com/rishi-security-labs/multi-format-password-cracker/issues)
- Submit PRs for new formats (e.g., 7z, PDF, Office docs)
- Improve wordlist patterns in `password_generator.py`

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Rishi Security Labs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  Made with 🖤 by <a href="https://github.com/rishi-security-labs">Rishi Security Labs</a> · Termux Edition 🔥
</p>

<p align="center">
  ⭐ If this project helped you, consider giving it a star!
</p>
