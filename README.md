# Auto File Organizer

Automated file organizer that watches a folder and automatically sorts files 
into categories using Watchdog and Mutagen.

## How it works
Watches a source folder in real time. When a new file is detected, it moves 
it to the corresponding destination folder based on its extension and type.

| Type | Formats |
|------|---------|
| 🎵 Music | .mp3, .wav, .flac, .m4a, .wma, .aac |
| 🔊 SFX | Audio files under 30 seconds |
| 🎬 Video | .mp4, .mov, .avi, .webm, .mkv... |
| 🖼️ Images | .jpg, .png, .gif, .svg, .psd... |
| 📄 Documents | .pdf, .docx, .xlsx, .pptx... |

## Requirements
pip install watchdog mutagen

## Setup
1. Clone the repository
2. Fill in the directory paths in auto.py
3. Run the script

## Usage
python auto.py

## Auto Start (Windows)
1. Create a shortcut of `run.bat`
2. Press `Win + R` → type `shell:startup` → Enter
3. Move the shortcut to that folder

The organizer will start automatically every time you log in.**
