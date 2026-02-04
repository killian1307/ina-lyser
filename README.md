[![Static Badge](https://img.shields.io/badge/lang-en-FF0000)](README.md) [![Static Badge](https://img.shields.io/badge/lang-fr-0000FF)](README.fr.md)

# ⚡⚽ Ina-Lyser ⚽⚡

![Official Artwork](assets/img/cover.jpg)
<p align="right">
<em>Official Artwork</em>
</p>

[![Static Badge](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🌐 Online Access

**You can access and use the scanner directly in your browser without installation:**

<h2 align="center">
🚀 Click here to launch: <a href="" target="_blank">https://ina-lyser.streamlit.app</a>
</h2>

**Ina-Lyser** is an automated tool designed for **Inazuma Eleven: Victory Road** players. It allows you to upload screenshots of your team formations, automatically detects player names, stats, and tactical setups using local AI (OCR), and exports the data into a clean JSON format. My goal was primarily to build this tool as part of a larger **Inazuma Eleven: Victory Road** competitive website project, but other tools or team builders could take advantage of the simple execution and clean format too!

## Summary

The project solves the tedious task of manually transcribing team data. By using **Computer Vision** and **Fuzzy String Matching**, Ina-Lyser can read low-resolution or slightly obstructed text from game screenshots, match it against a database of known players, and reconstruct your exact team formation in a clean format.

## Features

* **Local, AI-Powered Scanning:** Uses `EasyOCR` and `OpenCV` to read text from images.
* **Fuzzy Matching:** Smart detection that fixes OCR typos (e.g., correcting "Yuya Kogurer" to "Yuya Kogure").
* **Formation Detection:** Automatically identifies formations like 4-4-2 Diamond, 4-4-2 Box, 3-5-2 Freedom, etc.
* **JSON Export:** Generates a structured `.json` file containing all player data, stats, and positions.
* **Dual Language Support:** Capable of detecting player names in both Romanji and Localized formats.

## Prerequisites & Installation

> 📝
> The project is hosted online at [https://ina-lyser.streamlit.app/](https://ina-lyser.streamlit.app/), so no installation is required for standard use. However, if you wish to run it locally or contribute, follow these steps.

### Setup Steps

1.  **Clone the Repository:**
    Download the source code from GitHub to your local machine.

2.  **Install Python:**
    Ensure you have **Python 3.9+** installed.

3.  **Install Dependencies:**
    Open your terminal or command prompt in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App:**
    Start the local server using Streamlit:
    ```bash
    streamlit run main.py
    ```
    *(Note: Replace `main.py` with your entry file name if different, e.g., `app.py`)*

## Usage Protocol

1.  **Upload:** Drag and drop a clear screenshot of your team menu (JPG/PNG) into the upload zone.
    * *Limit:* Max 5MB per file.
2.  **Scan:** Click the **"Scan Team"** button.
    * The app will process the image, applying filters to enhance text readability.
    * It will display a log of detected players in real-time.
3.  **Verify & Download:**
    * Once finished, the detected team members and formation will be displayed.
    * Click **"Download JSON"** to save your team data.

> 💡
> **Tip:** For best results, use standard 1080p screenshots. Avoid taking photos of your screen with a phone, as glare can interfere with the text recognition.

## Architecture Overview

The project structure is organized as follows:

* **`main.py`**: The entry point for the Streamlit web application.
* **`assets/`**:
    * **`package/detector.py`**: The core logic containing the `ExactTeamScanner` class, OCR engine, and fuzzy matching algorithms.
    * **`package/website.py`**: Handles the UI layout and file upload management.
    * **`models/`**: Contains the offline EasyOCR models (to ensure fast cloud deployment).
    * **`players/db.csv`**: The database containing valid player names and stats.
* **`requirements.txt`**: List of Python libraries required to run the app.

## Dependencies

This project relies on the following open-source libraries:

* **Streamlit:** For the web interface and cloud hosting.
* **EasyOCR:** For optical character recognition (text reading).
* **OpenCV (headless):** For image preprocessing (grayscale, contrast, resizing).
* **Pandas:** For managing the player database (CSV).
* **Difflib:** For fuzzy string matching and typo correction.

## License

**MIT License**

You are free to use, modify, distribute, and sell this software, provided that you include the original copyright notice and license in any copies or substantial portions of the software.

For more details, please refer to the [LICENSE](LICENSE) file in this repository.
