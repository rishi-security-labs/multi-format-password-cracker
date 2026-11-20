#!/usr/bin/env python3
"""
ZIP Password Cracker - Termux Edition
Supports: ZIP (ZipCrypto + AES), multi-threaded
Feature: Folder browse karke file select karo
"""

import zipfile
import os
import sys
import time
import threading
from queue import Queue

# Color codes
G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
B = '\033[1m'
X = '\033[0m'

# Global flags
found_password = None
stop_flag = threading.Event()
tried_count = 0
lock = threading.Lock()


def banner():
    print(f"""{C}
╔══════════════════════════════════════╗
║      ZIP PASSWORD CRACKER v2.0       ║
║         Termux Edition 🔥            ║
╚══════════════════════════════════════╝
{X}""")


def list_dir(path):
    """Folder ka content list karo - folders pehle, phir files"""
    try:
        items = os.listdir(path)
    except PermissionError:
        print(f"{R}[!] Permission denied: {path}{X}")
        return [], []
    except Exception as e:
        print(f"{R}[!] Error: {e}{X}")
        return [], []

    dirs = sorted([d for d in items if os.path.isdir(os.path.join(path, d))])
    files = sorted([f for f in items if os.path.isfile(os.path.join(path, f))])
    return dirs, files


def browse_file(start_path, file_filter=None, prompt="Select file"):
    """
    Interactive file browser
    file_filter: list of extensions like ['.zip', '.7z'] (optional)
    Returns: selected file ka full path ya None
    """
    current = start_path

    while True:
        print(f"\n{C}📁 Current: {current}{X}")
        dirs, files = list_dir(current)

        if file_filter:
            files = [f for f in files if any(f.lower().endswith(ext) for ext in file_filter)]

        print(f"{Y}{'─' * 50}{X}")

        # Parent option
        print(f"{C}  [0] 📂 .. (Parent folder){X}")

        idx = 1
        dir_options = {}
        file_options = {}

        # Folders
        for d in dirs:
            print(f"{C}  [{idx}] 📁 {d}/{X}")
            dir_options[idx] = d
            idx += 1

        # Files
        for f in files:
            size = os.path.getsize(os.path.join(current, f))
            size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
            print(f"{G}  [{idx}] 📄 {f}  ({size_str}){X}")
            file_options[idx] = f
            idx += 1

        # Manual path option
        print(f"{Y}  [m] ✏️  Manual path enter karo{X}")
        print(f"{Y}  [q] ❌ Cancel{X}")
        print(f"{Y}{'─' * 50}{X}")

        choice = input(f"{C}➤ {prompt}: {X}").strip().lower()

        if choice == 'q':
            return None
        elif choice == 'm':
            manual = input(f"{C}➤ Full path: {X}").strip()
            if os.path.isfile(manual):
                return manual
            elif os.path.isdir(manual):
                current = manual
            else:
                print(f"{R}[!] Path not found{X}")
        elif choice == '0':
            current = os.path.dirname(current) or '/'
        elif choice.isdigit():
            num = int(choice)
            if num in dir_options:
                current = os.path.join(current, dir_options[num])
            elif num in file_options:
                return os.path.join(current, file_options[num])
            else:
                print(f"{R}[!] Invalid choice{X}")
        else:
            print(f"{R}[!] Invalid input{X}")


def smart_resolve(path, file_filter=None):
    """
    Path ko resolve karo:
    - Agar full path hai aur exists => return
    - Agar sirf filename hai => common locations check karo
    """
    if os.path.exists(path):
        return path

    common_dirs = [
        '/sdcard/Download',
        '/sdcard',
        '/storage/emulated/0/Download',
        '/storage/emulated/0',
        os.path.expanduser('~'),
        os.getcwd(),
    ]

    for d in common_dirs:
        candidate = os.path.join(d, path)
        if os.path.exists(candidate):
            return candidate

    return None


def get_file_from_user(label, default_dir, file_filter=None):
    """
    User se file lene ka master function:
    1. Direct path try karo
    2. Agar na mile toh browse mode open karo
    """
    user_input = input(f"{C}📂 {label} (path ya Enter = browse): {X}").strip()

    if user_input:
        resolved = smart_resolve(user_input, file_filter)
        if resolved and os.path.isfile(resolved):
            return resolved
        elif resolved and os.path.isdir(resolved):
            # Folder diya toh browse karo usme
            return browse_file(resolved, file_filter, prompt="File select karo")
        else:
            print(f"{Y}[!] '{user_input}' nahi mila, browser khol rahe hain...{X}")
            return browse_file(default_dir, file_filter, prompt="File select karo")

    # Empty input = browse
    return browse_file(default_dir, file_filter, prompt="File select karo")


def is_encrypted(zip_path):
    """Check karo ZIP encrypted hai ya nahi"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for info in zf.infolist():
                if info.flag_bits & 0x1:
                    return True
        return False
    except Exception as e:
        print(f"{R}[!] ZIP open error: {e}{X}")
        return False


def try_password(zip_path, password):
    """Ek password try karo"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            for info in zf.infolist():
                if info.flag_bits & 0x1:
                    try:
                        zf.read(info.filename, pwd=password.encode('utf-8'))
                        return True
                    except (RuntimeError, zipfile.BadZipFile, NotImplementedError):
                        return False
            return True
    except Exception:
        return False


def worker(zip_path, queue, total):
    """Worker thread"""
    global tried_count, found_password

    while not stop_flag.is_set():
        try:
            password = queue.get(timeout=1)
        except:
            return

        if password is None:
            return

        password = password.rstrip('\r\n')

        with lock:
            tried_count += 1
            current = tried_count

        if try_password(zip_path, password):
            found_password = password
            stop_flag.set()
            print(f"\n\n{G}{B}[✓] PASSWORD FOUND: {password}{X}")
            return

        if current % 200 == 0:
            print(f"{Y}[*] Tried: {current}/{total}{X}", end='\r')

        queue.task_done()


def crack(zip_path, wordlist_path, threads=4):
    global tried_count, found_password
    tried_count = 0
    found_password = None
    stop_flag.clear()

    if not is_encrypted(zip_path):
        print(f"{Y}[!] ZIP encrypted nahi hai - direct extract kar sakte ho{X}")
        return None

    print(f"{C}[*] Loading wordlist...{X}")
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{R}[!] Wordlist read error: {e}{X}")
        return None

    total = len(passwords)
    print(f"{C}[*] Total passwords: {total}{X}")
    print(f"{C}[*] Threads: {threads}{X}")
    print(f"{C}[*] Starting crack...{X}\n")

    queue = Queue()
    for pwd in passwords:
        queue.put(pwd)

    start = time.time()

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(zip_path, queue, total))
        t.daemon = True
        t.start()
        thread_list.append(t)

    try:
        while not stop_flag.is_set():
            if queue.empty() and all(not t.is_alive() for t in thread_list):
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted by user{X}")
        stop_flag.set()

    elapsed = time.time() - start
    speed = tried_count / elapsed if elapsed > 0 else 0

    print(f"\n\n{C}[*] Elapsed: {elapsed:.2f}s | Speed: {speed:.0f}/sec{X}")

    return found_password


def main():
    banner()

    # Default start folder
    default_dir = '/sdcard/Download'
    if not os.path.isdir(default_dir):
        default_dir = os.path.expanduser('~')

    # ---- ZIP file select ----
    print(f"\n{B}═══ STEP 1: ZIP file select karo ═══{X}")
    zip_path = get_file_from_user(
        "ZIP file path",
        default_dir,
        file_filter=['.zip']
    )
    if not zip_path:
        print(f"{R}[!] Koi file select nahi ki. Exiting.{X}")
        return
    print(f"{G}[✓] ZIP: {zip_path}{X}")

    # ---- Wordlist select ----
    print(f"\n{B}═══ STEP 2: Wordlist select karo ═══{X}")
    wl_path = get_file_from_user(
        "Wordlist path",
        default_dir,
        file_filter=['.txt', '.lst', '.wordlist']
    )
    if not wl_path:
        print(f"{R}[!] Koi wordlist select nahi ki. Exiting.{X}")
        return
    print(f"{G}[✓] Wordlist: {wl_path}{X}")

    # ---- Threads ----
    try:
        threads_input = input(f"\n{C}⚙️  Threads (default 4): {X}").strip()
        threads = int(threads_input) if threads_input else 4
        if threads < 1 or threads > 32:
            threads = 4
    except:
        threads = 4

    # ---- Start crack ----
    print(f"\n{B}═══ STEP 3: Cracking ═══{X}")
    result = crack(zip_path, wl_path, threads)

    if result:
        print(f"\n{G}{B}═══════════════════════════════════════{X}")
        print(f"{G}{B}   ✓ PASSWORD: {result}{X}")
        print(f"{G}{B}═══════════════════════════════════════{X}\n")
    else:
        print(f"\n{R}[✗] Password not found in wordlist{X}")
        print(f"{Y}[!] Try a bigger/different wordlist{X}\n")


if __name__ == "__main__":
    main()
