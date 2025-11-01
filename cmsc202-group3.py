#this is the workspace for mastermind project

from getpass import getpass
import sys

# Start the Program
# Show game mechanics

shift_val = 7
FILENAME = 'players.txt' # Define the database filename for easy reuse
auth_username = ''


#---------------Define functions----------------
#Function used to clear n previous lines
def clear_lines(n=1):
    """Clears the previous n lines in the terminal."""
    for _ in range(n):
        # Move cursor up one line
        sys.stdout.write('\033[F')
        # Clear the entire line
        sys.stdout.write('\033[K')
    sys.stdout.flush()

# Function to 'encrypt' a password using Caesar's Cipher
def caesar_encrypt(password, shift=shift_val):
    """Encrypts the password using Caesar's Cipher with a fixed shift value."""
    enc_pw = ''

    for char in password:
        # Check if the current char is an alphabet
        if char.isalpha():
            # Set the order of the base character starting from 'A' (65) or 'a' (97)
            base_char = ord('A') if char.isupper() else ord('a')

            # Formula for character rotation (A-Z or a-z)
            enc_pw += chr((ord(char) - base_char + shift) % 26 + base_char)

        # Check if the current char is a digit
        elif char.isdigit():
            # Formula for digit rotation (0-9)
            enc_pw += chr((ord(char) - ord('0') + shift) % 10 + ord('0'))

        else:
            # Special characters are skipped and not encrypted
            enc_pw += char

    return enc_pw

#Function to check if a username already exists in the database
def check_username_exists(username):
    """Checks if a username already exists in the database."""
    try:
        with open(FILENAME, 'r', encoding='utf-8') as players:
            for line in players:
                user, _ = line.strip().split(',')
                if user == username:
                    return True
        return False
    except FileNotFoundError:
        # If the file doesn't exist, no users exist yet.
        return False
    except ValueError:
        # Handle lines that might be improperly formatted
        print("Warning: The database file contains an invalid entry.")
        return False
    except IOError as e:
        print(f"An error occurred while reading the database: {e}")
        return False


# Function which handles the user registration process
def register_user():
    """Handles the user registration process."""
    looped = 0 # used to determine if the loop has already been executed at least once;  used to determine if previous lines should be cleared
    print("\n--- User Registration ---")
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
        input_username = input('Enter desired username: ').strip().lower()


        #---- Unsuccessful username attempts -----
        if not input_username:
            print("Username cannot be empty.")
            input_error = True
            continue

        # Check if the username already exists using the check_username_exists() function
        if check_username_exists(input_username):
            print(f"Username '{input_username}' is already taken.")
            input_error = True
            continue

        #---- End of unsuccessful username attempts -----


        # Enter password using getpass for secrecy
        input_pw = getpass('Enter your password: ')

        input_pw2 = getpass('Re-type password: ')


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

        print(f"Registration successful! Welcome, {input_username}!")
        registration_successful = True

        # Append the new user's details to the database
        try:
            with open(FILENAME, 'a', encoding='utf-8') as players:
                players.write(f'{input_username},{encrypted_pw}\n')
            
        except IOError as e:
            print(f"An error occurred while writing to the database: {e}")
            break

        if registration_successful == True:
            return input_username #Return value after a successful registration


# Function to login existing users
def login_user():
    """Handles the user login process."""
    print("\n--- User Login ---")
    while True:
        # Enter username; strip white spaces and convert to lowercase
        input_username = input('Username: ').strip().lower()

        # Enter password using getpass for secrecy
        input_pw = getpass('Password: ')

        user_found = False
        login_successful = False

        try:
            # Open database for player details (username and password).
            with open(FILENAME, 'r', encoding='utf-8') as players:
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
            print(f"Error: Database file '{FILENAME}' not found. Please register first.")
            break
        except IOError as e:
            print(f"An error occurred while reading the database: {e}")
            break

# ----------------------------------------------------------------------

## Main Application Loop

def main_app():
    """The main application loop for registration and login."""
    while True:
        print("\n==============================")
        print("Choose an option:")
        print("  [R] Register")
        print("  [L] Login")
        print("  [E] Exit")
        print("==============================")

        choice = input('Your choice: ').strip().upper()

        if choice == 'R':
            auth_username = register_user()
            if auth_username != '':
                print(f'\nShowing game mechanics for {auth_username}...')
                break
        elif choice == 'L':
            auth_username = login_user()
            if auth_username != '':
                print(f'\nShowing game mechanics for {auth_username}...')
                break
        elif choice == 'E':
            print("Exiting application. Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter R, L, or E.")


if __name__ == "__main__":
    main_app()

