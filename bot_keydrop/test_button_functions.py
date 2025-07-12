import tkinter as tk
from unittest import mock

# Import the GUI from the existing simple app
from test_app_simple import KeydropBotGUI


def run_button_tests():
    """Instantiate the GUI and invoke each button callback."""
    # Ensure Tk uses a virtual display
    root = tk.Tk()
    root.withdraw()  # Hide main window
    app = KeydropBotGUI()
    app.root = root  # use our hidden root

    with mock.patch('tkinter.messagebox.showinfo') as info, \
         mock.patch('tkinter.messagebox.showwarning') as warning, \
         mock.patch('tkinter.messagebox.askyesno', return_value=True):
        app.start_automation()
        app.stop_automation()
        app.emergency_stop()

    root.destroy()
    print("All button callbacks executed successfully")


if __name__ == "__main__":
    run_button_tests()
