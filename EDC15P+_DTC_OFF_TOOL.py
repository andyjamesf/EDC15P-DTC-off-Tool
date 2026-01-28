import struct
import os
import sys
import datetime

PATCH = {
    -3: 65535,
    -2: 0
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ask(msg):
    return input(msg).strip()

def error(msg):
    print(f"\n[ERROR] {msg}")
    sys.exit(1)

def log(msg):
    print(msg)
    with open(LOGFILE, "a") as f:
        f.write(msg + "\n")

print("\n" + "=" * 40)
print("     EDC15P+ DTC OFF TOOL (Terminal)")
print("=" * 40 + "\n")

# ---------- STEP 1: LIST BIN FILES ----------
bin_files = [f for f in os.listdir(BASE_DIR) if f.lower().endswith(".bin")]

if not bin_files:
    error("No .bin files found in the tool directory")

print("BIN files found:\n")
for i, f in enumerate(bin_files, start=1):
    print(f"{i}) {f}")

choice = ask("\nSelect BIN file number:\n> ")

if not choice.isdigit() or not (1 <= int(choice) <= len(bin_files)):
    error("Invalid selection")

bin_name = bin_files[int(choice) - 1]
BIN_IN = os.path.join(BASE_DIR, bin_name)

# ---------- STEP 2: DTCs ----------
dtc_input = ask("\nEnter DTCs (5 digits, comma-separated):\n> ")

dtc_list = []
for d in dtc_input.split(","):
    d = d.strip()
    if not d.isdigit() or len(d) != 5:
        error(f"Invalid DTC: {d}")
    dtc_list.append(int(d))

# ---------- STEP 3: MODE ----------
print("\nExecution mode:")
print("[1] Execute patch")
print("[2] Dry-run (simulation)")

mode = ask("Select (1/2): ")

if mode == "1":
    DRY_RUN = False
elif mode == "2":
    DRY_RUN = True
else:
    error("Invalid option")

# ---------- OUTPUT ----------
base, ext = os.path.splitext(bin_name)
DEFAULT_OUT = base + "_DTC_OFF.bin"
BIN_OUT = os.path.join(BASE_DIR, DEFAULT_OUT)

if os.path.exists(BIN_OUT) and not DRY_RUN:
    error("Output file already exists")

# ---------- LOG ----------
LOGFILE = os.path.join(BASE_DIR, base + "_DTC_OFF.log")

log("\n" + "=" * 60)
log(f"Execution   : {datetime.datetime.now()}")
log(f"Input BIN   : {bin_name}")
log(f"Output BIN  : {DEFAULT_OUT}")
log(f"DTCs        : {dtc_list}")
log(f"Mode        : {'DRY-RUN' if DRY_RUN else 'EXECUTE'}")

# ---------- SUMMARY ----------
print("\nSummary:")
print(f"- Input BIN : {bin_name}")
print(f"- DTCs      : {dtc_list}")
print(f"- Output    : {DEFAULT_OUT}")
print(f"- Mode      : {'DRY-RUN' if DRY_RUN else 'EXECUTE'}")

confirm = ask("\nConfirm? (y/n): ").lower()
if confirm != "y":
    print("Operation cancelled by user.")
    sys.exit(0)

# ---------- OPEN BIN ----------
with open(BIN_IN, "rb") as f:
    data = bytearray(f.read())

log(f"BIN size: {len(data)} bytes")

# ---------- READ 16-BIT WORDS ----------
words = [
    struct.unpack_from("<H", data, i)[0]
    for i in range(0, len(data) - 1, 2)
]

total_hits = 0

# ---------- APPLY PATCH ----------
for TARGET in dtc_list:
    hits = [i for i, w in enumerate(words) if w == TARGET]
    log(f"[+] DTC {TARGET}: {len(hits)} occurrences")
    total_hits += len(hits)

    for idx in hits:
        log(f"    Patch at word {idx} (offset 0x{idx*2:X})")
        for rel, val in PATCH.items():
            pos = idx + rel
            if 0 <= pos < len(words):
                words[pos] = val

if total_hits == 0:
    log("[-] No occurrences found. BIN not modified.")
    sys.exit(0)

# ---------- CONVERT BACK TO BYTES ----------
patched = bytearray()
for w in words:
    patched += struct.pack("<H", w)

# ---------- WRITE OUTPUT ----------
if DRY_RUN:
    log("[DRY-RUN] No file written")
else:
    with open(BIN_OUT, "wb") as f:
        f.write(patched)
    log(f"[✓] BIN written successfully ({total_hits} patches applied)")

log("=" * 60)

print("\n[✓] Process completed successfully")
