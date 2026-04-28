# Windows Configuration Detector

This project reads local Windows configuration data and writes it down plainly.
It does not call external services. It reads the registry, shows results in a GUI, and exports reports.

## Project Requirement

Note 1: Make sure to include tutorial (readme) file with guidelines on how to compile and run your source code.

## What Each Component Does

- `src/app.py`
  Builds the desktop interface.
  It runs scans, displays OS and software results, and triggers export.

- `src/os_detector.py`
  Reads Windows product name, build number, and architecture from the registry.
  It also corrects the common case where Windows 11 is labeled as Windows 10 in registry text.

- `src/software_scanner.py`
  Scans uninstall registry paths for installed software entries.
  It extracts name, version, publisher, and install date, then formats dates as `YYYY-MM-DD` when possible.

- `src/csv_exporter.py`
  Writes report output files.
  It exports both:
  - `output/osinfo.csv`
  - `output/osinfo.txt` (same CSV-style content, `.txt` extension)

## Runtime Requirements

- Windows 11 (intended target)
- Python 3.11+ recommended
- No third-party runtime libraries are required for scanning/export logic

## How to Run from Source

1. Open a terminal in the project root.
2. (Optional but recommended) create and activate a virtual environment.
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python src/app.py
   ```

## How to Build an EXE

1. Install build requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Build:
   ```bash
   pyinstaller --onefile --windowed --name WindowsConfigDetector src/app.py
   ```
3. Find the executable at:
   - `dist/WindowsConfigDetector.exe`

## Output Files

After scanning and export:
- `output/osinfo.csv`
- `output/osinfo.txt`
