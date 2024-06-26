# uMyo_and_uLabel_python_tools

Welcome to the uMyo_and_uLabel Python tools repository! This project provides tools for gathering and processing somatosensory data using machine learning techniques.

## Overview

This repository contains Python scripts and modules to assist in collecting, labeling, and analyzing data from somatosensory devices. These tools are designed to facilitate the development of machine learning models for various applications in the field of somatosensory research.

## Features

- **Data Collection**: Scripts to gather data from somatosensory devices.
- **Labeling Tools**: Tools for labeling collected data.
- **Machine Learning**: Scripts to train and test machine learning models on labeled data.
- **Utilities**: Additional utilities for data parsing and mathematical operations.

## Repository Structure

- **`training_data/`**: Directory containing sample training data.
- **`bootloader_usb.py`**: Script for bootloading via USB.
- **`quat_math.py`**: Module for quaternion mathematics.
- **`train_machine_learning.py`**: Script to train machine learning models.
- **`ulabel_class.py`**: Class definition for labeling tools.
- **`ulabel_display.py`**: Script for displaying labeled data.
- **`ulabel_gather_data2file.py`**: Main script for gathering data to file.
- **`ulabel_parser.py`**: Parser for labeled data.
- **`ulabel_testing.py`**: Script for testing labeled data.
- **`umyo_class.py`**: Class definition for uMyo device.
- **`umyo_parser.py`**: Parser for uMyo data.

## Installation

Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/turfptax/uMyo_and_uLabel_python_tools.git
cd uMyo_and_uLabel_python_tools
pip install -r requirements.txt
```

## Usage

To gather data using the main script, run:

```bash
python ulabel_gather_data2file.py
```
### Main Script: ulabel_gather_data2file.py
This script collects data from connected somatosensory devices and saves it to a CSV file. It reads data from available serial ports, parses the data using umyo_parser and ulabel_parser, and displays it using ulabel_display. The collected data includes attributes such as device IDs, sensor values, and timestamps.

**Key Functions**
parse_preprocessor(data): Preprocesses the incoming data for parsing.
get_file_number_and_timestamp(directory): Generates a file number and timestamp for naming output files.
get_ulabel_data(ulabel_data): Extracts data from uLabel devices.
get_umyo_data(umyo_data): Extracts data from uMyo devices.
append_to_csv(file_name, ulabel_data, umyo_data): Appends data to a CSV file.
write_to_csv(file_name): Writes the collected data to a CSV file.
append_to_object(file_name, ulabel_data, umyo_data): Appends data to an in-memory object for later writing.

## Example Usage

```python
# Run the script
python ulabel_gather_data2file.py

# Follow the on-screen instructions for training.
```
## License
This project is licensed under the MIT License. See the LICENSE file for more details.

