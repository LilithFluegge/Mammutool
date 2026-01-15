"""
Deezer API Playlist Creator
Fetches top songs for artists from an Excel spreadsheet and saves to text file.
"""

import sys
import subprocess
import importlib.util

# Check and install required packages
def check_and_install_requirements():
    """Check if required packages are installed, install if not."""
    required_packages = {
        'requests': 'requests',
        'openpyxl': 'openpyxl',
        'tkinter': 'tkinter'  # This is built-in with Python
    }
    
    missing_packages = []
    
    for package_import, package_pip in required_packages.items():
        if package_import == 'tkinter':
            # tkinter comes with Python, skip pip check
            spec = importlib.util.find_spec(package_import)
        else:
            spec = importlib.util.find_spec(package_import)
        
        if spec is None and package_import != 'tkinter':
            missing_packages.append(package_pip)
    
    if missing_packages:
        print("🔄 Installiere fehlende Pakete...")
        for package in missing_packages:
            try:
                print(f"   📦 {package}...", end=" ", flush=True)
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
                print("✓")
            except subprocess.CalledProcessError:
                print(f"✗ Fehler beim Installieren von {package}")
                sys.exit(1)
        print("✓ Alle Pakete installiert!\n")

# Run the check before importing
check_and_install_requirements()

import requests
import openpyxl
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import threading


class DeezerPlaylistCreator:
    """Creates a playlist from artists in an Excel spreadsheet using Deezer API."""
    
    BASE_URL = "https://api.deezer.com"
    
    def __init__(self, excel_file: str, output_file: str = "playlist.txt"):
        """
        Initialize the creator.
        
        Args:
            excel_file: Path to the Excel file containing artist names
            output_file: Path to the output text file
        """
        self.excel_file = excel_file
        self.output_file = output_file
        self.songs = []
        self.not_found = []
        self.no_songs = []
    
    def get_artists_from_excel(self) -> list:
        """
        Extract artist names from Excel file (B2:BX).
        
        Returns:
            List of artist names
        """
        try:
            wb = openpyxl.load_workbook(self.excel_file)
            ws = wb.active
            artists = []
            
            # Get values from B2 to BX (column B only, rows 2 to 76)
            for row in range(2, 77):
                cell_value = ws[f'B{row}'].value
                if cell_value and isinstance(cell_value, str):
                    artist = cell_value.strip()
                    if artist:
                        artists.append(artist)
            
            return artists
        except FileNotFoundError:
            print(f"Error: Excel file '{self.excel_file}' not found.")
            return []
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return []
    
    def search_artist(self, artist_name: str) -> dict:
        """
        Search for an artist on Deezer.
        
        Args:
            artist_name: Name of the artist
            
        Returns:
            Artist data or empty dict if not found
        """
        try:
            url = f"{self.BASE_URL}/search/artist"
            params = {"q": artist_name}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                return data["data"][0]
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Error searching for artist '{artist_name}': {e}")
            return {}
    
    def get_top_songs(self, artist_id: int, limit: int = 3) -> list:
        """
        Get top songs for an artist.
        
        Args:
            artist_id: Deezer artist ID
            limit: Maximum number of songs to retrieve
            
        Returns:
            List of song titles
        """
        try:
            url = f"{self.BASE_URL}/artist/{artist_id}/top"
            params = {"limit": limit}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            songs = []
            if data.get("data"):
                for track in data["data"]:
                    songs.append(track.get("title", "Unknown"))
            
            return songs
        except requests.exceptions.RequestException as e:
            print(f"Error getting top songs for artist ID {artist_id}: {e}")
            return []
    
    def process_artists(self):
        """Process all artists and fetch their top songs."""
        artists = self.get_artists_from_excel()
        
        if not artists:
            print("No artists found in Excel file.")
            return
        
        print(f"Processing {len(artists)} artist(s)...")
        
        for artist_name in artists:
            print(f"Processing: {artist_name}")
            
            artist_data = self.search_artist(artist_name)
            
            if not artist_data:
                self.not_found.append(f"{artist_name} not found")
                continue
            
            artist_id = artist_data.get("id")
            top_songs = self.get_top_songs(artist_id)
            
            if not top_songs:
                self.no_songs.append(f"no songs for {artist_name} found")
            else:
                for song in top_songs:
                    self.songs.append(f"{artist_name} - {song}")
    
    def save_playlist(self):
        """Save the playlist to a text file."""
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                # Write found songs first
                f.write("Playlist:\n")
                for song in self.songs:
                    f.write(song + "\n")
                
                # Write no songs found
                if self.no_songs:
                    f.write("\nNo songs found:\n")
                    for entry in self.no_songs:
                        f.write(entry + "\n")
                
                # Write not found at the bottom
                if self.not_found:
                    f.write("\nNot found:\n")
                    for entry in self.not_found:
                        f.write(entry + "\n")
            
            print(f"\nPlaylist saved to '{self.output_file}'")
            print(f"Total entries: {len(self.songs) + len(self.no_songs) + len(self.not_found)}")
        except Exception as e:
            print(f"Error saving playlist: {e}")
    
    def ask_continue(self) -> bool:
        """Ask user if they want to continue."""
        while True:
            response = input("\nPress ENTER to continue or X to stop: ").strip().upper()
            if response == "X":
                return False
            elif response == "":
                return True
            else:
                print("Invalid input. Press ENTER to continue or X to stop.")
    
    def run(self):
        """Execute the complete process."""
        self.process_artists()
        self.save_playlist()


class PlaylistCreatorGUI:
    """GUI for the Deezer Playlist Creator using tkinter."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Mammut Bandtester")
        self.root.geometry("650x500")
        self.root.resizable(True, True)
        
        # Set color scheme
        bg_color = "#f0f0f0"
        header_color = "#2c3e50"
        accent_color = "#3498db"
        success_color = "#27ae60"
        error_color = "#e74c3c"
        
        self.root.configure(bg=bg_color)
        
        self.creator = None
        self.is_running = False
        self.excel_file = None
        
        # Title label
        title_label = tk.Label(
            root, 
            text="🎸 Mammut Bandtester", 
            font=("Arial", 18, "bold"),
            bg=header_color,
            fg="white",
            pady=15
        )
        title_label.pack(fill="x")
        
        # File selection frame
        file_frame = tk.Frame(root, bg=bg_color)
        file_frame.pack(pady=12, padx=20)
        
        # Browse button
        browse_button = tk.Button(
            file_frame,
            text="📁 Datei auswählen",
            command=self.browse_file,
            width=25,
            bg=accent_color,
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
            padx=10,
            pady=8,
            cursor="hand2"
        )
        browse_button.pack()
        
        # File info label
        self.file_info_label = tk.Label(
            root, 
            text="Keine Datei ausgewählt", 
            font=("Arial", 10), 
            fg=error_color,
            bg=bg_color
        )
        self.file_info_label.pack(pady=3)
        
        # Status label
        self.status_label = tk.Label(
            root, 
            text="Bereit", 
            font=("Arial", 10, "bold"), 
            fg=accent_color,
            bg=bg_color
        )
        self.status_label.pack(pady=3)
        
        # Progress label
        self.progress_label = tk.Label(
            root, 
            text="", 
            font=("Arial", 9), 
            fg="#7f8c8d",
            bg=bg_color
        )
        self.progress_label.pack(pady=2)
        
        # Output text area
        self.output_frame = tk.Frame(root, bg=bg_color)
        self.output_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.output_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Text widget
        self.output_text = tk.Text(
            self.output_frame, 
            height=10, 
            width=70, 
            yscrollcommand=scrollbar.set, 
            font=("Courier New", 9),
            bg="white",
            fg="#2c3e50",
            relief="solid",
            bd=1,
            padx=8,
            pady=8
        )
        self.output_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.output_text.yview)
        
        # Button frame
        button_frame = tk.Frame(root, bg=bg_color)
        button_frame.pack(pady=15)
        
        # Start button
        self.start_button = tk.Button(
            button_frame, 
            text="▶ Starten", 
            command=self.start_processing, 
            width=12, 
            bg=success_color, 
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
            padx=10,
            pady=8,
            cursor="hand2"
        )
        self.start_button.pack(side="left", padx=5)
        
        # Stop button
        self.stop_button = tk.Button(
            button_frame, 
            text="⏹ Stopp", 
            command=self.stop_processing, 
            width=12, 
            bg=error_color, 
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
            padx=10,
            pady=8,
            cursor="hand2",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        # Save button
        self.save_button = tk.Button(
            button_frame, 
            text="💾 Speichern", 
            command=self.save_file, 
            width=12, 
            bg="#9b59b6", 
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
            padx=10,
            pady=8,
            cursor="hand2",
            state="disabled"
        )
        self.save_button.pack(side="left", padx=5)
    
    def browse_file(self):
        """Browse for Excel file."""
        file_path = filedialog.askopenfilename(
            title="Excel Datei auswählen",
            filetypes=[("Excel Dateien", "*.xlsx *.xls"), ("Alle Dateien", "*.*")]
        )
        if file_path:
            self.excel_file = file_path
            self.file_info_label.config(text=f"✓ Datei: {os.path.basename(file_path)}", fg="#27ae60")
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", f"Ausgewählt: {file_path}\n\nBereit zum Verarbeiten. Klicke auf 'Starten' um zu beginnen.")
            self.output_text.config(state="disabled")
    
    def start_processing(self):
        """Start processing the playlist."""
        if not self.excel_file:
            messagebox.showerror("Fehler", "Bitte wähle zuerst eine Excel-Datei aus")
            return
        
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Verarbeitung läuft...", fg="orange")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")
        
        # Run in a separate thread to avoid freezing GUI
        thread = threading.Thread(target=self.process_thread)
        thread.daemon = True
        thread.start()
    
    def log_output(self, message):
        """Add message to output text widget."""
        self.output_text.config(state="normal")
        self.output_text.insert("end", message + "\n")
        self.output_text.see("end")
        self.output_text.config(state="disabled")
        self.root.update()
    
    def process_thread(self):
        """Process playlist in a separate thread."""
        try:
            self.creator = DeezerPlaylistCreator(self.excel_file, "playlist.txt")
            artists = self.creator.get_artists_from_excel()
            self.log_output(f"Es wurden {len(artists)} Band(s) gefunden\n{'─' * 50}")
            
            for i, artist_name in enumerate(artists):
                if not self.is_running:
                    self.log_output(f"\n⚠ Verarbeitung vom Benutzer gestoppt")
                    break
                
                self.progress_label.config(text=f"Verarbeite {i+1}/{len(artists)}: {artist_name[:30]}...")
                self.log_output(f"\n[{i+1}/{len(artists)}] {artist_name}")
                
                artist_data = self.creator.search_artist(artist_name)
                
                if not artist_data:
                    self.creator.not_found.append(f"{artist_name} not found")
                    self.log_output(f"      ✗ Nicht auf Deezer gefunden")
                    continue
                
                artist_id = artist_data.get("id")
                top_songs = self.creator.get_top_songs(artist_id)
                
                if not top_songs:
                    self.creator.no_songs.append(f"no songs for {artist_name} found")
                    self.log_output(f"      ⚠ Keine Songs verfügbar")
                else:
                    self.log_output(f"      ✓ {len(top_songs)} Song(s) gefunden:")
                    for j, song in enumerate(top_songs, 1):
                        self.creator.songs.append(f"{artist_name} - {song}")
                        self.log_output(f"         {j}. {song}")
            
            if self.is_running:
                self.status_label.config(text="✓ Verarbeitung abgeschlossen!", fg="#27ae60")
                self.save_button.config(state="normal")
                self.log_output(f"\n{'─' * 50}\n✓ Fertig! Klicke auf 'Speichern' um die Playlist zu speichern.")
            else:
                self.status_label.config(text="⚠ Vom Benutzer gestoppt", fg="#e74c3c")
        except Exception as e:
            self.status_label.config(text=f"✗ Fehler: {str(e)}", fg="#e74c3c")
            self.log_output(f"\n✗ Fehler: {str(e)}")
        finally:
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.progress_label.config(text="")
            self.is_running = False
    
    def stop_processing(self):
        """Stop the processing."""
        self.is_running = False
        self.status_label.config(text="Stopping...", fg="red")
    
    def save_file(self):
        """Save the playlist to a specific location."""
        if self.creator is None:
            messagebox.showerror("Fehler", "Noch keine Playlist generiert")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Playlist speichern unter",
            defaultextension=".txt",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
        )
        
        if file_path:
            try:
                self.creator.output_file = file_path
                self.creator.save_playlist()
                messagebox.showinfo("✓ Erfolg", f"Playlist gespeichert unter:\n{file_path}")
                self.save_button.config(state="disabled")
                self.log_output(f"\n✓ Playlist gespeichert unter: {file_path}")
            except Exception as e:
                messagebox.showerror("✗ Fehler", f"Fehler beim Speichern:\n{str(e)}")


def main():
    """Main entry point."""
    root = tk.Tk()
    gui = PlaylistCreatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
