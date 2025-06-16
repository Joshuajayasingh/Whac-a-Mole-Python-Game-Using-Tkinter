
# Whac-A-Mole Game 

A fun GUI-based Whac-A-Mole game built using Python's `tkinter` and `pygame` libraries.

## Features

- Interactive GUI with images and sound effects
- Background music with mute on game start and resume on game over
- Leaderboard with top 10 scores (high & cumulative)
- Level-based gameplay with increasing difficulty
- Rules page and proper error handling for missing assets

---

## Requirements

- Python 3.6 or above
- Dependencies:
  - `tkinter` (usually included with Python)
  - `pygame`
  - `Pillow`

Install dependencies with:

```bash
pip install pygame pillow
````

---

## Setup

1. **Download Required Assets**

This game needs the following assets:

* `whacs.jpg` — Background image
* `moles.png` — Mole image
* `theme.wav` — Background music
* `hit.wav` — Sound on hitting mole
* `lost.wav` — Sound on losing the game

You can download all required files from this link:
🔗 [Download Game Assets](https://drive.google.com/drive/folders/14k5J8jKl5MqXV1a7fVO2uFpHjWntE4Tm?usp=sharing)

2. **Place Files**

Place all the downloaded files in the same directory as `whac-a-mole.py`.

---

## How to Run

```bash
python whac-a-mole.py
```

---

## Game Rules

* The game has infinite levels. Each level has 10 mole appearances.
* You must hit all 10 moles to proceed to the next level.
* Missing even 1 mole ends the game.
* The mole speed increases with each level.
* Your score and name are saved in a persistent leaderboard.

---

## Leaderboard Storage

Scores are stored locally in `leaderboard.bin` using Python's `pickle`. It records:

* High score per player
* Cumulative score across all sessions

---

## Notes

* If image or sound files are missing, an error popup with a download link appears.
* Works cross-platform as long as Python and dependencies are installed.
* You can change the assets and sounds to customize your version of the game.

---

## License

This project is free to use for personal or educational purposes.

