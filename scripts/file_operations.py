import os
import datetime

print("=" * 40)
print("FILE OPERATIONS PRACTICE")
print("=" * 40)

# 1. WRITING to a file
print("\n1. Writing to a file...")
with open("test_log.txt", "w") as f:
    f.write("Attack detected from IP: 192.168.1.100\n")
    f.write("Attacker tried username: root\n")
    f.write("Attacker tried password: admin123\n")
    f.write(f"Timestamp: {datetime.datetime.now()}\n")
print("File written successfully!")

# 2. READING from a file
print("\n2. Reading the file...")
with open("test_log.txt", "r") as f:
    content = f.read()
print(content)

# 3. READING line by line
print("3. Reading line by line...")
with open("test_log.txt", "r") as f:
    for line in f:
        print(f"  Line: {line.strip()}")

# 4. APPENDING to a file
print("\n4. Appending new attack...")
with open("test_log.txt", "a") as f:
    f.write("Attacker uploaded file: malware.elf\n")

# 5. READ again to confirm append worked
print("\n5. File after appending:")
with open("test_log.txt", "r") as f:
    print(f.read())

# 6. DELETE the test file
os.remove("test_log.txt")
print("6. Test file cleaned up!")
print("=" * 40)