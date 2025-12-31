# Vericode
Python-based desktop application for generating and scanning secure, customizable QR codes with encryption and batch processing support.

## Overview

Vericode is a Python-based desktop application that provides a unified interface for generating and scanning QR codes with advanced customization, encryption, and batch processing capabilities. It is designed to support both individual and large-scale QR generation workflows through an intuitive, user-focused interface.

Developed as part of an undergraduate Semester 3 mini project, Vericode emphasizes practical implementation, clean design, and real-world applicability.

## Features

- Text & File-Based QR Generation: Generate QR codes from direct user input or uploaded text files.

- Batch QR Generation:
Create multiple QR codes simultaneously using structured CSV or Excel files.

- Encrypted QR Codes
Secure QR content using password-based encryption to protect sensitive data.

- Color Customization
Customize QR foreground and background colors for improved readability and branding.

- Logo Embedding
Embed custom logos within QR codes without affecting scan reliability.

- Multi-Format Export
Save generated QR codes in PNG, JPG, or PDF formats.

- QR Code Scanning
Decode QR codes from uploaded images using computer vision techniques.

- Dark & Light Mode Interface
Switch between light and dark themes for enhanced user experience.

## Demo Video



## Screenshots
<img width="902" height="839" alt="image" src="https://github.com/user-attachments/assets/a7008962-6848-4652-87ef-81d249149b74" />
<img width="902" height="839" alt="image" src="https://github.com/user-attachments/assets/0e029506-bcee-4406-a104-9c8667f5d232" />
<img width="902" height="839" alt="image" src="https://github.com/user-attachments/assets/1458ba30-a3d0-45c2-abd9-e478daeb221b" />
<img width="1920" height="1030" alt="image" src="https://github.com/user-attachments/assets/6bacea27-4c7a-42e3-b407-a10379d2e896" />









## Tech Stack

| Area | Tools / Libraries |
|------|------------------|
| Core Language | Python |
| Desktop Interface | Tkinter, ttkbootstrap |
| QR Code Creation | qrcode |
| Image Handling | Pillow (PIL) |
| QR Code Detection | OpenCV (cv2) |
| Data Security | cryptography (Fernet) |
| Data & File Operations | pandas, csv, os |
| Export Utilities | FPDF |
| UI Components | ttkbootstrap, ScrolledFrame |


## Installation

- Clone the repository
```bash
git clone <repository-url>
cd vericode
```

- Install required dependencies
```bash
pip install -r requirements.txt
```

- Run the application
```bash
python vericode.py
```
## Workflow

- Application Launch:
Initializes the user interface, theme settings, and core QR modules.

- User Input Selection:
Accepts text input or file uploads as QR data sources.

- Customization & Security:
Applies visual customization options and optional encryption.

- QR Code Generation:
Encodes processed data and generates the QR code output.

- Batch Processing:
Processes structured files to generate QR codes in bulk.

- Export & Storage:
Saves generated QR codes in selected formats and locations.

- QR Code Scanning & Decoding:
Decodes uploaded QR images and securely decrypts protected data.

