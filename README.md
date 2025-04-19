# GRAYBYTE-PipBlaze


**GRAYBYTE PipBlaze is a Python script that automates the installation of a predefined list of Python packages using pip. It provides detailed system information, logs installation results, and features a visually appealing console output with centered ASCII art and consistent spacing. Designed for system administrators and developers, this script is cross-platform, supporting both Linux (e.g., Garuda Linux) and Windows environments.**


## 🔥Features

Automated Package Installation: Installs a curated list of Python packages with a single command.
Cross-Platform Compatibility: Works on Linux and Windows, with specific fixes for Windows console Unicode issues.
Formatted Output: Displays centered ASCII art, section headers with borders, and two blank lines after each print for readability.
System Information: Shows OS, release, version, machine type, and Python version details.
Logging: Records installation success/failure with timestamps in a log file (pip_install_external_log.txt).
Error Handling: Checks for Python 3 and pip availability, with clear error messages.
Customizable Package List: Easily modify the packages list to include desired modules.



## 🔥Supported Packages
The script installs the following Python packages (editable in the packages list):

aiofiles
aiohttp
beautifulsoup4
colorama
crayons
matplotlib
paramiko
prettytable
psutil
pyshark
PyQt6
requests
rich
scapy
sqlmap
tabulate
telethon
textual
tqdm
urllib3

## Requirements

Python: Version 3.7 or higher (due to sys.stdout.reconfigure usage).
pip: Must be installed and accessible in the Python environment.
Operating System: Linux (e.g., Ubuntu, Garuda Linux) or Windows (10/11 recommended).
Terminal: On Windows, Windows Terminal is recommended for optimal Unicode support, though Command Prompt and PowerShell are supported.
Permissions: Some packages (e.g., PyQt6, sqlmap) may require administrative privileges or additional dependencies.

## Installation

Clone the Repository:
git clone https://github.com/Graybyt3/graybyte-pipblaze.git
cd graybyte-pipblaze


Ensure Python and pip: Verify Python 3 and pip are installed:
python3 --version
python3 -m pip --version

If not installed, download Python from python.org and follow pip installation instructions.

Run the Script: Execute the script using Python 3:
python3 module_installer.py



## Usage

Start the Script: Run the script in a terminal:
python3 module_installer.py


Review System Information: The script displays your OS, release, version, machine type, and Python version.

Confirm Installation: When prompted with WOULD YOU LIKE TO PROCEED? (YES/NO):, type yes to install all packages or no to exit.

Monitor Progress: The script installs each package, showing STARTING INSTALLATION, INSTALLING, and COMPLETED or SKIPPED messages, with two blank lines after each for clarity.

Check Results:

A summary shows the total modules processed, successful installations, failed installations, and time taken.
Detailed logs are saved to pip_install_external_log.txt.



Example Output
=================================================================
=             GRAYBYTE PYTHON AUTO-MODULE INSTALLER             =
=================================================================


----------------------------------------
-            SYSTEM INFORMATION            -
----------------------------------------
  OS: Windows
  RELEASE: 10
  VERSION: 10.0.19041
  MACHINE: AMD64
  WINDOWS EDITION: Pro
  PYTHON VERSION: 3.10.6


----------------------------------------
- READY TO INSTALL ALL YOUR SPECIFIED PYTHON MODULES -
----------------------------------------
WOULD YOU LIKE TO PROCEED? (YES/NO): yes

yes


STARTING INSTALLATION FOR aiofiles


INSTALLING aiofiles NOW, PLEASE WAIT


COMPLETED INSTALLATION OF aiofiles


[2025-04-18 18:30:00] aiofiles - Success


[... other packages ...]

==============================================
=            INSTALLATION SUMMARY            =
==============================================
  TOTAL MODULES PROCESSED: 20
  SUCCESSFULLY INSTALLED: 20
  FAILED INSTALLATIONS: 0
  TOTAL TIME TAKEN: 10.25 SECONDS
CHECK 'pip_install_external_log.txt' FOR DETAILED LOGS. GOODBYE



## Customization

Add/Remove Packages: Edit the packages list in module_installer.py to include or exclude modules.
packages = ["numpy", "pandas", ...]


Modify Output: Adjust the print_with_margins function (e.g., change width = min(width, 80) to width = min(width, 120)) for wider/narrower output.


Troubleshooting

Unicode Issues on Windows: If the logo appears broken, use Windows Terminal or ensure your console font (e.g., Consolas) supports Unicode. The script uses a plain ASCII logo (GRAYBYTE PYTHON AUTO-MODULE INSTALLER) on Windows to avoid issues.

Package Installation Errors: Some packages may require additional dependencies (e.g., PyQt6 needs Qt libraries). Check the log file (pip_install_external_log.txt) for error details and install dependencies manually if needed.

Permission Errors: Run the script with elevated privileges if required:
sudo python3 module_installer.py  # Linux

Or open Command Prompt as Administrator on Windows.


# 👨🏻‍💻 FOR MORE INFORMATION AND SUPPORT 👨🏻‍💻

[TELEGRAM](https://t.me/rex_cc) | 
[FACEBOOK](https://www.facebook.com/graybyt3) | 
[X](https://x.com/gray_byte) | 
[INSTAGRAM](https://www.instagram.com/gray_byte)
