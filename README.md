# File Sorter

File Sorter is a simple, yet effective Python application for organizing files in a directory. This script categorizes files into folders based on their file type, such as Images, Documents, Archives, Audio, Video, PDFs, HTML, and Executables. Additionally, it normalizes filenames to ensure consistency and readability.

## Features

- **File Organization:** Automatically sorts files into designated folders based on file type.
- **Filename Normalization:** Converts Cyrillic names to Latin script and replaces non-alphanumeric characters with underscores.
- **Archive Handling:** Unpacks archive files (.zip, .rar, etc.) and sorts their contents.
- **User Interface:** Easy-to-use GUI for selecting a directory and initiating the sorting process.
- **Log Output:** Real-time log updates on the GUI displaying the sorting progress.

## Prerequisites

- Python 3.x
- Tkinter library (usually comes pre-installed with Python).

## Installation

Clone the repository or download the source code. Then install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Run file_sorter.py.

- Click the "Выбрать папку" button to select a directory.
- Press the "Начать сортировку" button to start sorting the files in the selected directory.

- Monitor the process through the log output on the GUI.

## Contributing

- Contributions are welcome! If you have a suggestion or an improvement, please feel free to fork the repository and create a pull request.

## License

MIT License