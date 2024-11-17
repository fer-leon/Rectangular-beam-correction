# Laser Cutter Rectangular Beam Correction

Most blue laser engravers have a rectangular beam geometry, making the cut more effective in one direction than the other. This program modifies an existing GCODE file to correct the cutting speed on the less powerful axis, ensuring more consistent results without requiring repeated passes.

---


## Features

- Adjusts the feed rate of GCODE files based on the selected axis.
- Provides a graphical user interface (GUI) for selecting the axis and opening/saving files.

---

## Requirements

- **Python 3.x**
- **tkinter library** (usually included with Python)
- **re library** (usually included with Python)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/fer-leon/Rectangular-beam-correction.git
```


Ensure you have Python 3.x installed.

## Usage

1. Run the script:

   ```bash
   python Rectangular_beam_correction.py
   ```

2. A file dialog will appear to select a GCODE file.

3. After selecting the file, a window will appear to choose the axis (X or Y) to correct.

4. The program will adjust the feed rate based on the selected axis and save the corrected GCODE file.
