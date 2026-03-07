import os
import platform
import datetime

# System Information Script
# This is your first project script!

print("=" * 40)
print("HONEYPOT PROJECT - SYSTEM INFO")
print("=" * 40)

# Basic system info
print(f"Username: {os.getlogin()}")
print(f"OS: {platform.system()}")
print(f"OS Version: {platform.version()}")
print(f"Machine: {platform.machine()}")
print(f"Hostname: {platform.node()}")
print(f"Current Directory: {os.getcwd()}")
print(f"Date & Time: {datetime.datetime.now()}")

print("=" * 40)
print("PROJECT FOLDERS:")
print("=" * 40)

# List project folders
for folder in os.listdir(os.getcwd()):
    print(f"  📁 {folder}")

print("=" * 40)
print("System check complete!")