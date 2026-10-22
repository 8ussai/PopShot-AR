# PopShot AR

A webcam game: hold up your hand and pop the enemies floating up the screen with your index finger.
Don't let any of them escape off the top. Every 5 pops, new enemies get faster.

A scoreboard window next to the game shows the top 4 scores.

## Requirements

- A webcam
- Python 3.10 (MediaPipe 0.10.14 supports Python 3.9–3.12)

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

## Controls

| Key | Action |
| --- | --- |
| Index finger | Pop enemies (both hands work) |
| Esc | Quit |
| Type, then Enter | Save your name after a top score |
| Esc on the name screen | Skip saving |

Closing either window also quits.

## Fonts

The scoreboard fonts are in `fonts/*.zip`. On Windows the game unpacks them into `fonts/_extracted/`
and loads them automatically. On macOS and Linux, unzip them and install the `.ttf`/`.otf` files
yourself, or the scoreboard uses the default font.

Licenses: Angkor and DynaPuff are under the SIL Open Font License (see `OFL.txt` in their zips).
Night Holiday has no license file. **Rinder Spring is a demo font for personal use only.**
Buy a license from NoahType before any commercial use.

## Scores

Scores are saved in `scores.db` (SQLite) in the project folder. Delete the file to reset the scoreboard.

## Project layout

```
src/
  main.py            game loop and screens
  enemy.py           enemy movement and hit checks
  hand_detector.py   MediaPipe fingertip tracking
  scoreboard_gui.py  Tkinter scoreboard window
  database.py        score storage
  fonts.py           unpacks and loads the fonts
  utils.py           image loading, drawing helpers
  config.py          sizes, speeds, file paths
assets/              enemy pictures, finger cursor, logo, pop sound
fonts/               font zips
```
