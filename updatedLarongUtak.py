import random
import string
import sys
from typing import List, Tuple, Dict, Optional
import platform

def get_password_with_asterisks(prompt="Password: "):
   """Get password from user showing asterisks while typing."""
   password = ""
   print(prompt, end='', flush=True)
   if platform.system() == 'Windows':
       import msvcrt
       while True:
           char = msvcrt.getch()
           char = char.decode('utf-8') if isinstance(char, bytes) else char
           if char == '\r' or char == '\n':  # Enter key
               print()
               break
           elif char == '\b':  # Backspace
               if password:
                   password = password[:-1]
                   print('\b \b', end='', flush=True)
           elif char.isprintable():
               password += char
               print('*', end='', flush=True)
   else:  # Unix-like
       import termios
       import tty
       fd = sys.stdin.fileno()
       old_settings = termios.tcgetattr(fd)
       try:
           tty.setraw(fd)
           while True:
               char = sys.stdin.read(1)
               if char == '\r' or char == '\n':  # Enter key
                   print()
                   break
               elif char == '\x7f':  # Backspace
                   if password:
                       password = password[:-1]
                       print('\b \b', end='', flush=True)
               elif char.isprintable():
                   password += char
                   print('*', end='', flush=True)
       finally:
           termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return password

# GLOBAL CONSTANTS
SHIFT_VAL = 7
PLAYERS_FILE = "players.txt"
HIGHSCORES_FILE = "highscores.txt"
COLORS = ["R", "G", "B", "Y", "W", "O"]
CODE_LENGTH = 4
SCORING = ["Scoring: 10 less than the no. of attempts", "If your number of attempts is 2, then your score is 8. If 6, then 4."]
GAME_MECHANICS = ["1️ The computer randomly generates a 4-color code.", "2️ You must guess the code using colors: R, G, B, Y, W, O.", "3️ After each guess, you'll get feedback:", "   - Black: Correct color in the correct position.", "   - White: Correct color but in the wrong position.", "4️ You have 10 attempts to guess the correct code.", "5️ Beat your best score and climb the leaderboard!"]

# --- HELPER FUNCTIONS ---
def generate_random_username(length: int = 6) -> str:
   """Generates a random username consisting of 3 lowercase letters and 3 digits."""
   letters = ''.join(random.choices(string.ascii_lowercase, k=3))
   numbers = ''.join(random.choices(string.digits, k=3))
   return letters + numbers

def caesar_encrypt(password: str, shift: int = SHIFT_VAL) -> str:
   """Implements a Caesar cipher for letters (A-Z, a-z) and digits (0-9)."""
   enc = []
   for ch in password:
       if ch.isalpha():
           base = ord("A") if ch.isupper() else ord("a")
           rotated = chr((ord(ch) - base + shift) % 26 + base)
           enc.append(rotated)
       elif ch.isdigit():
           rotated = chr((ord(ch) - ord("0") + shift) % 10 + ord("0"))
           enc.append(rotated)
       else:
           enc.append(ch)
   return "".join(enc)

def check_username_exists(username: str) -> bool:
   """Checks if a username exists in the players file."""
   try:
       with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
           for line in f:
               line = line.strip()
               if not line:
                   continue
               try:
                   user, _ = line.split(",", 1)
               except ValueError:
                   continue
               if user == username:
                   return True
       return False
   except FileNotFoundError:
       return False
   except IOError:
       return False

# --- NEW/MODIFIED ACCOUNT MANAGEMENT FUNCTIONS ---
def update_password_in_file(username: str, new_enc_pw: str) -> bool:
   """Updates the encrypted password for a specific user in the players file."""
   lines = []
   updated = False
   try:
       with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
           for line in f:
               line = line.strip()
               if not line:
                   lines.append("")
                   continue
               parts = line.split(",", 1)
               if len(parts) == 2 and parts[0] == username:
                   lines.append(f"{username},{new_enc_pw}")
                   updated = True
               else:
                   lines.append(line)
       if updated:
           with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
               f.write('\n'.join(lines) + '\n')
           return True
       return False
   except IOError as e:
       print(f"Error reading/writing database: {e}")
       return False

def forgot_password() -> None:
   """Handles the password reset process."""
   print("\n=== Forgot Password (Password Reset) ===")
   username = input("Enter your username: ").strip().lower()
   if not check_username_exists(username):
       print(f"User '{username}' not found.")
       return
   print(f"User '{username}' found. You can now reset your password.")
   while True:
       try:
           new_pw = get_password_with_asterisks("Enter your NEW password: ")
       except (KeyboardInterrupt, EOFError):
           print("\nPassword reset cancelled.")
           return
       if new_pw == "":
           print("Password cannot be empty.")
           continue
       enc_pw = caesar_encrypt(new_pw)
       if update_password_in_file(username, enc_pw):
           print("✅ Password successfully updated!")
           return
       else:
           print("❌ Error updating password. Please try again.")
           return

# Function which handles the user registration process
def register_user():
    """Handles the user registration process."""
    looped = 0 # used to determine if the loop has already been executed at least once;  used to determine if previous lines should be cleared
    print("\n=== User Registration ===")
    random_user = generate_random_username()
    print(f"Suggestion: Use '{random_user}'")
    input_error = False
    while True:

        if input_error == True:
            # Prompt to try again
            try_again = input('Do you want to try again? (If yes, enter Y. Otherwise, enter any key.): ').strip().upper()
            if try_again != 'Y':
                break # Exit the login loop
            else:
                print()

        registration_successful = False
        input_error = False
        # Enter username, strip white spaces, and convert to lowercase
        username = input('Enter desired username: ').strip().lower()


        #---- Unsuccessful username attempts -----
        if not username:
            print("Username cannot be empty.")
            input_error = True
            continue

        # Check if the username already exists using the check_username_exists() function
        if check_username_exists(username):
            print(f"Username '{username}' is already taken.")
            input_error = True
            continue

        #---- End of unsuccessful username attempts -----


        # Enter password using getpass for secrecy
        input_pw = get_password_with_asterisks("Enter your password: ")

        input_pw2 = get_password_with_asterisks("Re-enter your password: ")


        #---- Unsuccessful password attempts -----
        if input_pw != input_pw2:
            print("Passwords do not match.")
            input_error = True
            continue

        if not input_pw:
            print("Password cannot be empty.")
            input_error = True
            continue
        
        #---- End of unsuccessful password attempts -----


        # Encrypt the password using the caesar_encrypt() function
        encrypted_pw = caesar_encrypt(input_pw)

        print(f"Registration successful! Welcome, {username}!")
        registration_successful = True

        # Append the new user's details to the database
        try:
            with open(PLAYERS_FILE, 'a', encoding='utf-8') as players:
                players.write(f'{username},{encrypted_pw}\n')
            
        except IOError as e:
            print(f"An error occurred while writing to the database: {e}")
            break

        if registration_successful == True:
            return username #Return value after a successful registration



# Function to login existing users
def login_user():
    """Handles the user login process."""
    print("\n--- User Login ---")
    while True:
        # Enter username; strip white spaces and convert to lowercase
        input_username = input('Username: ').strip().lower()

        # Enter password using getpass for secrecy
        input_pw = get_password_with_asterisks('Password: ')

        user_found = False
        login_successful = False

        try:
            # Open database for player details (username and password).
            with open(PLAYERS_FILE, 'r', encoding='utf-8') as players:
                # Check every line in the opened players.txt file
                for line in players:
                    try:
                        user, enc_pw = line.strip().split(',')
                    except ValueError:
                        # Skip lines that don't conform to 'user,password' format
                        continue

                    # Check if the user matches with the input_user
                    if user == input_username:
                        user_found = True

                        # Check if the encrypted input_pw matches the stored enc_pw
                        if caesar_encrypt(input_pw) == enc_pw:
                            print(f'Login successful. Welcome back, {user}!')
                            login_successful = True
                            return user #Return value after a successful user login
                        else:
                            print('Incorrect password.')
                            print()

                        # Since the username has been found (or matched), break the inner loop
                        break

            if login_successful:
                break # Exit the login loop on success

            if not user_found:
                print('Username not found.')
                print()

            # Prompt to try again
            try_again = input('Do you want to try again? (Y/N): ').strip().upper()
            if try_again != 'Y':
                break # Exit the login loop
        
        except FileNotFoundError:
            print(f"Error: Database file '{PLAYERS_FILE}' not found. Please register first.")
            break
        except IOError as e:
            print(f"An error occurred while reading the database: {e}")
            break



# --- GAME LOGIC (Unchanged) ---
def generate_secret_code() -> List[str]:
   secret_code = []
   for i in range(1, CODE_LENGTH+1):
       secret_code.append(random.choice(COLORS))
   return secret_code

def parse_guess(raw: str) -> Optional[List[str]]:
   raw = raw.strip().upper()
   if not raw:
       return None
   for sep in [",", " "]:
       if sep in raw:
           parts = [p for p in (raw.replace(",", " ").split()) if p]
           if len(parts) != CODE_LENGTH:
               return None
           parts = [p[0] for p in parts]
           if all(p in COLORS for p in parts):
               return parts
           return None
   if len(raw) == CODE_LENGTH and all(ch in COLORS for ch in raw):
       return list(raw)
   return None

def score_guess(secret: List[str], guess: List[str]) -> Tuple[int, int]:
   black = sum(1 for s, g in zip(secret, guess) if s == g)
   secret_counts = {}
   guess_counts = {}
   for i in range(len(secret)):
       if secret[i] != guess[i]:
           secret_counts[secret[i]] = secret_counts.get(secret[i], 0) + 1
           guess_counts[guess[i]] = guess_counts.get(guess[i], 0) + 1
   white = 0
   for color, cnt in guess_counts.items():
       white += min(cnt, secret_counts.get(color, 0))
   return black, white

def play_game(username: str) -> Tuple[int, bool]:
   secret = generate_secret_code()
   print("\n=== Mastermind: Guess the 4-color code ===")
   print(f"Colors: {', '.join(COLORS)} (use letters). Code length: {CODE_LENGTH}.")
   print(f"You have 10 attempts. Repeats allowed.")
   attempts_used = 0
   while True:
        raw = input(f"\nAttempt {attempts_used+1}/10 - Enter your guess: ")
        guess = parse_guess(raw)
        if guess is None:
            print(f"\nInvalid guess. Enter {CODE_LENGTH} colors using letters from {COLORS}.")
            continue
        attempts_used += 1
        black, white = score_guess(secret, guess)
        print(f"Feedback -> Black: {black}, White: {white}")
        if black == CODE_LENGTH:
            print("\nYou Win! 🎉")
            return attempts_used
        elif attempts_used == 10:
            print("\nGame Over! Code was: " + "".join(secret))
            return False



# --- LEADERBOARD LOGIC (Unchanged) ---
def load_highscores() -> Dict[str, int]:
   scores = {}
   try:
       with open(HIGHSCORES_FILE, "r", encoding="utf-8") as f:
           for line in f:
               line = line.strip()
               if not line:
                   continue
               try:
                   user, s = line.split(",", 1)
                   scores[user] = int(s)
               except ValueError:
                   continue
   except FileNotFoundError:
       pass
   except IOError:
       pass
   return scores

def save_highscores(scores: Dict[str, int]) -> None:
   try:
       with open(HIGHSCORES_FILE, "w", encoding="utf-8") as f:
           for user, score in scores.items():
               if user == 
               f.write(f"{user},{s}\n")
   except IOError as e:
       print(f"Error writing highscores: {e}")

def update_leaderboard(username: str, score: int) -> None:
   scores = load_highscores()
   prev = scores.get(username)
   if prev is None or score < prev:
       scores[username] = score
       save_highscores(scores)
       if prev is None:
           print(f"New highscore added for {username}: {score}")
       else:
           print(f"Highscore improved for {username}: {prev} -> {score}")
   else:
       print(f"No leaderboard update: {username}'s best is {prev}, your score was {score}")

def display_top5() -> None:
   scores = load_highscores()
   if not scores:
       print("No highscores yet.")
       return
   sorted_scores = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))
   print("\n=== Top 5 Players ===")
   for i, (user, s) in enumerate(sorted_scores[:5], start=1):
       print(f"{i}. {user} - {s}")
   print("=====================")


#----- GAME MECHANICS ------
def game_mech():
    print("========================================")
    print("WELCOME TO THE MASTERMIND GAME")
    print("========================================")
    for i in range(len(GAME_MECHANICS)):
        print(GAME_MECHANICS[i])

    for i in range(len(SCORING)):
        print(SCORING[i])

    print("========================================")

# --- MAIN MENU (Modified) ---
def main_menu() -> None:
   """Displays the main menu and handles user choices."""
   game_mech()
   while True:
       print("\nMain Menu")
       print("[R] Register")
       print("[L] Login & Play")
       print("[F] Forgot Password")
       print("[E] Exit")
       choice = input("Your choice: ").strip().upper()
       if choice == "R":
            success, username = register_user()
            if success:
               attempts = play_game(username)
               score = 10 - attempts
               update_leaderboard(username, score)
               display_top5()
       elif choice == "L":
           success, username = login_user()
           if success:
               attempts = play_game(username)
               score = 10 - attempts
               update_leaderboard(username, score)
               display_top5()
       elif choice == "F":
           forgot_password()
       elif choice == "E":
           print("Exiting application. Goodbye! 👋")
           break
       else:
           print("Invalid choice. Please enter R, L, F, or E.")

if __name__ == "__main__":
   try:
       main_menu()
   except KeyboardInterrupt:
       print("\nInterrupted. Goodbye! 👋")
       sys.exit(0)
