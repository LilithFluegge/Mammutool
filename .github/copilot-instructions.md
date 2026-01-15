# Deezer Playlist Creator Project Instructions

## Project Overview
Python application that fetches top songs for artists from an Excel spreadsheet using the Deezer API.

## Setup Steps Completed
- [x] Project structure created
- [x] Main Python script implemented (main.py)
- [x] Dependencies specified (requests, openpyxl)
- [x] README documentation created

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Place your Excel file with artist names in column B (B2:BX) in the project directory
3. Update `excel_file` path in main.py if needed
4. Run: `python main.py`

## Output
Creates `playlist.txt` with artist names and their top songs in the format:
- `artist name - song title`
- `artist name not found` (if artist not found)
- `no songs for artist name found` (if no songs available)
