# 🎸 Mammut Bandtester

Dieses Programm hilft dir, die Top-Songs aus einer Bandliste automatisch zu finden und in deine bevorzugte Musikplattform (Spotify, Apple Music, Deezer, etc.) zu importieren.

## 🎯 Wofür ist das?

Mammut gibt dir eine Excel-Liste mit Bands? Dieses Programm:
1. Sucht die Top-3-Songs jeder Band auf Deezer
2. Erstellt eine schöne Liste mit all deinen gefundenen Songs
3. Ermöglicht es dir, diese Songs ganz einfach in Spotify, Apple Music oder deine andere liebste Musikplattform zu importieren

## ⚙️ Installation

### Schritt 1: Das Programm herunterladen

1. Gehe auf die GitHub-Seite des Projekts
2. Klicke auf den grünen Button **"Code"** (rechts oben)
3. Klicke auf **"Local"**
4. Klicke auf **"Download ZIP"**
5. Die Datei wird heruntergeladen
6. **Entpacke** die ZIP-Datei (Rechtsklick → "Alles extrahieren..." oder "Extract All")
7. Öffne den entpackten Ordner

### Schritt 2: Das Programm starten

**Voraussetzung: Python muss installiert sein**

Falls Python noch nicht installiert ist:
1. In dem ordner findest du die Datei **`python-3.13.9-amd64.exe`**
2. Doppelklick auf die Datei
3. **WICHTIG:** Bei der Installation unbedingt das Häkchen bei **"Add Python to PATH"** setzen! (unten links)
4. Klicke auf "Install Now"
5. Warte bis die Installation fertig ist
6. Schließe das Fenster

**Dann das Programm starten:**

**Einfachste Variante (für alle):**
- Doppelklick auf `main.py`
- Das wars! Das Programm startet und lädt alle notwendigen Erweiterungen automatisch herunter (beim ersten Mal)

**Alternative (wenn Doppelklick nicht funktioniert):**
1. Öffne PowerShell/Eingabeaufforderung im Ordner des Programms
2. Tippe: `python main.py`

**Hinweis:** Das Programm öffnet sich dann in einem schönen Fenster mit Buttons - nicht erschrecken! 😉

## 🚀 Wie du das Programm nutzt

### Schritt 1: Excel-Datei laden

1. Das Programm öffnet sich automatisch
2. Klicke auf den Button **"📁 Datei auswählen"**
3. Wähle deine Excel-Datei aus (die, die du von Mammut bekommen hast)
4. Das Programm zeigt dir die ausgewählte Datei an

### Schritt 2: Die Verarbeitung starten

1. Klicke auf den grünen Button **"▶ Starten"**
2. Das Programm sucht nun nach jeder Band und deren Top-3-Songs
3. Du siehst live in der Mitte, welche Bands gerade verarbeitet werden
4. Dies kann ein paar Minuten dauern (hängt davon ab, wie viele Bands du hast)
5. Wenn es fertig ist, zeigt es dir eine Meldung an

### Schritt 3: Die Playlist speichern

1. Wenn das Programm fertig ist, klicke auf **"💾 Speichern"**
2. Wähle einen Ort auf deinem Computer, wo die Datei gespeichert werden soll
3. Die Datei wird als `playlist.txt` gespeichert

## 📝 Die Playlist nutzen

Nachdem die Datei gespeichert wurde:

### Schritt 1: Die gefundenen Songs kopieren

1. Öffne die `playlist.txt` Datei mit Notepad oder Word
2. Du siehst die Ergebnisse aufgeteilt in drei Bereiche:
   - **Playlist:** Die gefundenen Songs (das brauchst du!)
   - **No songs found:** Bands, die keine Songs hatten
   - **Not found:** Bands, die nicht gefunden wurden

3. **Markiere ALLE Songs im "Playlist" Bereich** (die Zeilen mit "Band - Song")
4. Kopiere sie (STRG+C)

### Schritt 2: Zu TuneMyMusic gehen

1. Öffne deinen Internet-Browser
2. Gehe auf: **https://www.tunemymusic.com/**

### Schritt 3: Die Songs einfügen

1. Auf der TuneMyMusic-Seite siehst du oben verschiedene Optionen
2. Scrolle bis zum Ende der Liste
3. Klicke auf **"Free Text"** (oder "Freitext")
4. Im großen Textfeld kannst du nun deine kopierten Songs einfügen
5. Klicke dort rein und füge die Songs ein (STRG+V)
6. Klicke auf **"Transfer"** oder **"Übertragen"**

### Schritt 4: Dein Ziel wählen

1. TuneMyMusic fragt dich jetzt, in welche Musikplattform du die Songs importieren möchtest
2. Wähle aus:
   - 🎵 **Spotify**
   - 🎵 **Apple Music**
   - 🎵 **Deezer**
   - 🎵 **YouTube Music**
   - Oder eine andere Plattform deiner Wahl

### Schritt 5: Anmelden und fertig!

1. Klicke auf deine gewählte Plattform
2. Du wirst aufgefordert, dich anzumelden (falls noch nicht geschehen)
3. Gib deine Zugangsdaten ein
4. TuneMyMusic importiert automatisch alle Songs in deine Playlist
5. **Fertig!** Deine Playlist ist jetzt in deiner Musikapp verfügbar 🎉

## 📊 Ergebnis-Beispiel

Die `playlist.txt` sieht dann ungefähr so aus:

```
Playlist:
Metallica - Enter Sandman
Metallica - The Unforgiven
Metallica - Master of Puppets
Iron Maiden - The Trooper
Iron Maiden - Hallowed Be Thy Name
Iron Maiden - Wasted Years
Black Sabbath - Paranoid
...

No songs found:
(hier würden Bands stehen, die gefunden wurden, aber keine Songs haben)

Not found:
(hier würden Bands stehen, die gar nicht gefunden wurden)
```

## ⚠️ Häufige Probleme

### "Keine Datei gewählt"
- Wähle eine Excel-Datei aus, bevor du "Starten" klickst

### "Band nicht gefunden"
- Manche Bands existieren nicht auf Deezer (oder haben einen anderen Namen)
- Diese werden am Ende der Datei aufgelistet
- Das ist normal!

### "Keine Songs verfügbar"
- Manche Bands haben keine indexierten Top-Songs auf Deezer
- Diese werden auch in der Datei vermerkt
- Das ist auch normal!

### "Ich kann die Datei nicht öffnen"
- Versuche die Datei mit Notepad zu öffnen (Rechtsklick → Öffnen mit → Notepad)
- Oder kopiere den Inhalt einfach direkt in den Browser

## 🆘 Hilfe

Falls etwas nicht funktioniert:
1. Überprüfe deine Internetverbindung
2. Versuche das Programm neu zu starten
3. Stelle sicher, dass es eine gültige Excel-Datei ist

