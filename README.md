# 🔎 USB Forensics with Autopsy

An educational and practical toolkit designed to demonstrate how investigators recover deleted files and trace USB connection history on Windows hosts.

While Autopsy (the desktop application) handles the deep disk-image analysis and file carving, this repository contains the automation scripts to **generate test evidence**, **parse host-side registry artifacts** and **auto-generate comprehensive investigation reports**.

---

## 🎯 Why This Project Matters

Every time a USB device is plugged into a system, it leaves a trail of breadcrumbs. This project bridges the gap between device-level file recovery and host-level system artifacts. By working through this lab, you will learn to reconstruct a timeline of user activity and understand exactly what evidence remains after a breach.

---

## 🗂️ Repository Structure

```text
usb-forensics/
├── scripts/
│   ├── generate_usb_testdata.py   # Populates a drive with known test files and deletes a subset
│   ├── parse_usb_history.py       # Extracts USB connection history from SYSTEM hive & SetupAPI logs
│   └── generate_report.py         # Cross-references recovered files and builds MD/DOCX reports
├── web/
│   ├── app.py                     # Streamlit web interface for demoing the workflow
│   └── requirements.txt           # App and script dependencies
├── examples/
│   ├── manifest.json              # Source of truth for generated files
│   ├── recovered_files.csv        # Template for carved files identified in Autopsy
│   ├── timeline.json              # Parsed connection history output
│   └── example_report.md          # Sample generated investigation report (also in .docx)
└── README.md

```

---

## ⚙️ Quickstart

### 1. Run the Web Demo (No Virtual Machine Required)

To explore the core concepts and score a pre-made recovery dataset instantly without setting up a forensic environment:

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit dashboard
cd web
streamlit run app.py

```

---

## 💻 Full DFIR Analysis Workflow

Follow these steps to run a complete, end-to-end USB forensic simulation:

1. **Generate Test Evidence:** Step 1: Populate the Drive.
Run the generation script against a target virtual disk (or a physical USB drive). This creates a known list of files, deletes a randomized subset and saves a `manifest.json` as your "ground truth."

```bash
python scripts/generate_usb_testdata.py --target E:\ --count 15 --delete-ratio 0.4

```


2. **Acquire and Analyze the Image:** Step 2: Forensic Carving.
1. Image the target drive using **FTK Imager** or `dd`.
2. Load the raw image into **Autopsy** as a data source.
3. Run Ingest Modules (specifically *Extension Mismatch Detector* and *File Recovery/Carving*).
4. Export your findings as `recovered_files.csv` using the schema layout found in `examples/recovered_files.csv`.


3. **Extract Host-Side Artifacts:** Step 3: Registry & Log Parsing.
Collect the critical Windows artifacts from the host machine to prove the USB was connected:

```bash
# Copy host registry and log files
reg save HKLM\SYSTEM C:\temp\SYSTEM
copy C:\Windows\inf\setupapi.dev.log C:\temp\setupapi.dev.log

# Parse connection times, serial numbers, and vendor IDs
python scripts/parse_usb_history.py --system SYSTEM --setupapi setupapi.dev.log --json timeline.json

```


4. **Build the Final Report:** Step 4: Cross-Reference & Score.
Run the reporting engine to compare the files carved in Step 2 against the ground truth from Step 1, append the connection timeline from Step 3, and output a polished report.

```bash
python scripts/generate_report.py --manifest manifest.json --recovered recovered_files.csv --timeline timeline.json --out report.md --docx report.docx

```


---

## 📊 Core Artifacts Analyzed

This project focuses on extracting and cross-referencing three primary types of evidence:

| Artifact Source | Forensics Value | Key Information Extracted |
| --- | --- | --- |
| **FAT32/NTFS Directory Entries** | Device-level | Recovered filenames, deletion timestamps, directory structures. |
| **SYSTEM Registry Hive** | Host-level | USB serial numbers, vendor/product IDs (VID/PID), and drive letter mounts. |
| **SetupAPI Log (`setupapi.dev.log`)** | Host-level | Highly precise timestamps of when the USB drivers were first installed. |

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
