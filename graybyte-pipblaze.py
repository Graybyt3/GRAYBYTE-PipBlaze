import subprocess
import sys
import datetime
import platform
import time
import os
import ctypes
import shutil

LOGO = """𝗚𝗥𝗔𝗬𝗕𝗬𝗧𝗘 𝗣𝗬𝗧𝗛𝗢𝗡 𝗔𝗨𝗧𝗢-𝗠𝗢𝗗𝗨𝗟𝗘 𝗜𝗡𝗦𝗧𝗔𝗟𝗟𝗘𝗥"""
LOGO_WIN = """GRAYBYTE PYTHON AUTO-MODULE INSTALLER"""

# you can add aro module names eikahne
packages = [
    "aiofiles",
    "aiohttp",
    "beautifulsoup4",
    "colorama",
    "crayons",
    "matplotlib",
    "paramiko",
    "prettytable",
    "psutil",
    "pyshark",
    "PyQt6",
    "requests",
    "rich",
    "scapy",
    "sqlmap",
    "tabulate",
    "telethon",
    "textual",
    "tqdm",
    "urllib3"
]

log_file = "pip_install_external_log.txt"

def configure_windows_console():
    """Configure Windows console for UTF-8 and Unicode support."""
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
        except Exception as e:
            print(f"Warning: Could not configure console for UTF-8: {e}\n\n")

def print_with_margins(text, border_char='=', width=None, top_bottom_border=True):
    """Print text with centered alignment, margins, and optional borders."""
    if width is None:
        width = shutil.get_terminal_size().columns
    width = min(width, 80)  
    text_lines = text.split('\n')
    max_line_length = max(len(line) for line in text_lines)
    padding = (width - max_line_length - 4) // 2  
    if padding < 2:
        padding = 2

    if top_bottom_border:
        print('\n' + border_char * width)
    for line in text_lines:
        print(f"{border_char} {' ' * padding}{line.center(max_line_length)}{' ' * padding} {border_char}")
    if top_bottom_border:
        print(border_char * width + '\n\n')
    else:
        print('\n\n')

def initialize_log_file():
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n\n\n" + LOGO + "\n\n\n")

def log_message(module, status, error_message=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {module} - {status}"
    if error_message:
        log_entry += f" - {error_message}"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
    print(log_entry + '\n\n')

def check_pip_availability():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        return True
    except subprocess.CalledProcessError:
        return False

def install_package(package, success_count, fail_count):
    print(f"STARTING INSTALLATION FOR {package}\n\n")
    print(f"INSTALLING {package} NOW, PLEASE WAIT\n\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        log_message(package, "Success")
        print(f"COMPLETED INSTALLATION OF {package}\n\n")
        return success_count + 1, fail_count
    except subprocess.CalledProcessError as e:
        log_message(package, "Fail", f"Installation error: {e}")
        print(f"SKIPPED {package} DUE TO INSTALLATION ERROR\n\n")
        return success_count, fail_count + 1
    except Exception as e:
        log_message(package, "Fail", f"Unexpected error: {e}")
        print(f"SKIPPED {package} DUE TO UNEXPECTED ERROR\n\n")
        return success_count, fail_count + 1

def main():
    
    configure_windows_console()
    
    
    display_logo = LOGO_WIN if platform.system() == "Windows" else LOGO
    
    
    print('\n\n')  
    print_with_margins(display_logo)
    
    
    print_with_margins("SYSTEM INFORMATION", border_char='-', top_bottom_border=True)
    print(f"  OS: {platform.system()}")
    print(f"  RELEASE: {platform.release()}")
    print(f"  VERSION: {platform.version()}")
    print(f"  MACHINE: {platform.machine()}")
    if platform.system() == "Windows":
        try:
            print(f"  WINDOWS EDITION: {platform.win32_edition()}")
        except AttributeError:
            print("  WINDOWS EDITION: NOT AVAILABLE")
    print(f"  PYTHON VERSION: {sys.version.split()[0]}\n\n")

    # python ache na nai?
    if sys.version_info.major != 3:
        print_with_margins("ERROR: THIS SCRIPT REQUIRES PYTHON 3", border_char='!')
        print("PLEASE INSTALL PYTHON 3 AND TRY AGAIN. VISIT:  https://www.python.org/downloads/ FOR DETAILS\n\n")
        return

    if not check_pip_availability():
        print_with_margins("ERROR: PIP IS NOT INSTALLED OR NOT ACCESSIBLE", border_char='!')
        print("PLEASE INSTALL PIP TO PROCEED. VISIT: https://pip.pypa.io/en/stable/installation FOR DETAILS\n\n")
        return

    print_with_margins("READY TO INSTALL ALL YOUR SPECIFIED PYTHON MODULES", border_char='-')
    response = input("WOULD YOU LIKE TO PROCEED? (YES/NO): ").strip().lower() + '\n\n'
    print(response)
    if response.strip() != "yes":
        print_with_margins("OPERATION CANCELLED. EXITING NOW", border_char='!')
        return

    initialize_log_file()
    log_message("Bulk installation", "Started")

    success_count = 0
    fail_count = 0
    start_time = time.perf_counter()

    for package in packages:
        success_count, fail_count = install_package(package, success_count, fail_count)

    total_time = time.perf_counter() - start_time

    log_message("Bulk installation", "Completed")

    print('\n')
    print_with_margins("INSTALLATION SUMMARY", border_char='=', top_bottom_border=True)
    print(f"  TOTAL MODULES PROCESSED: {len(packages)}")
    print(f"  SUCCESSFULLY INSTALLED: {success_count}")
    print(f"  FAILED INSTALLATIONS: {fail_count}")
    print(f"  TOTAL TIME TAKEN: {total_time:.2f} SECONDS")
    print("CHECK 'pip_install_external_log.txt' FOR DETAILED LOGS. GOODBYE\n\n")

if __name__ == "__main__":
    main()
