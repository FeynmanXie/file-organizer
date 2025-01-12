# Language

[English](README.md) | [中文](README_chinese.md)


# Intelligent File Organizer

## Project Overview

This is a Python-based intelligent file organization tool designed to help users automatically organize and categorize files in folders. Through a customizable rule system, users can easily automatically classify various types of files into different directories.

The tool features a modern graphical user interface, supporting real-time preview, progress display, operation undo, and other functions, making file organization simple and efficient.

### Key Features

- Automatic recognition and classification of various file types
- Customizable file classification rules
- Modern graphical user interface
- Detailed organization process logs
- Prevention of filename conflicts
- Batch processing support
- Real-time progress display
- File organization preview
- Undo operation support
- Rule import/export functionality
- Rule search functionality
- Keyboard shortcut support

## System Requirements

### Basic Requirements

- Operating System: Windows 7 or higher / macOS 10.12 or higher / Linux (major distributions)
- Python Version: 3.6 or higher
- Disk Space: At least 50MB available space
- Memory: At least 2GB RAM

### Python Dependencies

- tkinter >= 8.6
- pathlib >= 1.0.1
- typing >= 3.7.4
- dataclasses >= 0.8 (Python 3.6)

## Detailed Installation Steps

1. Ensure Python 3.6 or higher is installed:
```bash
python --version
```

2. Download or clone the project:
```bash
git clone https://github.com/FeynmanXie/file-organizer.git
cd file-organizer
```

3. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Verify installation:
```bash
cd project/src
python gui.py
```

## User Guide

### Basic Usage

1. Start the program:
   - Double-click to run `project/src/gui.py`
   - Or run in command line:
     ```bash
     cd project/src
     python gui.py
     ```

2. Select directory to organize:
   - Click "Browse" button
   - Or use shortcut Ctrl+O
   - Select the folder to organize

3. Manage classification rules:
   - View existing rules
   - Use search box to quickly find rules
   - Add/Edit/Delete rules
   - Import/Export rule configurations

4. Organize files:
   - Click "Preview Organization Results" to see how files will be classified
   - Click "Start Organization" to execute file organization
   - Use "Undo Last Operation" to restore file locations

### Keyboard Shortcuts

- Ctrl+N: Add new rule
- Ctrl+D: Delete rule
- Ctrl+E: Edit rule
- Ctrl+O: Open directory
- Ctrl+Z: Undo last operation

### Default Classification Rules

The program includes the following default classifications:

| Category | File Extensions |
|----------|----------------|
| Documents | .doc, .docx, .pdf, .txt, .md |
| Images | .jpg, .jpeg, .png, .gif, .bmp |
| Audio | .mp3, .wav, .flac, .m4a |
| Video | .mp4, .avi, .mkv, .mov |
| Archives | .zip, .rar, .7z, .tar, .gz |
| Programs | .exe, .msi, .app |
| Code | .py, .java, .cpp, .js, .html, .css |

### Custom Rules

1. Add Rule:
   - Click "Add Rule" button
   - Enter category name
   - Enter file extensions (comma-separated)
   - Click save

2. Edit Rule:
   - Select rule to edit
   - Click "Edit Rule" button
   - Modify category name or extensions
   - Click save

3. Delete Rule:
   - Select rule to delete
   - Click "Delete Rule" button
   - Confirm deletion

4. Import/Export Rules:
   - Click "Import Rules" to import rules from other configuration files
   - Click "Export Rules" to save current rule configuration

## Project Structure

```
project/
├── src/          # Source code
│   ├── file_organizer.py  # Core functionality implementation
│   └── gui.py            # Graphical interface implementation
├── tests/        # Test code
├── docs/         # Documentation
├── config/       # Configuration files
│   └── rules.json       # Classification rules configuration
├── assets/       # Static resources
│   └── icon.ico        # Program icon
├── logs/         # Log files
└── README.md     # Project documentation
```

## Developer Guide

### Environment Setup

1. Clone project and set up development environment:
```bash
git clone https://github.com/FeynmanXie/file-organizer.git
cd file-organizer
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

2. Install development dependencies:
```bash
pip install pytest pytest-cov pylint black
```

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Use pylint for code quality checking
- Keep function and method docstrings updated

### Testing

Run tests:
```bash
pytest tests/
```

Generate test coverage report:
```bash
pytest --cov=src tests/
```

## Troubleshooting

### Common Issues

1. Program won't start
   - Check if Python version meets requirements
   - Confirm all dependencies are correctly installed
   - Check error messages in log files

2. Cannot select directory
   - Confirm user has read/write permissions for target directory
   - Check if directory path contains special characters

3. Rules not working
   - Check if rule format is correct
   - Confirm file extensions have dot (.)
   - Verify rules.json file integrity

4. File organization fails
   - Check write permissions for target directory
   - Confirm no files are in use by other programs
   - View log files for detailed error information

### Log Location

Log files are saved in the `logs` directory, format: `file_organizer_YYYYMMDD.log`.

## Security Considerations

1. File Safety
   - Backup important files before organizing
   - Program will not delete any files, only move them
   - Automatically rename files if same name exists at destination

2. Permission Requirements
   - Program needs read/write permissions for source and target directories
   - Not recommended to run program with administrator privileges

## Change Log

### v1.0.0 (2025-01-12)
- Initial version release
- Implemented basic file organization functionality
- Added graphical user interface
- Added custom rules support
- Added preview and undo functionality

### v1.1.0 (Planned, update next month at latest)
- Add more file type support
- Optimize performance
- Improve user interface
- Add batch rule import functionality

## Contribution Guidelines

We welcome various forms of contribution, including but not limited to:

- Reporting issues and suggestions
- Submitting code improvements
- Improving documentation
- Adding new features
- Fixing bugs

### Contribution Steps

1. Fork project
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

### Submission Guidelines

- Use clear commit messages
- Keep commit granularity moderate
- Ensure code passes all tests
- Update relevant documentation

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Author

[Feynman]
- Email: woshixieruiman@gmail.com
- GitHub: [@FeynmanXie](https://github.com/FeynmanXie)

## Acknowledgments

Thanks to all developers who have contributed to this project. 
