# Inno Setup Extractor GUI

Inno Setup Extractor GUI is a graphical user interface for the `innoextract` program by Daniel Scharrer (https://constexpr.org/innoextract/). This GUI provides an easy way to extract files from Inno Setup installers without running the actual setup executable.

## About Inno Setup and innoextract

**Inno Setup** is a tool to create installers for Microsoft Windows applications. **innoextract** allows you to extract such installers without running the actual setup executable under Windows or using Wine.

innoextract currently supports installers created by Inno Setup 1.2.10 to 6.2.2. It also supports some modified Inno Setup variants including Martijn Laan's My Inno Setup Extensions 1.3.10 to 3.0.6.1 as well as GOG.com's Inno Setup-based game installers. innoextract is able to unpack Wadjet Eye Games installers, Arx Fatalis patches, as well as various other Inno Setup executables.

## Features

- **Auto Extract**: Automatically extract files from a selected Inno Setup installer.
- **Advanced Extract**: Customize extraction options through a user-friendly interface.
- **Help and About**: Access detailed help information and about dialog from the GUI.

## Usage

1. **Select Installer**: Click "Browse" to select an Inno Setup installer file.
2. **Auto Extract**: Click "Auto Extract" to automatically extract the installer.
3. **Advanced Extract**: Click "Advanced Extract" to customize extraction options.
4. **Help**: Access help information from the advanced extract window or the menu bar.
5. **About**: Access information about the GUI from the menu bar.

## Installation

1. Download the `innoextract` executable from [constexpr.org](https://constexpr.org/innoextract/).
2. Place the `innoextract.exe` in the same directory as the GUI script.
3. Run the GUI script using Python.
```
python InnoExtracterGUI.py
```

## Compile from source
Install nuitka
```
pip install nuitka
```

Compile
```
nuitka --standalone --onefile --enable-plugin=tk-inter --output-dir=dist InnoExtracterGUI.py

```

## Full List of Dependencies
- Python standard library modules:
- tkinter
- subprocess
- os
- ctypes
- tkinter.filedialog
- tkinter.messagebox



## License

This project is licensed under the zlib/libpng license. See the LICENSE file for details.

## Acknowledgments

- **Daniel Scharrer**: Author of `innoextract` (daniel@constexpr.org)
- **Inno Setup**: Tool to create installers for Microsoft Windows applications.

## Limitations

- innoextract is developed on Linux but is cross-platform and works with any C++03 to C++17 compiler, architecture, and operating system supported by CMake, Boost, liblzma, and (optionally) iconv.
- Some features may not be fully supported on all platforms.

For more details, visit the [official innoextract page](https://constexpr.org/innoextract/).

