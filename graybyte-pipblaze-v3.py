import subprocess
import sys
import datetime
import platform
import time
import os
import ctypes
import shutil
import re
import urllib.request
import tempfile


# Graybyt3 - Ex-Blackhat 🖤 | Ex Super Mod of Team_CC.
# Now securing systems as a Senior Security Expert 🛡️.
# I hack servers for fun, patch them to torture you.
#
# "My life is a lie, and i'm living in this only truth.- Graybyt3"
#
# WARNING: Steal my code, and I'll call you Pappu
# There's no worse shame in this world than being called Pappu.
# FuCk_Pappu


LOGO = "GRAYBYTE PYTHON AUTO-MODULE INSTALLER"

packages = [
    "aiofiles",
    "aiohttp",
    "beautifulsoup4",
    "colorama",
    "matplotlib",
    "numpy",
    "prettytable",
    "psutil",
    "PyQt6",
    "requests",
    "rich",
    "tabulate",
    "telethon",
    "textual",
    "tqdm",
    "urllib3",
    "cryptography",
    "netifaces",
    "dnspython",
    "lxml",
    "pyinstaller",
]

log_file = "pip_install_external_log.txt"

# Global flags set during detection
USE_BREAK_SYSTEM_PACKAGES = False
PIP_CMD = None          # ["pip"] or ["pip3"] or full path
INSTALL_BASE_CMD = None # full base command list used for every package


def configure_windows_console():
    if platform.system() == "Windows":
        try:
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            mode.value |= 0x0004
            kernel32.SetConsoleMode(handle, mode)
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass


def print_with_margins(text, border_char="=", width=None, top_bottom_border=True):
    if width is None:
        try:
            width = shutil.get_terminal_size(fallback=(80, 24)).columns
        except Exception:
            width = 80

    width = min(width, 100)
    text_lines = str(text).split("\n")
    max_line_length = max(len(line) for line in text_lines)
    padding = max((width - max_line_length - 4) // 2, 2)

    if top_bottom_border:
        print("\n" + border_char * width)

    for line in text_lines:
        print(f"{border_char} {' ' * padding}{line.center(max_line_length)}{' ' * padding} {border_char}")

    if top_bottom_border:
        print(border_char * width + "\n")
    else:
        print("\n")


def initialize_log_file():
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n\n" + ("=" * 80) + "\n")
        f.write(LOGO + "\n")
        f.write("INSTALLATION STARTED: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 80 + "\n\n")


def log_message(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {text}"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    print(entry)


def run_cmd(cmd, capture=False, check=False):
    """Helper to run a command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=check
            )
            return result.returncode, result.stdout
        else:
            result = subprocess.run(cmd, check=check)
            return result.returncode, None
    except Exception as e:
        return 1, str(e)


def check_pip_availability():
    """Return True if pip/pip3 is usable."""
    global PIP_CMD
    candidates = []
    if platform.system() == "Windows":
        candidates = [["pip"], ["python", "-m", "pip"], ["py", "-m", "pip"]]
    else:
        candidates = [["pip3"], ["pip"], ["python3", "-m", "pip"], ["python", "-m", "pip"]]

    for cmd in candidates:
        code, _ = run_cmd(cmd + ["--version"], capture=True)
        if code == 0:
            PIP_CMD = cmd
            return True
    return False


def install_pip():
    """Install pip if missing. Returns True on success."""
    log_message("PIP NOT FOUND – ATTEMPTING TO INSTALL PIP")

    if platform.system() == "Windows":
        # Try ensurepip first
        code, out = run_cmd([sys.executable, "-m", "ensurepip", "--upgrade"], capture=True)
        if code == 0:
            log_message("PIP INSTALLED VIA ensurepip")
            return True

        # Fallback: get-pip.py
        try:
            log_message("DOWNLOADING get-pip.py ...")
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
                urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", tmp.name)
                code, _ = run_cmd([sys.executable, tmp.name], capture=True)
                os.unlink(tmp.name)
                if code == 0:
                    log_message("PIP INSTALLED VIA get-pip.py")
                    return True
        except Exception as e:
            log_message(f"get-pip.py FAILED: {e}")
        return False

    # Linux / Unix
    # 1. Try package manager (Arch / Garuda / Debian / Ubuntu / Fedora)
    pkg_managers = [
        (["sudo", "pacman", "-S", "--noconfirm", "python-pip"], "pacman"),
        (["sudo", "apt-get", "update"], None),  # update first
        (["sudo", "apt-get", "install", "-y", "python3-pip"], "apt"),
        (["sudo", "dnf", "install", "-y", "python3-pip"], "dnf"),
        (["sudo", "yum", "install", "-y", "python3-pip"], "yum"),
    ]

    for cmd, name in pkg_managers:
        if name is None:
            run_cmd(cmd)  # just update
            continue
        log_message(f"TRYING PACKAGE MANAGER: {name}")
        code, _ = run_cmd(cmd, capture=True)
        if code == 0:
            log_message(f"PIP INSTALLED VIA {name}")
            return True

    # 2. Fallback get-pip.py
    try:
        log_message("DOWNLOADING get-pip.py ...")
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", tmp.name)
            code, _ = run_cmd(["sudo", sys.executable, tmp.name], capture=True)
            os.unlink(tmp.name)
            if code == 0:
                log_message("PIP INSTALLED VIA get-pip.py")
                return True
    except Exception as e:
        log_message(f"get-pip.py FAILED: {e}")

    return False


def detect_break_system_packages():
    """
    Detect whether the system requires --break-system-packages.
    Returns True if the flag is needed.
    """
    if platform.system() == "Windows":
        return False

    # Method 1: Look for EXTERNALLY-MANAGED marker (PEP 668)
    python_paths = [
        f"/usr/lib/python{sys.version_info.major}.{sys.version_info.minor}/EXTERNALLY-MANAGED",
        f"/usr/lib/python{sys.version_info.major}/EXTERNALLY-MANAGED",
        "/usr/lib/python3/EXTERNALLY-MANAGED",
    ]
    for path in python_paths:
        if os.path.isfile(path):
            log_message(f"EXTERNALLY-MANAGED MARKER FOUND: {path}")
            return True

    # Method 2: Dry-run a harmless install and check error message
    test_cmd = PIP_CMD + ["install", "--dry-run", "requests"]
    code, output = run_cmd(test_cmd, capture=True)
    if code != 0 and output:
        if "externally-managed-environment" in output.lower() or "break-system-packages" in output.lower():
            log_message("PIP REPORTS EXTERNALLY-MANAGED ENVIRONMENT – --break-system-packages REQUIRED")
            return True

    # Method 3: Common on Arch / Garuda / newer Debian-based
    if platform.system() == "Linux":
        # Quick check for Arch-based
        if os.path.exists("/etc/arch-release") or os.path.exists("/etc/garuda-release"):
            log_message("ARCH / GARUDA DETECTED – ENABLING --break-system-packages")
            return True

    log_message("NO EXTERNALLY-MANAGED RESTRICTION DETECTED")
    return False


def build_install_base_command():
    """Build the base install command once after detection."""
    global INSTALL_BASE_CMD, USE_BREAK_SYSTEM_PACKAGES

    if platform.system() == "Windows":
        INSTALL_BASE_CMD = PIP_CMD + ["install", "--no-cache-dir"]
        USE_BREAK_SYSTEM_PACKAGES = False
        return

    # Linux
    USE_BREAK_SYSTEM_PACKAGES = detect_break_system_packages()

    if USE_BREAK_SYSTEM_PACKAGES:
        INSTALL_BASE_CMD = ["sudo"] + PIP_CMD + ["install", "--no-cache-dir", "--break-system-packages"]
    else:
        INSTALL_BASE_CMD = ["sudo"] + PIP_CMD + ["install", "--no-cache-dir"]

    log_message(f"INSTALL COMMAND PATTERN: {' '.join(INSTALL_BASE_CMD)} <package>")


def get_install_command(package):
    return INSTALL_BASE_CMD + [package]


def check_already_installed(package):
    try:
        cmd = PIP_CMD + ["show", package]
        result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        version_line = [line for line in result.splitlines() if line.startswith("Version:")][0]
        version = version_line.split(":", 1)[1].strip()
        return True, version
    except Exception:
        return False, None


def sudo_auth_once():
    if platform.system() == "Windows":
        return True

    print_with_margins("LINUX SUDO AUTHENTICATION", border_char="-")
    print("SUDO PASSWORD WILL BE REQUESTED ONCE BEFORE INSTALLATION STARTS.\n")

    try:
        result = subprocess.run(["sudo", "-v"])
        if result.returncode == 0:
            log_message("SUDO AUTHENTICATION SUCCESSFUL")
            return True
        else:
            log_message("SUDO AUTHENTICATION FAILED")
            return False
    except Exception as e:
        log_message(f"SUDO AUTHENTICATION ERROR: {e}")
        return False


def install_package(package):
    print("\n" + "-" * 80)
    log_message(f"PROCESSING PACKAGE: {package}")

    print(f"CHECKING IF {package} IS ALREADY INSTALLED...")
    installed, version = check_already_installed(package)

    if installed:
        print(f"{package} IS ALREADY INSTALLED (version {version})")
        log_message(f"{package} - SKIPPED (ALREADY INSTALLED, VERSION {version})")
        print(f"Skipping {package}\n")
        return True, 0.0

    print(f"{package} IS NOT FOUND LOCALLY. PROCEEDING WITH INSTALLATION...")
    log_message(f"{package} - STARTING INSTALLATION")

    install_cmd = get_install_command(package)
    print(f"Command: {' '.join(install_cmd)}\n")

    start_time = time.perf_counter()

    process = subprocess.Popen(
        install_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    speed_pattern = re.compile(r"(\d+(?:\.\d+)?)\s*(KB|MB|GB)/s")
    current_speed = "0 KB/s"

    for line in process.stdout:
        line = line.rstrip()
        print(line)

        speed_match = speed_pattern.search(line)
        if speed_match:
            current_speed = speed_match.group(1) + " " + speed_match.group(2) + "/s"

    process.wait()
    elapsed = time.perf_counter() - start_time

    if process.returncode == 0:
        print(f"\nINSTALLATION OF {package} COMPLETED SUCCESSFULLY")
        log_message(f"{package} - SUCCESS | Time: {elapsed:.2f}s | Peak speed: {current_speed}")
        print(f"Time taken: {elapsed:.2f} seconds | Peak download speed: {current_speed}\n")
        return True, elapsed
    else:
        print(f"\nINSTALLATION OF {package} FAILED (exit code: {process.returncode})")
        log_message(f"{package} - FAILED | Time: {elapsed:.2f}s | Exit code: {process.returncode}")
        print("CONTINUING WITH NEXT PACKAGE...\n")
        return False, elapsed


def main():
    configure_windows_console()

    print("\n")
    print_with_margins(LOGO)

    print_with_margins("SYSTEM INFORMATION", border_char="-", top_bottom_border=True)
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  MACHINE: {platform.machine()}")

    if platform.system() == "Windows":
        try:
            edition = platform.win32_edition()
            print(f"  WINDOWS EDITION: {edition}")
        except AttributeError:
            pass

    print(f"  PYTHON VERSION: {platform.python_version()}\n")

    if sys.version_info.major != 3:
        print_with_margins("ERROR: THIS SCRIPT REQUIRES PYTHON 3", border_char="!")
        return

    # === STEP 1: Check / Install pip ===
    print_with_margins("PIP AVAILABILITY CHECK", border_char="-")
    if not check_pip_availability():
        print("PIP NOT FOUND. ATTEMPTING TO INSTALL PIP...\n")
        if not install_pip():
            print_with_margins("FATAL: COULD NOT INSTALL PIP", border_char="!")
            return
        # Re-check after install
        if not check_pip_availability():
            print_with_margins("FATAL: PIP STILL NOT AVAILABLE AFTER INSTALL ATTEMPT", border_char="!")
            return
        print("PIP SUCCESSFULLY INSTALLED AND VERIFIED.\n")
    else:
        print(f"PIP IS AVAILABLE → {' '.join(PIP_CMD)}\n")
        log_message(f"PIP DETECTED: {' '.join(PIP_CMD)}")

    # === STEP 2: Detect OS install pattern ===
    print_with_margins("DETECTING INSTALL COMMAND PATTERN", border_char="-")
    build_install_base_command()

    if platform.system() == "Windows":
        print("INSTALL MODE: WINDOWS")
        print(f"COMMAND PATTERN: {' '.join(INSTALL_BASE_CMD)} <package>\n")
    else:
        print("INSTALL MODE: LINUX")
        if USE_BREAK_SYSTEM_PACKAGES:
            print("DETECTED: --break-system-packages REQUIRED (PEP 668 / Arch / Garuda style)")
        else:
            print("DETECTED: Standard pip install (no --break-system-packages)")
        print(f"COMMAND PATTERN: {' '.join(INSTALL_BASE_CMD)} <package>\n")

    print_with_margins(f"READY TO PROCESS {len(packages)} MODULES", border_char="-")
    print("Already installed modules will be silently skipped.")
    print("Failed installations will not stop the process.\n")

    response = input("PROCEED WITH INSTALLATION? (YES/NO): ").strip().lower()
    print("\n")

    if response not in ["yes", "y"]:
        print_with_margins("INSTALLATION CANCELLED BY USER", border_char="!")
        return

    initialize_log_file()
    log_message("BULK INSTALLATION STARTED")
    log_message(f"USING PATTERN: {' '.join(INSTALL_BASE_CMD)} <package>")

    if not sudo_auth_once():
        print_with_margins("SUDO AUTHENTICATION FAILED", border_char="!")
        return

    success_count = 0
    skipped_count = 0
    fail_count = 0
    total_start = time.perf_counter()
    module_times = []

    for package in packages:
        success, elapsed = install_package(package)

        if success and elapsed > 0:
            success_count += 1
        elif success and elapsed == 0:
            skipped_count += 1
        else:
            fail_count += 1

        if elapsed > 0:
            module_times.append(elapsed)

    total_time = time.perf_counter() - total_start

    log_message(f"BULK INSTALLATION COMPLETED | Total time: {total_time:.2f}s")

    print_with_margins("INSTALLATION SUMMARY", border_char="=")
    print(f"  TOTAL PACKAGES PROCESSED:    {len(packages)}")
    print(f"  NEWLY INSTALLED:             {success_count}")
    print(f"  ALREADY INSTALLED SKIPPED:   {skipped_count}")
    print(f"  FAILED:                      {fail_count}")
    print(f"  TOTAL TIME ELAPSED:          {total_time:.2f} seconds")

    if module_times:
        avg_time = sum(module_times) / len(module_times)
        print(f"  AVERAGE INSTALL TIME:        {avg_time:.2f} SECONDS EXCLUDING SKIPPED\n")

    print(f"DETAILED LOG SAVED TO: {log_file}\n")


if __name__ == "__main__":
    main()
