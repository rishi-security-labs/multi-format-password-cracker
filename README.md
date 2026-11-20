# 🔐 Multi-Format Password Cracker — Termux Edition

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Windows-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Use](https://img.shields.io/badge/Use-Authorized%20Security%20Research%20Only-red?style=for-the-badge)

A fast, multi-threaded **archive password recovery tool** built for Termux and Linux. It supports dictionary attacks against **ZIP, RAR, TAR.GZ, TAR.BZ2, and TAR.XZ** archives with an interactive file browser, automatic format detection via magic bytes, and configurable thread counts.

> ⚠️ **Disclaimer:** This tool is intended for **authorized security research, CTF challenges, and recovering your own encrypted files**. Do not use it against files you do not own or have explicit permission to test. The author assumes no liability for misuse.

---

## 📖 Overview

**Multi-Format Password Cracker** is a command-line utility designed for security researchers and CTF players. Instead of juggling separate scripts for ZIP and RAR files, this toolkit unifies archive recovery under a single interactive menu. It auto-detects archive format using **magic-byte signatures** (not just extensions), verifies encryption status before attacking, and uses a multi-threaded wordlist engine to maximize throughput.

Two scripts are included:
- **`multi_cracker.py`** — the flagship multi-format cracker.
- **`zip_cracker.py`** — a lightweight, ZIP-only cracker (fallback / minimal-dependency version).

---

## ✨ Key Features

### 🧩 Core Engine
- **Multi-format support:** ZIP, RAR, TAR.GZ, TGZ, TAR.BZ2, TAR.XZ, TAR.
- **Magic-byte format detection** — reliable even if extensions are wrong or stripped.
- **Multi-threaded password engine** (1–32 threads, default 4).
- **Encryption pre-check** — warns you if the archive isn't encrypted before wasting time.
- **Live progress counter** and speed (passwords/second) reporting.

### 🗂️ User Experience
- **Interactive file browser** — navigate folders with numbered menus, no need to type full paths.
- **Smart path resolution** — auto-searches `/sdcard/Download`, `/sdcard`, `~/`, and current dir.
- **File size + format labels** displayed in the browser for quick identification.
- **Clean colored UI** with banners, status indicators, and error messages.
- **Graceful interrupt handling** (Ctrl+C stops all threads cleanly).

### ⚙️ Platform
- **Termux-optimized** (default path `/sdcard/Download`).
- Works on **Linux** and **Windows** (auto-clears screen appropriately).
- **No mandatory third-party deps** for ZIP/TAR — RAR needs `rarfile` + `unrar`.

---

## 📁 Project Folder Structure

```
multi-format-password-cracker/
│
├── multi_cracker.py        # Main multi-format cracker (ZIP/RAR/TAR.*)
├── zip_cracker.py          # Standalone ZIP-only cracker
├── requirements.txt        # Optional dependencies (rarfile)
├── README.md               # This file
├── LICENSE                 # MIT License
└── .gitignore              # Ignore caches, wordlists, test archives
```

---

## 🚀 Installation & Usage

### 🔹 Termux (Android)

```bash
# 1. Update packages
pkg update && pkg upgrade -y

# 2. Install Python
pkg install python -y

# 3. (Optional) Install unrar for RAR support
pkg install unrar -y

# 4. Install Python dependencies
pip install rarfile

# 5. Grant storage permission (needed for /sdcard access)
termux-setup-storage

# 6. Clone the repo
git clone https://github.com/rishi-security-labs/multi-format-password-cracker.git
cd multi-format-password-cracker

# 7. Run
python multi_cracker.py
```

### 🔹 Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip unrar -y
pip3 install rarfile

git clone https://github.com/rishi-security-labs/multi-format-password-cracker.git
cd multi-format-password-cracker
python3 multi_cracker.py
```

### 🔹 Windows

```powershell
# Install Python 3.8+ from python.org, then:
pip install rarfile
# Install UnRAR: https://www.rarlab.com/rar_add.htm (add to PATH)

git clone https://github.com/rishi-security-labs/multi-format-password-cracker.git
cd multi-format-password-cracker
python multi_cracker.py
```

---

## 🎮 How to Use

1. Run the script: `python multi_cracker.py`
2. Choose **[1] Start Cracking** from the main menu.
3. **Select the encrypted archive** — type a path or press Enter to open the interactive browser.
4. **Select the wordlist** (`rockyou.txt`, custom `.txt` / `.lst` / `.wordlist`).
5. Set **thread count** (default `4`, max `32`).
6. Wait for the result. Found passwords are printed in a green banner:

```
═══════════════════════════════════════
   ✓ PASSWORD: mysecret123
═══════════════════════════════════════
```

### Example Wordlists

| Wordlist | Source |
|----------|--------|
| `rockyou.txt` | [SecLists](https://github.com/danielmiessler/SecLists) |
| `10-million-password-list` | [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Passwords) |

> 💡 **Tip:** On Termux, save your wordlist to `/sdcard/Download/` so the browser finds it instantly.

---

## ⚙️ Configuration & Dependencies

### Environment Variables
None required — the tool is fully self-contained and config-driven through the interactive menu.

### Default Paths
| Setting | Default |
|---------|---------|
| Start folder (Termux) | `/sdcard/Download` |
| Fallback start folder | `~` (home directory) |
| Default thread count | `4` |
| Max thread count | `32` |

### Dependencies

| Package | Required? | Purpose |
|---------|-----------|---------|
| `zipfile` | ✅ Built-in | ZIP cracking |
| `tarfile` | ✅ Built-in | TAR.* detection |
| `rarfile` | ⚠️ Optional | RAR cracking |
| `unrar` | ⚠️ Optional | RAR backend for `rarfile` |

Install RAR dependencies:
```bash
pkg install unrar        # Termux
sudo apt install unrar   # Linux
pip install rarfile
```

### Supported Formats & Encryption

| Format | Encryption Support |
|--------|-------------------|
| ZIP | ✅ ZipCrypto + AES |
| RAR | ✅ RAR5 / RAR4 (needs `unrar`) |
| TAR.GZ / TAR.BZ2 / TAR.XZ | ❌ TAR has no native encryption (tool warns) |

---

## 🧠 How It Works

1. **Format detection** — reads the first 8 bytes of the file and matches magic signatures (`PK\x03\x04`, `Rar!`, `\x1f\x8b`, etc.).
2. **Encryption check** — inspects archive headers (ZIP `flag_bits & 0x1`, RAR `needs_password()`).
3. **Wordlist loading** — reads all non-empty lines into memory.
4. **Worker pool** — spawns `N` daemon threads pulling from a `Queue`.
5. **Early exit** — on first successful password, a global `stop_flag` is set and all threads terminate.

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 rishi-security-labs

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

## 🙏 Credits

- Built for the **Termux** community and CTF players.
- Wordlist ecosystem by [SecLists](https://github.com/danielmiessler/SecLists).
- RAR backend by [rarfile](https://github.com/markokr/rarfile).

---

<div align="center">

**⭐ If this tool helped you, star the repo! ⭐**

Made with 🖤 by [rishi-security-labs](https://github.com/rishi-security-labs)

</div>
