# MKV to MOV Converter

## Overview

The **MKV to MOV Converter** is a user-friendly desktop application that simplifies the process of converting MKV files to MOV format. Built with PySide6 and powered by FFmpeg, this tool ensures efficient and seamless video conversion while offering a modern and intuitive interface.

---

## Features

- **File Selection**: Easily choose MKV files for conversion using a graphical interface.
- **Output Customization**: Select the desired location and name for the converted MOV file.
- **Progress Monitoring**: Real-time logs display the conversion process in detail.
- **Theme Support**: Toggle between light and dark themes for optimal viewing.
- **Cross-Platform**: Runs on Linux, Windows, and macOS with minimal setup.
- **About Section**: Provides quick access to version details and credits.

---

## Prerequisites

- **FFmpeg**: Ensure FFmpeg is installed and accessible via the command line.
  
  ```bash
  sudo apt install ffmpeg  # For Linux
  brew install ffmpeg      # For macOS
  choco install ffmpeg     # For Windows (using Chocolatey)
  ```

- **Python 3.9+**: Install Python from the [official website](https://www.python.org/).

- **PySide6**: Install the required library using pip:

  ```bash
  pip install PySide6
  ```

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/mkv-to-mov-converter.git
   cd mkv-to-mov-converter
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:

   ```bash
   python main.py
   ```

---

## Usage

1. Launch the application.
2. Click **"Select MKV File"** and choose the file you want to convert.
3. Click **"Generate MOV"** and specify the output location and file name.
4. Monitor the progress in the log section.
5. Once completed, the MOV file will be available at your specified location.

---

## Screenshots

### Light Theme:
![image](https://github.com/user-attachments/assets/6b98799d-1faf-45b3-8c74-aef66132741f)

### Dark Theme:
![image](https://github.com/user-attachments/assets/612be71f-debd-4b91-91cb-44764e179474)

---

## License

This program is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for more details.

---

## Contributing

Contributions are welcome! If you have ideas for new features or improvements:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## Acknowledgments

- **FFmpeg**: For powering the video conversion process.
- **PySide6**: For providing the tools to build a modern GUI.

---

## Contact

For support or inquiries, feel free to reach out at [muhammmedaly@gmail.com](mailto:muhammmedaly@gmail.com).

