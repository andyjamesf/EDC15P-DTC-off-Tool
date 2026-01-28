# DTC OFF Tool for EDC15P+ (Terminal)

Interactive Python tool to automatically apply **DTC OFF patches** to ECU **BIN files**, automating the repetitive manual workflow commonly performed in WinOLS.

Designed for **bench work and technical analysis**, this tool provides a safe, repeatable, and user-friendly way to apply known diagnostic patches directly from the terminal.

---

## Features

- Interactive step-by-step terminal assistant
- Automatic detection and listing of `.bin` files in the tool directory
- Support for multiple DTCs in a single run
- Relative offset patching (WinOLS-style workflow)
- Automatic creation of a new BIN file (original is never overwritten)
- Dry-run mode (simulation only, no file written)
- Detailed log file generated for every execution
- No external Python dependencies

---

## Requirements

- Python 3.10 or newer  
- Linux / macOS (Windows should work but is not officially tested)

Check Python version:
```bash
python --version
```

---

## Installation

```bash
git clone https://github.com/andyjamesf/EDC15P-DTC-off-Tool.git
cd EDC15P-DTC-off-Tool
```
No additional Python packages are required.

---

## How to Use

1. Place your ECU `.bin` file in the **same directory** as `dtc_off.py`
2. Run the tool:
```bash
python dtc_off.py
```
3. Follow the interactive steps:
   - Select the BIN file from the numbered list
   - Enter one or more DTCs (5 digits, comma-separated)
   - Choose execution mode (execute or dry-run)
   - Confirm before patching

---

## Example Session

```text
========================================
    EDC15P+ DTC OFF TOOL (Terminal)
========================================

BIN files found:

1) orig.bin
2) golf_edc16.bin

Select BIN file number:
> 2

Enter DTCs (5 digits, comma separated):
> 17978,17896

Execution mode:
[1] Execute patch
[2] Dry-run (simulation)

Confirm? (y/n):
> y
```

Output files:
- `golf_edc16_DTC_OFF.bin`
- `golf_edc16_DTC_OFF.log`

---

## Logs

A log file is automatically created for each execution:

```
<original_name>_DTC_OFF.log
```

The log contains:
- execution date and time
- selected BIN file
- processed DTCs
- patch offsets (word and byte)
- execution mode
- number of applied patches

---

## IMPORTANT: Checksum Notice

This tool directly modifies ECU BIN files.

After any modification, **checksum recalculation or correction is mandatory**.

Checksums are required to:
- ensure file integrity
- prevent ECU boot failures
- avoid flashing errors or corrupted memory

Always recalculate or fix the checksum using an appropriate tool or method  
**before flashing the ECU**.

This project does not bypass or remove checksum requirements.

---

## Safety Notes

- The original BIN file is never overwritten
- No output file is written if no DTC patterns are found
- Dry-run mode allows safe testing without modifying files
- User confirmation is required before execution

---

## Disclaimer

This software is provided **for educational and technical purposes only**.

The author assumes no responsibility for improper use, ECU damage,
or legal or regulatory issues resulting from the use of this tool.

---

## Roadmap

- Automatic checksum plugins per ECU type
- Batch processing of multiple BIN files
- TUI with keyboard navigation
- ECU profile system (EDC16 / EDC17 / MED / Delphi)

Contributions, issues, and suggestions are welcome.
