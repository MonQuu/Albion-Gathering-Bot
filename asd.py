import threading
import time
import keyboard
import customtkinter as ct
import sys
import pyautogui

# Global flags
main_function_paused = False
exit_program = False

root = ct.CTk()

X1entry = None
Y1entry = None

X2entry = None
Y2entry = None

foodCounter = 0

coords = []  # Global variable to store coordinate pairs


def closed():
    """Callback function to handle the UI window close event."""
    global exit_program
    exit_program = True
    root.destroy()  # Break the mainloop and end the program


def display_mouse_coordinates():
    """Displays the current mouse coordinates in real time."""
    while not exit_program:
        x, y = pyautogui.position()
        print(f"Current Mouse Position: X={x}, Y={int(y)}", end="\r")  # The '\r' ensures it overwrites the same line.
        time.sleep(0.1)  # Refresh rate of 100ms



def click_coordinates(x, y):
    """Perform a mouse click at the given x, y coordinates."""
    try:
        x, y = int(x), int(y)  # Convert coordinates to integers
        pyautogui.moveTo(x, y)
        pyautogui.click()
        print(f"Clicked at coordinates: ({x}, {y})")
    except ValueError:
        print("Invalid coordinates, cannot click.")


def run_bot():
    """Callback for the runButton to initiate clicking at entered coordinates."""
    global main_function_paused
    main_function_paused = False  # Unpause the main function

    x1 = X1entry.get()
    y1 = Y1entry.get()
    x2 = X2entry.get()
    y2 = Y2entry.get()

    # Store the coordinates globally so they can be accessed in the main_function
    global coords
    coords = [(x1, y1), (x2, y2)]  # List of (X, Y) coordinate pairs to click on
    print(f"Coordinates set: {coords}")


def ui_init():
    global X1entry, Y1entry, X2entry, Y2entry, intervals
    """Initialize the customtkinter UI."""
    ct.set_appearance_mode("dark")
    ct.set_default_color_theme("dark-blue")

    root.geometry("800x600")
    root.title("Albion Gathering Bot")

    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure((2, 3), weight=0)

    frame = ct.CTkFrame(master=root)
    frame.pack(padx=60, pady=20, fill="both", expand=True)

    label = ct.CTkLabel(master=frame, text="Albion Gathering Bot", font=("Arial", 24))
    label.pack(padx=10, pady=12)

    X1entry = ct.CTkEntry(master=frame, placeholder_text="X coord of stone 1 (int)")
    Y1entry = ct.CTkEntry(master=frame, placeholder_text="Y coord of stone 1 (int)")

    X2entry = ct.CTkEntry(master=frame, placeholder_text="X coord of stone 2 (int)")
    Y2entry = ct.CTkEntry(master=frame, placeholder_text="Y coord of stone 2 (int)")

    X1entry.pack(padx=5, pady=6)
    Y1entry.pack(padx=5, pady=6)
    X2entry.pack(padx=5, pady=6)
    Y2entry.pack(padx=5, pady=6)

#---------------------------------------------------------------------------------------
    # Set the runButton to call the run_bot function when pressed
    runButton = ct.CTkButton(master=frame, text="Start the bot", command=run_bot)
    runButton.pack(padx=10, pady=12)

    root.protocol("WM_DELETE_WINDOW", closed)
    root.mainloop()


def main_function():
    """Main function that runs in a loop unless paused or exited."""
    global main_function_paused, exit_program, coords, intervals

    coords = []  # Initialize an empty list to hold the coordinates

    while not exit_program:
        if main_function_paused or not coords:
            time.sleep(1)  # Sleep while paused or no coordinates entered
            continue

        # Click on each coordinate pair in the coords list
        for x, y in coords:
            click_coordinates(x, y)  # Now clicking (X, Y) pairs correctly
            time.sleep(3)  # Add a delay between each click (adjust as needed)

        print("Clicking cycle completed, waiting before the next cycle...")
        time.sleep(3)  # Add a delay between clicking cycles (adjust as needed)


def secondary_function():
    """Function to pause the main function every 30 minutes for 10 seconds."""
    global main_function_paused, exit_program, foodCounter

    while not exit_program:
        time.sleep(30 * 60)  # Wait for 30 minutes
        if exit_program:  # Check for exit condition
            break
        main_function_paused = True
        print("Pausing main function for 10 seconds...")
        # -
        time.sleep(1)  # Pause for 10 seconds
        pyautogui.press("2")

        time.sleep(10)
        # -
        main_function_paused = False
        print("Resuming main function...")


def listen_for_exit():
    """Listen for 'esc' key press to trigger program exit."""
    global exit_program

    while not exit_program:
        if keyboard.is_pressed("esc"):
            print("Exit key pressed. Exiting...")
            exit_program = True
            root.destroy()  # End the UI loop and exit
            break
        time.sleep(0.05)  # Check more frequently with less sleep


if __name__ == "__main__":
    # Launch the main function in a separate thread
    main_thread = threading.Thread(target=main_function, daemon=True)
    main_thread.start()

    # Launch the secondary function in a separate thread
    secondary_thread = threading.Thread(target=secondary_function, daemon=True)
    secondary_thread.start()

    # Launch the keyboard listener in a separate thread
    listen_thread = threading.Thread(target=listen_for_exit, daemon=True)
    listen_thread.start()

    # Launch the mouse coordinate display in a separate thread
    mouse_coord_thread = threading.Thread(target=display_mouse_coordinates, daemon=True)
    mouse_coord_thread.start()

    # Initialize the UI (runs in the main thread and blocks until closed)
    ui_init()

    # Ensure the program exits cleanly after UI is closed
    print("Waiting for threads to finish...")
    main_thread.join()
    secondary_thread.join()
    listen_thread.join()
    mouse_coord_thread.join()

    # Fully exit the program
    print("Program has exited.")
    sys.exit()
