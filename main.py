import threading, time, keyboard, pyautogui as pag, customtkinter as ct

# Flag to control the execution of the main function
main_function_paused = False
exit_program = False

root = ct.CTk()


def closed():
    global exit_program

    root.destroy()
    exit_program = True


def ui_init():
    ct.set_appearance_mode("dark")
    ct.set_default_color_theme("dark-blue")

    root.geometry("800x600")
    root.title("Albion Gathering Bot")


    frame = ct.CTkFrame(master=root)
    frame.pack(padx=60, pady=20, fill="both", expand=True)

    label = ct.CTkLabel(master=frame, text="Albion Gathering Bot", font=("Arial", 24))
    label.pack(padx=10, pady=12)

    root.protocol("WM_DELETE_WINDOW", closed)
    root.mainloop()
    

def main_function():
    """Main function running in a loop."""
    global main_function_paused
    while not exit_program:
        if not main_function_paused:
            print("Main function is running...")
            # Simulate some work being done
            time.sleep(1)  # Sleep for 1 second in each iteration
        else:
            print("Main function is paused.")
            time.sleep(1)  # Sleep for a bit while paused


def secondary_function():
    """Function called every 30 minutes to pause main function."""
    global main_function_paused
    while not exit_program:
        time.sleep(30 * 60)  # Sleep for 30 minutes (30 * 60 seconds)
        main_function_paused = True
        print("Secondary function is running (pausing main function)...")
        # Simulate some work in the secondary function
        time.sleep(10)  # Simulate that the secondary function takes 10 seconds
        main_function_paused = False
        print("Secondary function is finished (resuming main function).")


def listen_for_exit():
    """Function to listen for 'esc' key press to exit the program."""
    global exit_program
    while not exit_program:
        if keyboard.is_pressed("esc"):
            print("Exit key pressed. Exiting...")
            exit_program = True
            break
        time.sleep(.1)  # Check every 100ms for the key press


# Start the main function in a separate thread
main_thread = threading.Thread(target=main_function)
main_thread.daemon = True
main_thread.start()

# Start the secondary function in a separate thread
secondary_thread = threading.Thread(target=secondary_function)
secondary_thread.daemon = True
secondary_thread.start()

ui_thread = threading.Thread(target=ui_init)
ui_thread.daemon = True

# Start the keyboard listener in the main thread
listen_for_exit()

# Wait for threads to finish (this will only happen when 'esc' is pressed)
main_thread.join()
secondary_thread.join()
ui_thread.join()

print("Program has exited.")
