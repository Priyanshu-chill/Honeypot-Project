import subprocess
import os

print("=" * 40)
print("SUBPROCESS PRACTICE")
print("=" * 40)

# 1. RUN a simple command
print("\n1. Running 'whoami' command...")
result = subprocess.run("whoami", capture_output=True, text=True)
print(f"Output: {result.stdout.strip()}")

# 2. RUN command with arguments
print("\n2. Running 'ls -la' command...")
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)

# 3. RUN command and check if it succeeded
print("\n3. Checking if a folder exists...")
result = subprocess.run(["ls", "honeypot"], capture_output=True, text=True)
if result.returncode == 0:
    print("✅ honeypot folder exists!")
else:
    print("❌ folder not found!")

# 4. CREATE a test file and run 'file' command on it
print("\n4. Identifying file type...")
with open("testfile.txt", "w") as f:
    f.write("This is a test file")
result = subprocess.run(["file", "testfile.txt"], capture_output=True, text=True)
print(f"File type: {result.stdout.strip()}")

# 5. RUN strings command (used in malware analysis!)
print("\n5. Extracting strings from file...")
result = subprocess.run(["strings", "testfile.txt"], capture_output=True, text=True)
print(f"Strings found: {result.stdout.strip()}")

# cleanup
os.remove("testfile.txt")
print("\n=" * 40)
print("Subprocess practice complete!")