#!/usr/bin/env python3
"""
Multi-Format Password Cracker - Termux Edition
Supports: ZIP, RAR, TAR.GZ, TAR.BZ2, TAR.XZ
Feature: Folder browse + auto format detection + Menu
"""

import os
import sys
import time
import threading
from queue import Queue

# ============ OPTIONAL LIBRARIES ============
HAS_ZIP = HAS_RAR = HAS_TAR = True
try:
    import zipfile
except ImportError:
    HAS_ZIP = False
try:
    import rarfile
except ImportError:
    HAS_RAR = False
try:
    import tarfile
except ImportError:
    HAS_TAR = False

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

# Supported formats
SUPPORTED_EXTS = ['.zip', '.rar', '.tar.gz', '.tgz', '.tar.bz2', '.tar.xz', '.tar']


def banner():
    print(f"""{C}
╔══════════════════════════════════════╗
║   MULTI-FORMAT PASSWORD CRACKER      ║
║         Termux Edition 🔥            ║
║      ZIP | RAR | TAR.GZ | TAR.XZ     ║
╚══════════════════════════════════════╝
{X}""")


def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')


# ============ FORMAT DETECTION ============
def detect_format(filepath):
    """Magic bytes + extension se format detect karo"""
    try:
        with open(filepath, 'rb') as f:
            head = f.read(8)
    except Exception:
        return None

    if head[:4] in [b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08']:
        return 'zip'
    if head[:4] == b'Rar!\x1a\x07' or head[:7] == b'Rar!\x1a\x07\x01\x00':
        return 'rar'
    if head[:2] == b'\x1f\x8b':
        return 'tar.gz'
    if head[:3] == b'BZh':
        return 'tar.bz2'
    if head[:6] == b'\xfd7zXZ\x00':
        return 'tar.xz'
    lower = filepath.lower()
    for ext in SUPPORTED_EXTS:
        if lower.endswith(ext):
            return ext.lstrip('.')
    return None


def get_format_label(fmt):
    labels = {
        'zip': 'ZIP', 'rar': 'RAR',
        'tar.gz': 'TAR.GZ', 'tar.bz2': 'TAR.BZ2',
        'tar.xz': 'TAR.XZ', 'tar': 'TAR'
    }
    return labels.get(fmt, fmt.upper())


# ============ ENCRYPTION CHECK ============
def is_encrypted(filepath, fmt):
    try:
        if fmt == 'zip' and HAS_ZIP:
            with zipfile.ZipFile(filepath, 'r') as zf:
                for info in zf.infolist():
                    if info.flag_bits & 0x1:
                        return True
            return False
        elif fmt == 'rar' and HAS_RAR:
            with rarfile.RarFile(filepath) as rf:
                return rf.needs_password()
        elif fmt in ('tar.gz', 'tar.bz2', 'tar.xz', 'tar') and HAS_TAR:
            print(f"{Y}[!] TAR files aam taur pe encrypted nahi hoti{X}")
            return False
        return False
    except Exception as e:
        print(f"{R}[!] Encryption check error: {e}{X}")
        return False


# ============ PASSWORD TESTERS ============
def try_zip(filepath, password):
    try:
        with zipfile.ZipFile(filepath, 'r') as zf:
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


def try_rar(filepath, password):
    try:
        with rarfile.RarFile(filepath) as rf:
            rf.setpassword(password)
            for info in rf.infolist():
                try:
                    rf.read(info.filename)
                    return True
                except (rarfile.RarWrongPassword, rarfile.RarCRCError):
                    return False
                except Exception:
                    continue
            return True
    except Exception:
        return False


def try_password(filepath, fmt, password):
    if fmt == 'zip':
        return try_zip(filepath, password)
    elif fmt == 'rar':
        return try_rar(filepath, password)
    return False


# ============ FILE BROWSER ============
def list_dir(path):
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


def matches_filter(filename, file_filter):
    if not file_filter:
        return True
    lower = filename.lower()
    return any(lower.endswith(ext) for ext in file_filter)


def browse_file(start_path, file_filter=None, prompt="Select file"):
    current = start_path

    while True:
        print(f"\n{C}📁 Current: {current}{X}")
        dirs, files = list_dir(current)
        files = [f for f in files if matches_filter(f, file_filter)]

        print(f"{Y}{'─' * 55}{X}")
        print(f"{C}  [0] 📂 .. (Parent folder){X}")

        idx = 1
        dir_options = {}
        file_options = {}

        for d in dirs:
            print(f"{C}  [{idx}] 📁 {d}/{X}")
            dir_options[idx] = d
            idx += 1

        for f in files:
            full = os.path.join(current, f)
            try:
                size = os.path.getsize(full)
                size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
            except:
                size_str = "?"
            fmt = detect_format(full)
            tag = f" [{get_format_label(fmt)}]" if fmt else ""
            print(f"{G}  [{idx}] 📄 {f}{tag}  ({size_str}){X}")
            file_options[idx] = f
            idx += 1

        print(f"{Y}  [m] ✏️  Manual path{X}")
        print(f"{Y}  [q] ❌ Cancel{X}")
        print(f"{Y}{'─' * 55}{X}")

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
                print(f"{R}[!] Not found{X}")
        elif choice == '0':
            current = os.path.dirname(current) or '/'
        elif choice.isdigit():
            num = int(choice)
            if num in dir_options:
                current = os.path.join(current, dir_options[num])
            elif num in file_options:
                return os.path.join(current, file_options[num])
            else:
                print(f"{R}[!] Invalid{X}")
        else:
            print(f"{R}[!] Invalid{X}")


def smart_resolve(path):
    if os.path.exists(path):
        return path
    common = ['/sdcard/Download', '/sdcard', '/storage/emulated/0/Download',
              '/storage/emulated/0', os.path.expanduser('~'), os.getcwd()]
    for d in common:
        c = os.path.join(d, path)
        if os.path.exists(c):
            return c
    return None


def get_file_from_user(label, default_dir, file_filter=None):
    user_input = input(f"{C}📂 {label} (path ya Enter = browse): {X}").strip()

    if user_input:
        resolved = smart_resolve(user_input)
        if resolved and os.path.isfile(resolved):
            return resolved
        elif resolved and os.path.isdir(resolved):
            return browse_file(resolved, file_filter, prompt="Select")
        else:
            print(f"{Y}[!] '{user_input}' nahi mila, browser khol rahe hain...{X}")
            return browse_file(default_dir, file_filter, prompt="Select")

    return browse_file(default_dir, file_filter, prompt="Select")


# ============ WORKER ============
def worker(filepath, fmt, queue, total):
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

        if try_password(filepath, fmt, password):
            found_password = password
            stop_flag.set()
            print(f"\n\n{G}{B}[✓] PASSWORD FOUND: {password}{X}")
            return

        if current % 100 == 0:
            print(f"{Y}[*] Tried: {current}/{total}{X}", end='\r')

        queue.task_done()


# ============ CRACK DRIVER ============
def crack(filepath, wordlist_path, threads=4):
    global tried_count, found_password
    tried_count = 0
    found_password = None
    stop_flag.clear()

    fmt = detect_format(filepath)
    if not fmt:
        print(f"{R}[!] Format detect nahi hua{X}")
        return None

    print(f"{C}[*] Format detected: {get_format_label(fmt)}{X}")

    if fmt == 'zip' and not HAS_ZIP:
        print(f"{R}[!] zipfile module missing{X}"); return None
    if fmt == 'rar' and not HAS_RAR:
        print(f"{R}[!] rarfile missing. Run: pip install rarfile{X}")
        print(f"{Y}    Also install: pkg install unrar{X}")
        return None

    if not is_encrypted(filepath, fmt):
        print(f"{Y}[!] File encrypted nahi hai ya encryption detect nahi hui{X}")
        print(f"{Y}    Phir bhi try kar rahe hain...{X}")

    print(f"{C}[*] Loading wordlist...{X}")
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{R}[!] Wordlist error: {e}{X}")
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
        t = threading.Thread(target=worker, args=(filepath, fmt, queue, total))
        t.daemon = True
        t.start()
        thread_list.append(t)

    try:
        while not stop_flag.is_set():
            if queue.empty() and all(not t.is_alive() for t in thread_list):
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted{X}")
        stop_flag.set()

    elapsed = time.time() - start
    speed = tried_count / elapsed if elapsed > 0 else 0

    print(f"\n\n{C}[*] Elapsed: {elapsed:.2f}s | Speed: {speed:.0f}/sec{X}")
    return found_password


# ============ LIBRARY CHECK ============
def check_libraries():
    print(f"{C}[*] Library Status:{X}")
    print(f"    {'✓' if HAS_ZIP else '✗'} zipfile  (built-in)")
    print(f"    {'✓' if HAS_RAR else '✗'} rarfile  {'(installed)' if HAS_RAR else '(pip install rarfile)'}")
    print(f"    {'✓' if HAS_TAR else '✗'} tarfile  (built-in)")
    print()


# ============ START CRACKING FLOW ============
def start_cracking():
    default_dir = '/sdcard/Download'
    if not os.path.isdir(default_dir):
        default_dir = os.path.expanduser('~')

    # ---- Encrypted file select ----
    print(f"\n{B}═══ STEP 1: Encrypted file select karo ═══{X}")
    print(f"{Y}Supported: {', '.join(SUPPORTED_EXTS)}{X}")
    target = get_file_from_user("File path", default_dir, file_filter=SUPPORTED_EXTS)
    if not target:
        print(f"{R}[!] Koi file select nahi ki{X}")
        return
    print(f"{G}[✓] File: {target}{X}")

    fmt = detect_format(target)
    if fmt:
        print(f"{G}[✓] Format: {get_format_label(fmt)}{X}")
    else:
        print(f"{R}[!] Format detect nahi hua - crack skip{X}")
        return

    # ---- Wordlist select ----
    print(f"\n{B}═══ STEP 2: Wordlist select karo ═══{X}")
    wl = get_file_from_user("Wordlist path", default_dir,
                            file_filter=['.txt', '.lst', '.wordlist'])
    if not wl:
        print(f"{R}[!] Wordlist select nahi ki{X}")
        return
    print(f"{G}[✓] Wordlist: {wl}{X}")

    # ---- Threads ----
    try:
        ti = input(f"\n{C}⚙️  Threads (default 4): {X}").strip()
        threads = int(ti) if ti else 4
        threads = max(1, min(32, threads))
    except:
        threads = 4

    # ---- Crack ----
    print(f"\n{B}═══ STEP 3: Cracking ═══{X}")
    result = crack(target, wl, threads)

    if result:
        print(f"\n{G}{B}═══════════════════════════════════════{X}")
        print(f"{G}{B}   ✓ PASSWORD: {result}{X}")
        print(f"{G}{B}═══════════════════════════════════════{X}\n")
    else:
        print(f"\n{R}[✗] Password not found{X}")
        print(f"{Y}[!] Bigger wordlist try karo{X}\n")

    input(f"{C}Enter dabao main menu pe wapas jaane ke liye...{X}")


# ============ MAIN MENU ============
def main():
    while True:
        clear_screen()
        banner()
        check_libraries()

        print(f"{B}═══════════ MAIN MENU ═══════════{X}")
        print(f"{G}  [1]{X} 🚀 Start Cracking")
        print(f"{R}  [0]{X} ❌ Exit")
        print(f"{B}═════════════════════════════════{X}")

        choice = input(f"\n{C}➤ Choice: {X}").strip()

        if choice == '1':
            clear_screen()
            banner()
            start_cracking()
        elif choice == '0':
            print(f"\n{G}[✓] Bye bhai! Phir milenge 👋{X}\n")
            sys.exit(0)
        else:
            print(f"{R}[!] Invalid choice, 1 ya 0 daalo{X}")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Y}[!] Exiting...{X}\n")
        sys.exit(0)
