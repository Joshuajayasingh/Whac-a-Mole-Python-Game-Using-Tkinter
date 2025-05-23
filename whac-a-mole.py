import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser
import sys
import random
import pickle
import pygame

def play_background_music():
    pygame.mixer.music.load('theme.wav')
    pygame.mixer.music.play(-1)

def stop_background_music():
    pygame.mixer.music.stop()
def open_link(event):
    webbrowser.open("https://drive.google.com/drive/folders/14k5J8jKl5MqXV1a7fVO2uFpHjWntE4Tm?usp=sharing")

def show_error_message():
    error_window = tk.Toplevel()
    error_window.title("File Not Found")
    error_window.geometry("400x200")

    message = tk.Label(error_window, text="Required image files were not found. Download them from:", font=("Arial", 12))
    message.pack(pady=10)

    link = tk.Label(error_window, text="Google Drive", font=("Arial", 12), fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", open_link)

    def close_and_exit():
        error_window.destroy()
        sys.exit()

    close_button = ttk.Button(error_window, text="Close", command=close_and_exit)
    close_button.pack(pady=10)
    error_window.protocol("WM_DELETE_WINDOW", close_and_exit)

def save_score(name, score):
    try:
        with open('leaderboard.bin', 'rb') as file:
            leaderboard = pickle.load(file)
            if type(leaderboard) is not dict:
                leaderboard = {}
    except (FileNotFoundError, EOFError):
        leaderboard = {}

    if name in leaderboard:
        leaderboard[name]['cumulative_score'] += score
        if score > leaderboard[name]['high_score']:
            leaderboard[name]['high_score'] = score
    else:
        leaderboard[name] = {
            'high_score': score,
            'cumulative_score': score
        }

    with open('leaderboard.bin', 'wb') as file:
        pickle.dump(leaderboard, file)


def get_leaderboard():
    try:
        with open('leaderboard.bin', 'rb') as file:
            leaderboard = pickle.load(file)
    except (FileNotFoundError, EOFError):
        leaderboard = {}
    leaderboard_list = sorted(leaderboard.items(), key=lambda x: x[1]['high_score'], reverse=True)
    return leaderboard_list[:10]

def setup():
    with open('whack_a_mole.dat', 'ab'):
        pass

def create_home_page():
    home_frame.pack(fill="both", expand=True)
    home_canvas.pack(fill="both", expand=True)
    home_canvas.create_image(0, 0, anchor="nw", image=background_image)

    title_label = tk.Label(home_canvas, text="Whack-A-Mole Game", font=("Arial", 24), bg="#37ff37")
    home_canvas.create_window(400, 100, window=title_label)

    start_button = tk.Button(home_canvas, text="Start Game", command=ask_for_name)
    home_canvas.create_window(400, 300, window=start_button)

    leaderboard_button = tk.Button(home_canvas, text="Leaderboard", command=show_leaderboard)
    home_canvas.create_window(400, 350, window=leaderboard_button)

    rules_button = tk.Button(home_canvas, text="How To Play The Game", command=show_rules)
    home_canvas.create_window(400, 400, window=rules_button)

def reset_game():
    global level, score, mole_speed, total_points_per_level, current_points, mole_hit, tries, last_position
    level = 1
    score = 0
    mole_speed = 2000
    total_points_per_level = 10
    current_points = 0
    mole_hit = False
    tries = 0
    last_position = None

def ask_for_name():
    name_window = tk.Toplevel(root)
    name_window.title("Enter Your Name")
    name_window.geometry("300x150")
    name_window.grab_set() 
    name_label = tk.Label(name_window, text="Enter your name:", font=("Arial", 14))
    name_label.pack(pady=10)

    name_entry = tk.Entry(name_window, font=("Arial", 14))
    name_entry.pack(pady=5)

    def submit_name():
        global player_name
        entered_name = name_entry.get().strip()
        if entered_name:
            player_name = entered_name
        else:
            player_name = "Player"
        name_window.destroy()
        start_game()

    submit_button = tk.Button(name_window, text="Start Game", command=submit_name)
    submit_button.pack(pady=10)

    name_window.protocol("WM_DELETE_WINDOW", submit_name)
def start_game():
    global game_frame, score_label, level_label, mole_label
    pygame.mixer.music.pause()
    reset_game()
 
    home_frame.pack_forget()
    home_canvas.pack_forget()
    game_frame.pack(fill="both", expand=True)
    game_canvas.pack(fill="both", expand=True)
    game_canvas.create_image(0, 0, anchor="nw", image=background_image)

    score_label.config(text=f"Score: {score}")
    game_canvas.create_window(100, 20, window=score_label)

    level_label.config(text=f"Level: {level}")
    game_canvas.create_window(700, 20, window=level_label)

    mole_canvas.create_image(0, 0, anchor="nw", image=mole_positions_image)
    game_canvas.create_window(400, 350, window=mole_canvas)

    mole_label.bind("<Button-1>", whack_mole)
    next_mole()

def next_mole():
    global mole_hit, tries, last_position, new_position
    if current_points >= total_points_per_level:
        level_up()
        return

    if tries >= 10:
        end_game()
        return

    mole_hit = False
    tries += 1
    new_position = random.choice(mole_positions)
    while new_position == last_position:
        new_position = random.choice(mole_positions)

    last_position = new_position
    x1, y1, x2, y2 = new_position
    mole_label.place(x=x1 + (x2 - x1 - 90) // 2, y=y1 + (y2 - y1 - 90) // 2)
    root.after(mole_speed, next_mole)

def whack_mole(event):
    global mole_hit, score, current_points
    if not mole_hit:
        score += 1
        current_points += 1
        score_label.config(text=f"Score: {score}")
        mole_hit = True
        if hit_sound:
            hit_sound.play()

def level_up():
    global level, current_points, mole_speed, tries
    level += 1
    current_points = 0
    mole_speed = int(mole_speed * 0.9)
    tries = 0
    level_label.config(text=f"Level: {level}")
    next_mole()

def show_leaderboard():
    global leaderboard_frame, leaderboard_label, back_button, leaderboard
    home_frame.pack_forget()
    home_canvas.pack_forget()
    leaderboard_frame = tk.Frame(root)
    leaderboard_frame.pack(fill="both", expand=True)
    leaderboard_canvas = tk.Canvas(leaderboard_frame, width=800, height=600)
    leaderboard_canvas.pack(fill="both", expand=True)
    leaderboard_canvas.create_image(0, 0, anchor="nw", image=background_image)
    leaderboard_label = tk.Label(leaderboard_frame, text="Leaderboard", font=("Arial", 24), bg="green")
    leaderboard_canvas.create_window(400, 50, window=leaderboard_label)
    leaderboard = get_leaderboard()
    if leaderboard:
        for i, (name, scores) in enumerate(leaderboard):
            score_text = f"{i+1}. {name} - High Score: {scores['high_score']}, Cumulative Score: {scores['cumulative_score']}"
            score_label = tk.Label(leaderboard_frame, text=score_text, font=("Arial", 14), bg="green")
            leaderboard_canvas.create_window(400, 100 + i * 30, window=score_label)
    else:
        messagebox.showinfo("No scores available!", "Play at least one game to view the leaderboard.")
        back_to_home()
    back_button = tk.Button(leaderboard_frame, text="Back", command=back_to_home)
    leaderboard_canvas.create_window(400, 550, window=back_button)

def back_to_home():
    if 'leaderboard_frame' in globals():
        leaderboard_frame.pack_forget()
    if 'rules_frame' in globals():
        rules_frame.pack_forget()
    if 'game_frame' in globals():
        game_frame.pack_forget()
    create_home_page()

def end_game():
    save_score(player_name, score)
    game_frame.pack_forget()

    create_home_page()
    if die_sound:
        die_sound.play()
    messagebox.showinfo("Game Over", f"Game over! Your score: {score}")
    pygame.mixer.music.unpause()

def show_rules():
    home_frame.pack_forget()
    home_canvas.pack_forget()
    rules_frame = tk.Frame(root)
    rules_frame.pack(fill="both", expand=True)
    rules_canvas = tk.Canvas(rules_frame, width=800, height=600)
    rules_canvas.pack(fill="both", expand=True)
    rules_canvas.create_image(0, 0, anchor="nw", image=background_image)

    rules_text = """
    There are an infinite number of levels in this game. Each level has 10 points.
    If you miss even 1 point in a single level, you will lose that level, and your
    points up till that level will be counted. To move up a level, you have to clear
    all 10 points of the previous level, and then you will automatically be moved on
    to the next level. The mole gets faster with each consecutive level. The leaderboard
    will display the scores of the top 10 players, and also only the top score of each player.
    """
    rules_label = tk.Label(rules_canvas, text=rules_text, font=("Arial", 14), justify="center", wraplength=800, bg="#37ff37")
    rules_canvas.create_window(400, 200, window=rules_label)

    back_button = tk.Button(rules_canvas, text="Back", command=back_to_home)
    rules_canvas.create_window(400, 550, window=back_button)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    image_files_missing = False
    mole_positions = [
        (50, 50, 130, 130), (200, 50, 280, 130), (350, 50, 430, 130),
        (50, 200, 130, 280), (200, 200, 280, 280), (350, 200, 430, 280),
        (50, 350, 130, 430), (200, 350, 280, 430), (350, 350, 430, 430)
    ]
    pygame.mixer.init()

    a = "whacs.jpg"  
    b = "whacs.jpg" 
    c = "moles.png"   

    try:
        background_image = ImageTk.PhotoImage(Image.open(a).resize((800, 800), Image.Resampling.LANCZOS))
        mole_positions_image = ImageTk.PhotoImage(Image.open(b).resize((500, 500), Image.Resampling.LANCZOS))
        mole_image = ImageTk.PhotoImage(Image.open(c).resize((90, 90), Image.Resampling.LANCZOS))
        hit_sound = pygame.mixer.Sound('hit.wav')
        die_sound = pygame.mixer.Sound('lost.wav')
    except FileNotFoundError:
        image_files_missing = True
        background_image = None
        mole_positions_image = None
        mole_image = None
        hit_sound = None
        die_sound = None

    if image_files_missing:
        show_error_message()
    else:
        root.deiconify() 

        home_frame = tk.Frame(root)
        game_frame = tk.Frame(root)
        leaderboard_frame = tk.Frame(root)
        rules_frame = tk.Frame(root)

        home_canvas = tk.Canvas(home_frame, width=800, height=600)
        game_canvas = tk.Canvas(game_frame, width=800, height=600)
        leaderboard_canvas = tk.Canvas(leaderboard_frame, width=800, height=600)
        rules_canvas = tk.Canvas(rules_frame, width=800, height=600)

        score_label = tk.Label(game_canvas, text="Score: 0", bg="green", font=("Arial", 14))
        level_label = tk.Label(game_canvas, text="Level: 1", bg="green", font=("Arial", 14))

        mole_canvas = tk.Canvas(game_canvas, width=500, height=500, bg="green")
        for x1, y1, x2, y2 in mole_positions:
            mole_canvas.create_oval(x1, y1, x2, y2, fill="#0000ff", width=10)
        mole_label = tk.Label(mole_canvas, image=mole_image, bd=0, cursor='target', background='green')
        create_home_page()

        play_background_music()

        root.protocol("WM_DELETE_WINDOW", lambda: (stop_background_music(), root.destroy()))

    root.mainloop()