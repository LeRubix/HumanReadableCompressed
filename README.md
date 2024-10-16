# HumanReadableCompressed

Python scripts for compressing and decompressing human-readable serialized files (JSON/JSONL/YAML/YML). This project includes a convenient GUI executable file (`hrcGUI.exe`) for easy usage. Up to 99.8% compression has been achieved using this tool!

## Set up
To get started, download the [latest release](https://github.com/LeRubix/HumanReadableCompressed/releases/latest) and run the `hrcGUI.exe`, or execute the Python scripts through a terminal.

## Usage
### Command Line
To compress a file, use:
```bash
python hrc.py <path\to\file>
```
To decompress a file, use:
```bash
python hrdc.py <path\to\file.hrc>
```

### GUI
To use the GUI, simply open `hrcGUI.exe` and:
- Click the "Choose a file to compress" button to select a file for compression.
- Click the "Choose a file to decompress" button to select a `.hrc` file for decompression.


![image](https://github.com/user-attachments/assets/31ea9c00-5eef-44ae-990e-282662aa3c37)


## Future Plans
I may release a version in the future that specifically supports adding this tool to your system's PATH. Additionally, I am considering developing a Visual Studio Code extension that can read `.hrc` files directly, eliminating the need for decompression.

## License
This project is licensed under the Mozilla Public License 2.0 (MPL-2.0). See the [LICENSE](LICENSE) file for more details.