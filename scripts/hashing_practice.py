import hashlib
import os

print("=" * 40)
print("HASHING PRACTICE - SHA256")
print("=" * 40)

# 1. HASH a simple string
print("\n1. Hashing a string...")
text = "malware.elf"
hash_result = hashlib.sha256(text.encode()).hexdigest()
print(f"Text: {text}")
print(f"SHA256: {hash_result}")

# 2. HASH a file (like a real malware sample)
print("\n2. Hashing a file...")

# Create a fake malware file
with open("fake_malware.elf", "w") as f:
    f.write("This simulates malware content")

# Generate SHA256 hash of the file
sha256 = hashlib.sha256()
with open("fake_malware.elf", "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha256.update(chunk)

file_hash = sha256.hexdigest()
print(f"Filename: fake_malware.elf")
print(f"SHA256: {file_hash}")

# 3. SHOW why hashing matters
print("\n3. Same file = same hash always...")
sha256_check = hashlib.sha256()
with open("fake_malware.elf", "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha256_check.update(chunk)

print(f"Hash again: {sha256_check.hexdigest()}")
print(f"Hashes match: {file_hash == sha256_check.hexdigest()}")

# 4. DIFFERENT content = completely different hash
print("\n4. Different content = different hash...")
hash1 = hashlib.sha256("malware_v1".encode()).hexdigest()
hash2 = hashlib.sha256("malware_v2".encode()).hexdigest()
print(f"malware_v1: {hash1}")
print(f"malware_v2: {hash2}")
print(f"Hashes match: {hash1 == hash2}")

# cleanup
os.remove("fake_malware.elf")
print("\n=" * 40)
print("Hashing practice complete!")