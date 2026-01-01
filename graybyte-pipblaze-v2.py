import subprocess
import sys
import datetime
import platform
import time
import os
import ctypes
import shutil
import re

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
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

def print_with_margins(text, border_char='=', width=None, top_bottom_border=True):
    if width is None:
        try:
            width = shutil.get_terminal_size(fallback=(80, 24)).columns
        except:
            width = 80
    width = min(width, 100)
    text_lines = str(text).split('\n')
    max_line_length = max(len(line) for line in text_lines)
    padding = max((width - max_line_length - 4) // 2, 2)

    if top_bottom_border:
        print('\n' + border_char * width)
    for line in text_lines:
        print(f"{border_char} {' ' * padding}{line.center(max_line_length)}{' ' * padding} {border_char}")
    if top_bottom_border:
        print(border_char * width + '\n')
    else:
        print('\n')

def initialize_log_file():
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n\n" + ("=" * 80) + "\n")
        f.write(LOGO + "\n")
        f.write("Installation started: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("=" * 80 + "\n\n")

def log_message(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {text}"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
    print(entry)

def check_pip_availability():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def check_already_installed(package):
    try:
        result = subprocess.check_output(
            [sys.executable, "-m", "pip", "show", package],
            stderr=subprocess.DEVNULL,
            text=True
        )
        version_line = [line for line in result.splitlines() if line.startswith("Version:")][0]
        version = version_line.split(":", 1)[1].strip()
        return True, version
    except:
        return False, None

def install_package(package):
    print("\n" + "-" * 80)
    log_message(f"Processing package: {package}")

    print(f"Checking if {package} is already installed...")
    installed, version = check_already_installed(package)
    if installed:
        print(f"{package} is already installed (version {version})")
        log_message(f"{package} - SKIPPED (already installed, version {version})")
        print(f"Skipping {package}\n")
        return True, 0.0

    print(f"{package} not found locally. Proceeding with installation...")
    log_message(f"{package} - Starting installation")

    print(f"Command: pip install --no-cache-dir {package}\n")
    
    start_time = time.perf_counter()
    process = subprocess.Popen(
        [sys.executable, "-m", "pip", "install", "--no-cache-dir", package],
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
        print(f"\nInstallation of {package} completed successfully")
        log_message(f"{package} - SUCCESS | Time: {elapsed:.2f}s | Peak speed: {current_speed}")
        print(f"Time taken: {elapsed:.2f} seconds | Peak download speed: {current_speed}\n")
        return True, elapsed
    else:
        print(f"\nInstallation of {package} failed (exit code: {process.returncode})")
        log_message(f"{package} - FAILED | Time: {elapsed:.2f}s | Exit code: {process.returncode}")
        print(f"Continuing with next package...\n")
        return False, elapsed

def main():
    configure_windows_console()

    print('\n')
    print_with_margins(LOGO)

    print_with_margins("SYSTEM INFORMATION", border_char='-', top_bottom_border=True)
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
        print_with_margins("ERROR: THIS SCRIPT REQUIRES PYTHON 3", border_char='!')
        return

    if not check_pip_availability():
        print_with_margins("ERROR: PIP IS NOT AVAILABLE", border_char='!')
        return

    print_with_margins(f"READY TO PROCESS {len(packages)} MODULES", border_char='-')
    print("Already installed modules will be silently skipped.")
    print("Failed installations will not stop the process.\n")
    
    response = input("PROCEED WITH INSTALLATION? (YES/NO): ").strip().lower()
    print("\n")
    if response not in ["yes", "y"]:
        print_with_margins("INSTALLATION CANCELLED BY USER", border_char='!')
        return

    initialize_log_file()
    log_message("Bulk installation STARTED")

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

    log_message(f"Bulk installation COMPLETED | Total time: {total_time:.2f}s")

    print_with_margins("INSTALLATION SUMMARY", border_char='=')
    print(f"  TOTAL PACKAGES PROCESSED:   {len(packages)}")
    print(f"  NEWLY INSTALLED:            {success_count}")
    print(f"  ALREADY INSTALLED (SKIPPED):{skipped_count}")
    print(f"  FAILED:                     {fail_count}")
    print(f"  TOTAL TIME ELAPSED:         {total_time:.2f} seconds")
    if module_times:
        avg_time = sum(module_times) / len(module_times)
        print(f"  AVERAGE INSTALL TIME:       {avg_time:.2f} seconds (excluding skipped)\n")
    print(f"DETAILED LOG SAVED TO: {log_file}\n")

if __name__ == "__main__":
    main()
