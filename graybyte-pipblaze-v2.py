import subprocess
import sys
import datetime
import platform
import time
import os
import ctypes
import shutil
import re


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


def check_pip_availability():
    try:
        if platform.system() == "Windows":
            cmd = ["pip", "--version"]
        else:
            cmd = ["pip3", "--version"]

        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def check_already_installed(package):
    try:
        if platform.system() == "Windows":
            cmd = ["pip", "show", package]
        else:
            cmd = ["pip3", "show", package]

        result = subprocess.check_output(
            cmd,
            stderr=subprocess.DEVNULL,
            text=True
        )

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


def get_install_command(package):
    if platform.system() == "Windows":
        return ["pip", "install", "--no-cache-dir", package]
    else:
        return ["sudo", "pip3", "install", "--no-cache-dir", package, "--break-system-packages"]


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

    if not check_pip_availability():
        print_with_margins("ERROR: PIP IS NOT AVAILABLE", border_char="!")
        return

    print_with_margins(f"READY TO PROCESS {len(packages)} MODULES", border_char="-")
    print("Already installed modules will be silently skipped.")
    print("Failed installations will not stop the process.\n")

    if platform.system() == "Windows":
        print("INSTALL MODE: WINDOWS")
        print("COMMAND MODE: pip install module_name\n")
    else:
        print("INSTALL MODE: LINUX")
        print("COMMAND MODE: sudo pip3 install module_name --break-system-packages\n")

    response = input("PROCEED WITH INSTALLATION? (YES/NO): ").strip().lower()
    print("\n")

    if response not in ["yes", "y"]:
        print_with_margins("INSTALLATION CANCELLED BY USER", border_char="!")
        return

    initialize_log_file()
    log_message("BULK INSTALLATION STARTED")

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
