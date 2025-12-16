from tkinter import *
from PIL import Image, ImageTk
from random import randint

# --- 1. CONFIGURATION CONSTANTS (THEME & STYLE) ---
BG_COLOR = "#2C3E50"  # Dark Slate Blue (Background)
HEADER_COLOR = "#34495E" # Darker Gray-Blue (Headers/Frames)
TEXT_COLOR = "#ECF0F1"  # Off-White (Primary Text)
ACCENT_COLOR = "#F39C12" # Orange (Accent/Indicator)
WIN_COLOR = "#2ECC71"    # Green
LOSE_COLOR = "#E74C3C"   # Red

FONT_FAMILY = "Segoe UI" # Modern, readable font (or change to "Arial" if Segoe is unavailable)
HEADER_FONT = (FONT_FAMILY, 20, "bold")
SCORE_FONT = (FONT_FAMILY, 48, "bold")
MESSAGE_FONT = (FONT_FAMILY, 24, "italic")
BUTTON_FONT = (FONT_FAMILY, 14, "bold")


# --- 2. INITIALIZE WINDOW ---
window = Tk()
window.title("Rock Paper Scissor")
window.configure(background=BG_COLOR)


# --- 3. IMAGE LOADING (Must be done carefully for Tkinter) ---
# NOTE: Ensure your "Rock 1.png", "Paper 1.png", etc., files exist in the same directory.
try:
    # Open images (assuming they are scaled to a good size, e.g., 128x128)
    img_rock1 = Image.open("Rock 1.png")
    img_paper1 = Image.open("Paper 1.png")
    img_scissor1 = Image.open("Scissor 1.png")
    img_rock2 = Image.open("Rock 1 (2).png")
    img_paper2 = Image.open("Paper 1 (2).png")
    img_scissor2 = Image.open("Scissor 1 (2).png")

    # Convert to Tkinter PhotoImage objects
    player_images = {
        "rock": ImageTk.PhotoImage(img_rock1),
        "paper": ImageTk.PhotoImage(img_paper1),
        "scissor": ImageTk.PhotoImage(img_scissor1),
    }

    computer_images = {
        "rock": ImageTk.PhotoImage(img_rock2),
        "paper": ImageTk.PhotoImage(img_paper2),
        "scissor": ImageTk.PhotoImage(img_scissor2),
    }
except FileNotFoundError:
    print("Image files not found. Please ensure images are correctly named and in the same directory.")
    # Fallback to simple placeholder if images fail to load
    player_images = {"rock": None, "paper": None, "scissor": None}
    computer_images = {"rock": None, "paper": None, "scissor": None}


# --- 4. LAYOUT WITH FRAMES ---
window.grid_columnconfigure(0, weight=1) # Center the main frame

# Main container frame
main_frame = Frame(window, bg=BG_COLOR, padx=30, pady=30)
main_frame.grid(row=0, column=0, sticky="nsew")

# Score and Indicator Frame (Row 0 inside main_frame)
score_frame = Frame(main_frame, bg=BG_COLOR)
score_frame.grid(row=0, column=0, columnspan=5, pady=20)
score_frame.grid_columnconfigure((0, 4), weight=1) # Push elements to center


# --- 5. SCORE AND INDICATOR WIDGETS ---

# Player Indicator
player_indicator = Label(score_frame, text="PLAYER", font=HEADER_FONT, bg=ACCENT_COLOR, fg=BG_COLOR, padx=10, pady=5)
player_indicator.grid(row=0, column=3, padx=(20, 5))

# Player Score
player_score = Label(score_frame, text="0", font=SCORE_FONT, fg=TEXT_COLOR, bg=BG_COLOR, width=3)
player_score.grid(row=1, column=3, padx=(20, 5))

# Computer Score
computer_score = Label(score_frame, text="0", font=SCORE_FONT, fg=TEXT_COLOR, bg=BG_COLOR, width=3)
computer_score.grid(row=1, column=1, padx=(5, 20))

# Computer Indicator
computer_indicator = Label(score_frame, text="COMPUTER", font=HEADER_FONT, bg=ACCENT_COLOR, fg=BG_COLOR, padx=10, pady=5)
computer_indicator.grid(row=0, column=1, padx=(5, 20))

# Separator Label
separator = Label(score_frame, text=":", font=SCORE_FONT, fg=TEXT_COLOR, bg=BG_COLOR)
separator.grid(row=1, column=2, padx=10)


# --- 6. CHOICES DISPLAY WIDGETS ---

# Choices Frame (Row 1 inside main_frame)
choices_frame = Frame(main_frame, bg=HEADER_COLOR, padx=50, pady=20)
choices_frame.grid(row=1, column=0, columnspan=5, pady=20)
choices_frame.grid_columnconfigure((0, 2), weight=1) # For centering

# Computer Choice Display
# Start with a default image (or rock/scissor as you had)
initial_img_c = computer_images.get("scissor") 
label_computer = Label(choices_frame, image=initial_img_c, bg=HEADER_COLOR)
label_computer.grid(row=0, column=0, padx=40)

# Player Choice Display
initial_img_p = player_images.get("scissor")
label_player = Label(choices_frame, image=initial_img_p, bg=HEADER_COLOR)
label_player.grid(row=0, column=2, padx=40)

# VS Label
vs_label = Label(choices_frame, text="VS", font=SCORE_FONT, fg=ACCENT_COLOR, bg=HEADER_COLOR)
vs_label.grid(row=0, column=1)


# --- 7. BUTTONS AND MESSAGE FRAME ---

# Button Frame (Row 2 inside main_frame)
button_frame = Frame(main_frame, bg=BG_COLOR)
button_frame.grid(row=2, column=0, columnspan=5, pady=30)

# Message Label (Row 3 inside main_frame, spans columns)
final_message = Label(main_frame, font=MESSAGE_FONT, bg=BG_COLOR, fg=TEXT_COLOR, text="Make your move!")
final_message.grid(row=3, column=0, columnspan=5)


# --- 8. GAME LOGIC FUNCTIONS ---
choices = ["rock", "paper", "scissor"]

def updateMessage(msg, color=TEXT_COLOR):
    """Updates the message label text and color."""
    final_message.config(text=msg, fg=color)

def Computer_Update():
    """Increments computer's score and updates display."""
    current = int(computer_score.cget("text"))
    computer_score.config(text=str(current + 1))

def Player_Update():
    """Increments player's score and updates display."""
    current = int(player_score.cget("text"))
    player_score.config(text=str(current + 1))

def winner_check(p, c):
    """Checks the winner and updates scores/message."""
    if p == c:
        updateMessage("It's a TIE!", TEXT_COLOR)
    elif (p == "rock" and c == "scissor") or \
         (p == "paper" and c == "rock") or \
         (p == "scissor" and c == "paper"):
        updateMessage("Player WINS!", WIN_COLOR)
        Player_Update()
    else:
        updateMessage("Computer WINS!", LOSE_COLOR)
        Computer_Update()

def choice_update(player_choice):
    """Handles the player's choice, determines computer's choice, and checks winner."""
    choice_computer = choices[randint(0, 2)]

    # Update images using the dictionary lookup (cleaner and robust)
    label_computer.config(image=computer_images.get(choice_computer))
    label_player.config(image=player_images.get(player_choice))

    winner_check(player_choice, choice_computer)

# --- 9. BUTTON WIDGETS ---
button_rock = Button(button_frame, text="ROCK", font=BUTTON_FONT, bg=ACCENT_COLOR, fg=BG_COLOR,
                     width=12, pady=10, command=lambda: choice_update("rock"))
button_rock.grid(row=0, column=0, padx=10)

button_paper = Button(button_frame, text="PAPER", font=BUTTON_FONT, bg=ACCENT_COLOR, fg=BG_COLOR,
                      width=12, pady=10, command=lambda: choice_update("paper"))
button_paper.grid(row=0, column=1, padx=10)

button_scissor = Button(button_frame, text="SCISSOR", font=BUTTON_FONT, bg=ACCENT_COLOR, fg=BG_COLOR,
                        width=12, pady=10, command=lambda: choice_update("scissor"))
button_scissor.grid(row=0, column=2, padx=10)


# --- 10. RUN THE APPLICATION ---
window.mainloop()