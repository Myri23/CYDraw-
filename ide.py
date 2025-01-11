# Import required modules:
import customtkinter as ct         # CustomTkinter library for enhanced UI components.
from customtkinter import CTkTextbox  # CTkTextbox widget for customizable text input areas.
from tkinter import *             # Standard Tkinter library for GUI components.
from tkinter import messagebox, filedialog  # Specific Tkinter widgets for dialog boxes and file operations.
import subprocess                 # For running external commands or processes.
import re                         # Regular expressions for text pattern matching and validation.
 
 
# Create the main application window:
window = Tk()                             # Initialize the main Tkinter window.
window.geometry('900x590')                # Set the initial size of the window (width=900, height=590).
window.minsize(width=900, height=600)     # Define the minimum size of the window to prevent resizing below this limit.
window.title('Draw ++')                   # Set the title of the window to "Draw ++".

 
# Global variables for file management:
opened_files = []  # List to store the paths of currently opened files.
current_file_index = None  # Index of the currently active file in the opened_files list.

# Create a frame for file-related buttons:
# This frame will hold buttons for actions like opening, saving, or switching between files.
file_buttons_frame = Frame(window, bg="#333333", height=30)  # A frame with a dark background (#333333).
file_buttons_frame.pack(side="top", fill="x")  # Positioned at the top of the window, stretching horizontally.

 
 
# Function to save the content of the text area to a new Draw++ (.dpp) file.
#
# This function allows the user to choose a location and name for saving the
# content of the `text_area` widget. It manages the opened files list (`opened_files`)
# and updates the currently active file index (`current_file_index`).
#
# Parameters:
# - None.
#
# Logic:
# 1. Opens a "Save As" dialog box, restricted to files with the `.dpp` extension.
# 2. Writes the content of `text_area` to the specified file path.
# 3. Updates the `opened_files` list and `current_file_index` with the new file.
# 4. If the current file is "Untitled," replaces it with the new file path.
# 5. Displays a confirmation message upon successful saving or an error message upon failure.
#
# Notes:
# - The global variable `current_file_index` is used to track the active file in `opened_files`.
# - The function ensures that the text content is saved as plain text.
#
# Example Usage:
# save_as()  # Prompts the user to save the content of `text_area` to a .dpp file.
def save_as():
    global current_file_index  # Declare the global variable to track the current file index.

    # Step 1: Open a "Save As" dialog box to get the file path from the user.
    # Restricts the file type to Draw++ files (.dpp).
    file_path = filedialog.asksaveasfilename(
        defaultextension=".dpp",  # Default file extension is ".dpp".
        filetypes=[("Draw++ files", "*.dpp")]  # Only allow saving files as .dpp.
    )

    # Step 2: Check if the user selected a file path or canceled the dialog.
    if file_path:
        try:
            # Step 3: Write the content of `text_area` to the specified file.
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, END))  # Save the content of `text_area`.

            # Step 4: Display a confirmation message upon successful saving.
            messagebox.showinfo("Success", "File saved.")

            # Step 5: Update the `opened_files` list and `current_file_index`.
            if current_file_index is None or opened_files[current_file_index] == "Untitled":
                # If the current file is unnamed ("Untitled"), replace it with the new file path.
                opened_files[current_file_index] = file_path
            else:
                # Otherwise, add the new file to the list of opened files and update the index.
                opened_files.append(file_path)
                current_file_index = len(opened_files) - 1

        except Exception as e:
            # Step 6: Handle any exceptions during file writing.
            # Display an error message if the file could not be saved.
            messagebox.showerror("Error", f"Unable to save file : {e}")


 
# Function to save the content of the text area.
#
# This function saves the current content of `text_area` to the active file.
# If the active file is "Untitled" or no file is currently active, it prompts the
# user to choose a file location using the `save_as` function. If the file already
# exists, it overwrites the file with the new content.
#
# Parameters:
# - None.
#
# Logic:
# 1. Check if the active file is "Untitled" or no file is currently active:
#    - If true, call `save_as` to prompt the user for a file location.
#    - If the user successfully saves the file, return the file path.
#    - If the user cancels the operation, return `None`.
# 2. If a valid file already exists, overwrite its content:
#    - Write the content of `text_area` to the file.
#    - Display a confirmation message upon successful saving.
#    - Return the file path.
# 3. Handle any errors during the save operation:
#    - Display an error message if saving fails.
#    - Return `None`.
#
# Notes:
# - The global variable `current_file_index` tracks the active file in the `opened_files` list.
# - The function relies on `save_as` to handle new files or unsaved changes.
#
# Example Usage:
# save()  # Saves the content of `text_area` to the active file or prompts for a file location.
def save():
    global current_file_index  # Declare the global variable to track the active file index.

    # Step 1: Check if the active file is "Untitled" or no file is active.
    if current_file_index is None or opened_files[current_file_index] == "Untitled":
        # Call `save_as` to prompt the user for a file location.
        save_as()
        
        # Step 1.1: Check if the user successfully saved the file.
        if current_file_index is not None:
            # Retrieve the path of the newly saved file.
            file_path = opened_files[current_file_index]
            return file_path  # Return the file path.
        else:
            # If the user cancels the save operation, return None.
            return None

    else:
        # Step 2: Save to the existing file.
        file_path = opened_files[current_file_index]  # Retrieve the active file path.
        try:
            # Open the file in write mode and save the content of `text_area`.
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, END))  # Write all content from `text_area`.

            # Step 2.1: Display a confirmation message upon successful saving.
            messagebox.showinfo("Success", f"File saved : {file_path}")
            return file_path  # Return the file path of the saved file.

        except Exception as e:
            # Step 3: Handle errors during the save operation.
            messagebox.showerror("Error", f"Unable to save file : {e}")
            return None  # Return None if saving fails.

 
 
# Function to open and load a file into the text area.
#
# This function allows the user to select a file from their system, loads its content
# into the `text_area` widget, and updates the list of opened files (`opened_files`)
# along with the active file index (`current_file_index`). It also ensures that
# line numbers and UI elements related to file management are updated accordingly.
#
# Parameters:
# - None.
#
# Logic:
# 1. Opens a file dialog to let the user choose a file to open.
# 2. Reads the selected file's content and loads it into the `text_area`.
# 3. If the file is not already in `opened_files`, adds it to the list and updates
#    the active file index (`current_file_index`).
# 4. Updates the line numbers and refreshes the file-related UI elements.
# 5. Displays an error message if the file cannot be opened or read.
#
# Notes:
# - Supports files with the `.dpp` extension by default, but allows all file types.
# - Updates global variables `current_file_index` and `opened_files` to reflect the
#   newly opened file.
#
# Example Usage:
# open_file()  # Prompts the user to open a file and loads its content into `text_area`.
def open_file():
    global current_file_index, opened_files  # Declare global variables to manage opened files.

    # Step 1: Open a file dialog to let the user select a file.
    file_path = filedialog.askopenfilename(
        defaultextension=".dpp",  # Default file extension is ".dpp".
        filetypes=[("Text Files", "*.dpp"), ("All Files", "*.*")]  # Supported file types.
    )

    # Step 2: Check if the user selected a file or canceled the dialog.
    if file_path:
        try:
            # Step 3: Open and read the selected file.
            with open(file_path, "r") as file:
                content = file.read()  # Read the entire file content.

                # Step 3.1: Clear the current content in `text_area`.
                text_area.delete(1.0, END)

                # Step 3.2: Load the file content into `text_area`.
                text_area.insert(1.0, content)

            # Step 4: Update `opened_files` and `current_file_index`.
            if file_path not in opened_files:
                # Add the file to the list if it's not already present.
                opened_files.append(file_path)

            # Set the current file index to the newly opened file.
            current_file_index = opened_files.index(file_path)

            # Step 5: Update line numbers to match the loaded content.
            update_line_numbers()

        except Exception as e:
            # Step 6: Display an error message if the file cannot be opened or read.
            messagebox.showerror("Error", f"Unable to save file: {e}")

    # Step 7: Refresh the UI elements related to file management.
    update_file_buttons()


 
# Function to create a new file.
#
# This function clears the current text area and prepares the application for
# a new file. A temporary "Untitled" file is added to the `opened_files` list,
# and it becomes the active file. If an existing "Untitled" file is already
# present, it is removed before creating a new one to avoid duplicates.
#
# Parameters:
# - None.
#
# Logic:
# 1. Checks if an "Untitled" file already exists:
#    - If true, removes the "Untitled" file from `opened_files`.
# 2. Clears the `text_area` to prepare for the new file.
# 3. Adds a new "Untitled" file to the `opened_files` list.
# 4. Updates the active file index (`current_file_index`) to the newly created file.
# 5. Updates the line numbers and file-related UI elements.
#
# Notes:
# - This function does not save the new file to disk; it remains temporary until saved.
# - The `opened_files` list and `current_file_index` are global variables used to
#   manage the opened files.
#
# Example Usage:
# create_new_file()  # Clears the text area and creates a new temporary "Untitled" file.
def create_new_file():
    global current_file_index, opened_files  # Declare global variables for file management.

    # Step 1: Check if an "Untitled" file already exists.
    if current_file_index is not None and opened_files[current_file_index] == "Untitled":
        # If an "Untitled" file exists, remove it from the `opened_files` list.
        opened_files.pop(current_file_index)

    # Step 2: Clear the text area to prepare for the new file.
    text_area.delete(1.0, END)  # Removes all content from the text area.

    # Step 3: Add a new temporary "Untitled" file to the `opened_files` list.
    opened_files.append("Untitled")  # Append "Untitled" as a new temporary file.

    # Step 4: Update the active file index to point to the new "Untitled" file.
    current_file_index = len(opened_files) - 1  # Set the index to the last file in the list.
    print("New file created : Untitled")  # Debug message indicating a new file has been created.

    # Step 5: Update file-related UI elements.
    update_file_buttons()  # Refresh the file management buttons.
    update_line_numbers()  # Refresh the line numbers to match the cleared text area.

 
 
# Function to dynamically update the visible line numbers.
#
# This function ensures that the `line_numbers` widget displays line numbers
# corresponding to the visible portion of the `text_area`. It recalculates
# the first and last visible lines and updates the content of `line_numbers`
# accordingly.
#
# Parameters:
# - *args: Optional arguments to allow compatibility with event bindings (e.g., scrolling events).
#
# Logic:
# 1. Temporarily make the `line_numbers` widget editable.
# 2. Clear the existing line numbers.
# 3. Calculate the first and last visible lines in the `text_area`:
#    - The first visible line is determined using the index `@0,0` (top-left corner of the area).
#    - The last visible line is calculated using the widget's height.
# 4. Generate a string of line numbers for the visible lines.
# 5. Insert the generated line numbers into `line_numbers`.
# 6. Make the `line_numbers` widget non-editable again.
#
# Notes:
# - This function ensures that `line_numbers` always reflects the current scroll position
#   of `text_area`.
# - Designed to work efficiently by only displaying numbers for the visible portion of `text_area`.
#
# Example Usage:
# update_line_numbers()  # Dynamically refreshes the line numbers based on `text_area` visibility.
def update_line_numbers(*args):
    # Step 1: Temporarily make the `line_numbers` widget editable.
    line_numbers.configure(state='normal')  # Allow modifications to `line_numbers`.

    # Step 2: Clear the existing content of `line_numbers`.
    line_numbers.delete(1.0, END)  # Remove all content from the widget.

    # Step 3: Calculate the first and last visible lines in `text_area`.

    # 3.1: Determine the first visible line using the index `@0,0`.
    # `@0,0` represents the top-left corner of the visible area in `text_area`.
    first_visible_line = int(text_area.index('@0,0').split('.')[0])

    # 3.2: Determine the last visible line based on the height of `text_area`.
    # `@0,%d` uses the height of the widget to find the bottom of the visible area.
    last_visible_line = int(text_area.index('@0,%d' % text_area.winfo_height()).split('.')[0])

    # Step 4: Generate a string of line numbers for the visible lines.
    # Create a list of line numbers from the first to the last visible line.
    line_content = "\n".join(str(i) for i in range(first_visible_line, last_visible_line + 1))

    # Step 5: Insert the generated line numbers into `line_numbers`.
    line_numbers.insert(1.0, line_content)  # Add the generated content to the widget.

    # Step 6: Make the `line_numbers` widget non-editable again.
    line_numbers.configure(state='disabled')  # Prevent further modifications.

 
 
# Function to switch to a different file in the list of opened files.
#
# This function loads the content of a specified file from the `opened_files` list
# into the `text_area` widget and updates the `current_file_index` to the selected file.
# It ensures that the line numbers are updated and handles any errors that may occur
# during file access.
#
# Parameters:
# - index (int): The index of the file in the `opened_files` list to switch to.
#
# Logic:
# 1. Validate the given index:
#    - Ensure it is within the bounds of the `opened_files` list.
# 2. Update the active file index (`current_file_index`) to the given index.
# 3. Attempt to open the selected file:
#    - If successful, clear the current content in `text_area` and load the file's content.
#    - If an error occurs, display an error message to the user.
# 4. Refresh the line numbers to align with the loaded content.
# 5. Print a debug message indicating the file switch (optional).
#
# Notes:
# - This function relies on the global variables `current_file_index` and `opened_files`
#   for file management.
# - If the file cannot be opened or read, the function gracefully handles the error
#   and alerts the user.
#
# Example Usage:
# switch_file(1)  # Switches to the second file in the `opened_files` list.
def switch_file(index):
    global current_file_index  # Declare the global variable to track the active file index.

    # Step 1: Validate the given index.
    # Ensure the index is within the bounds of the `opened_files` list.
    if 0 <= index < len(opened_files):
        # Step 2: Update the active file index.
        current_file_index = index
        file_path = opened_files[index]  # Retrieve the file path from the `opened_files` list.

        try:
            # Step 3: Open the selected file and read its content.
            with open(file_path, "r") as file:
                content = file.read()  # Read the entire file content.

                # Step 3.1: Clear the current content in `text_area`.
                text_area.delete(1.0, END)

                # Step 3.2: Load the new content into `text_area`.
                text_area.insert(END, content)

            # Step 4: Refresh the line numbers to match the loaded content.
            update_line_numbers()

            # Step 5: Print a debug message indicating the file switch.
            print(f"Switched to file: {file_path}")

        except Exception as e:
            # Step 6: Handle any errors during file access.
            # Display an error message if the file cannot be opened or read.
            messagebox.showerror("Error", f"Unable to save file : {e}")

 
 
# Function to close an opened file and update the file management buttons.
#
# This function removes a file from the `opened_files` list and adjusts the
# application state accordingly. If the currently active file is closed, it
# switches to another file if available or clears the `text_area` if no files
# remain. It also updates the `current_file_index` and refreshes the file-related
# UI buttons.
#
# Parameters:
# - index (int): The index of the file in the `opened_files` list to close.
#
# Logic:
# 1. Validate the given index:
#    - Ensure it is within the bounds of the `opened_files` list.
# 2. Remove the specified file from the `opened_files` list.
#    - Print a debug message confirming the closed file.
# 3. Handle the case where the closed file is the currently active file:
#    - If other files are still open, switch to the first file in the list.
#    - If no files remain, clear the `text_area` and reset `current_file_index`.
# 4. Adjust the active file index (`current_file_index`) if a file before it is closed.
# 5. Update the file management buttons to reflect the current state.
#
# Notes:
# - This function assumes that `opened_files` and `current_file_index` are global variables.
# - If the closed file is the last one in the list, the application properly resets its state.
#
# Example Usage:
# remove_file(2)  # Closes the third file in the `opened_files` list.
def remove_file(index):
    global current_file_index  # Declare the global variable to track the active file index.

    # Step 1: Validate the given index.
    # Ensure the index is within the bounds of the `opened_files` list.
    if 0 <= index < len(opened_files):
        # Step 2: Remove the specified file from the `opened_files` list.
        closed_file = opened_files.pop(index)  # Remove the file at the given index.
        print(f"Closed file: {closed_file}")  # Debug message indicating the closed file.

        # Step 3: Handle the case where the closed file is the currently active file.
        if current_file_index == index:
            if opened_files:  # If there are other files in the list, switch to the first file.
                current_file_index = 0  # Set the active index to the first file.
                switch_file(current_file_index)  # Load the first file's content.
            else:  # If no files remain, clear the `text_area`.
                current_file_index = None  # Reset the active file index.
                text_area.delete(1.0, END)  # Clear all content from the text area.

        # Step 4: Adjust the active file index if a file before it is closed.
        elif current_file_index > index:
            current_file_index -= 1  # Decrement the active file index to account for the removal.

        # Step 5: Update the file management buttons.
        update_file_buttons()  # Refresh the UI buttons to reflect the updated file list.

 

# Function to switch to a different file using a popup dialog.
#
# This function allows the user to switch to a file in the `opened_files` list
# by interacting with a popup dialog. Once the file switch is performed using
# the `switch_file` function, the popup is closed.
#
# Parameters:
# - index (int): The index of the file in the `opened_files` list to switch to.
# - popup: The popup dialog object to be closed after switching files.
#
# Logic:
# 1. Calls `switch_file(index)` to load the content of the file at the given index.
# 2. Closes the popup dialog using `popup.destroy()` to ensure the interface is cleaned up.
#
# Notes:
# - Relies on the `switch_file` function to handle file switching logic.
# - The `popup` object must be a valid Tkinter or CustomTkinter dialog widget with a `.destroy()` method.
#
# Example Usage:
# switch_file_from_popup(1, popup)  # Switches to the second file and closes the popup.
def switch_file_from_popup(index, popup):
    # Step 1: Call the `switch_file` function to switch to the specified file.
    # This function loads the content of the file at the given index into the text area.
    switch_file(index)

    # Step 2: Close the popup dialog.
    # The popup dialog is destroyed to clean up the interface after the action is performed.
    popup.destroy()

 

# Function to update the list of opened file buttons at the top of the application.
#
# This function dynamically refreshes the file management buttons displayed at
# the top of the application. Each file in the `opened_files` list is represented
# by a button that allows the user to switch to the file or close it.
#
# Parameters:
# - None.
#
# Logic:
# 1. Clear any existing widgets in the `file_buttons_frame`.
# 2. Loop through the `opened_files` list to create a button for each file:
#    - A button to switch to the file, displaying the file name.
#    - A close button (red "x") to remove the file from the list.
# 3. Arrange these buttons within a container (`button_container`) to group
#    the file button and close button together.
# 4. Add each `button_container` to the `file_buttons_frame`.
#
# Notes:
# - Relies on global variables `opened_files` and `file_buttons_frame`.
# - Calls `switch_file` to switch to a file and `remove_file` to close a file.
# - Ensures the UI dynamically reflects the current state of the `opened_files` list.
#
# Example Usage:
# update_file_buttons()  # Refreshes the file buttons to reflect the current state of `opened_files`.
def update_file_buttons():
    """Update the list of opened file buttons at the top of the application."""
    global file_buttons_frame  # Use the global frame that contains the file buttons.

    # Step 1: Clear existing widgets in `file_buttons_frame`.
    for widget in file_buttons_frame.winfo_children():
        widget.destroy()  # Remove all child widgets from the frame.

    # Step 2: Create a button for each file in `opened_files`.
    for index, file_path in enumerate(opened_files):
        # Extract the file name from the full file path.
        file_name = file_path.split("/")[-1]  # Get the last part of the file path.

        # Step 2.1: Create a container for the file button and close button.
        button_container = Frame(file_buttons_frame, bg="#2B2B2B")  # Dark background for the container.
        button_container.pack(side="left", padx=2)  # Add some horizontal padding between containers.

        # Step 2.2: Create the button to switch to the file.
        Button(
            button_container,  # Parent is the button container.
            text=file_name,  # Display the file name on the button.
            bg="#4CAF50",  # Green background for the button.
            fg="white",  # White text color.
            font=("Helvetica", 10),  # Font style and size.
            command=lambda i=index: switch_file(i),  # Call `switch_file` with the file's index.
            bd=0,  # No border for a flat look.
            relief="flat",  # Flat appearance for the button.
            activebackground="#45a049",  # Slightly darker green when hovered.
            cursor="hand2",  # Change the cursor to a hand when hovering.
        ).pack(side="left")  # Place the button on the left side of the container.

        # Step 2.3: Create the close button (red "x") to remove the file.
        Button(
            button_container,  # Parent is the button container.
            text="x",  # Display "x" as the close button label.
            bg="#FF6347",  # Red background for the close button.
            fg="white",  # White text color.
            font=("Helvetica", 10, "bold"),  # Bold font for better visibility.
            command=lambda i=index: remove_file(i),  # Call `remove_file` with the file's index.
            bd=0,  # No border for a flat look.
            relief="flat",  # Flat appearance for the button.
            activebackground="#FF4500",  # Slightly darker red when hovered.
            cursor="hand2",  # Change the cursor to a hand when hovering.
        ).pack(side="right")  # Place the close button on the right side of the container.

 
 
# Function to synchronize scrolling between the text area and the line numbers.
#
# This function ensures that both `text_area` and `line_numbers` scroll in sync,
# providing a seamless user experience. It also updates the visible line numbers
# after each scrolling action.
#
# Parameters:
# - *args: A variable-length argument list capturing scroll-related arguments:
#    - If `args[0]` is "moveto", it indicates a direct move to a specific position.
#    - If `args[0]` is "scroll", it indicates a relative scroll action (up or down).
#
# Logic:
# 1. Check if scrolling arguments are provided and are valid (`moveto` or `scroll`).
# 2. Apply the scrolling action to both `text_area` and `line_numbers` using `yview`.
# 3. Call `update_line_numbers` to refresh the visible line numbers based on the new scroll position.
#
# Notes:
# - This function is typically bound to the vertical scrollbar or a scrolling event.
# - Synchronization ensures that the user sees accurate line numbers corresponding to
#   the visible text in `text_area`.
#
# Example Usage:
# on_scroll("moveto", 0.5)  # Scrolls both widgets to the middle of the content.
# on_scroll("scroll", -1, "units")  # Scrolls one line up in both widgets.
def on_scroll(*args):
    # Step 1: Check if scrolling arguments are provided and valid.
    # The first argument (`args[0]`) must indicate a scrolling action ("moveto" or "scroll").
    if args and args[0] in ('moveto', 'scroll'):
        # Step 2: Apply the scrolling action to both `text_area` and `line_numbers`.
        # Synchronize the vertical scroll position of `text_area` with the provided arguments.
        text_area.yview(*args)
        # Synchronize the vertical scroll position of `line_numbers` with the same arguments.
        line_numbers.yview(*args)

        # Step 3: Update the visible line numbers after scrolling.
        # This ensures the line numbers match the visible portion of the text area.
        update_line_numbers()

 
 
# Function to update the line numbers after the application window is resized.
#
# This function ensures that the `line_numbers` widget is updated whenever the
# application window is resized. It recalculates the visible lines in the `text_area`
# and refreshes the line numbers accordingly.
#
# Parameters:
# - event: The resize event object, containing information about the new size
#   of the window (e.g., width and height).
#
# Logic:
# 1. Trigger the `update_line_numbers` function to recalculate the visible line numbers.
#    - This ensures that the line numbers match the new dimensions of the `text_area`.
#
# Notes:
# - This function should be bound to the `<Configure>` event of the window or
#   a relevant container to automatically respond to resizing actions.
# - Works seamlessly with `update_line_numbers` to ensure consistent behavior.
#
# Example Usage:
# window.bind("<Configure>", on_resize)  # Binds the function to window resize events.
def on_resize(event):
    """Update line numbers after the window is resized."""
    # Step 1: Call `update_line_numbers` to refresh the visible line numbers.
    # This ensures that the line numbers reflect the new dimensions of the `text_area`.
    update_line_numbers()

 

# Function to execute the lexer and parser with the content of the main text area.
#
# This function saves the content of the `text_area` widget to a temporary file,
# executes the lexer script (`lexeurmy.py`) on the file, and displays the results
# or errors in the `correction_area` widget. If errors are detected, the corresponding
# lines in `text_area` are highlighted.
#
# Parameters:
# - None.
#
# Logic:
# 1. Retrieve the content of `text_area` and ensure it is not empty.
# 2. Save the content to a temporary file using the `save` function.
#    - If saving fails, display an error message and exit.
# 3. Run the `lexeurmy.py` script on the saved file using `subprocess.run`.
# 4. If the execution is successful:
#    - Display the output in the `correction_area` widget.
# 5. If errors are detected:
#    - Highlight the erroneous lines in `text_area`.
#    - Display the error messages in `correction_area`.
# 6. Handle any unexpected exceptions during execution:
#    - Display the exception details in `correction_area`.
#
# Notes:
# - The function uses the `subprocess` module to execute the lexer script.
# - Error messages are parsed to extract line numbers for highlighting.
# - The `correction_area` widget is temporarily made editable to insert results or errors.
#
# Example Usage:
# run_code()  # Executes the lexer on the current text area content and displays the results.
def run_code():
    """
    Execute the lexer and parser with the content of the main text area.
    Display results or errors in the correction area.
    """
    # Step 1: Retrieve the content of the `text_area`.
    content = text_area.get("1.0", "end-1c")  # Get all content except the trailing newline.
    if not content.strip():
        # If the content is empty, display an error message and exit.
        messagebox.showerror("Error", "The text field is empty.")
        return

    # Step 2: Save the content to a temporary file using the `save` function.
    try:
        file_path = save()
        if not file_path:
            # If the file could not be saved, display an error message and exit.
            messagebox.showerror("Error", "The file could not be saved.")
            return

        # Step 3: Execute the lexer script on the saved file.
        result = subprocess.run(
            ["python", "lexeurmy.py", file_path],  # Command to run the lexer script.
            capture_output=True, text=True  # Capture stdout and stderr as text.
        )

        # Step 4: Handle successful execution.
        if result.returncode == 0:
            # Temporarily make `correction_area` editable.
            correction_area.configure(state='normal')

            # Clear old highlights and corrections.
            text_area.tag_remove("err", "1.0", "end")
            correction_area.delete(1.0, END)

            # Insert the output into `correction_area` and configure the text style.
            correction_area.insert(END, result.stdout, "correction")
            correction_area.configure(state='disabled')  # Make `correction_area` read-only.
            correction_area.tag_config("correction", foreground="green")  # Set green text color.

        # Step 5: Handle errors in execution.
        else:
            # Temporarily make `correction_area` editable.
            correction_area.configure(state='normal')

            # Clear old highlights and corrections.
            text_area.tag_remove("err", "1.0", "end")
            correction_area.delete(1.0, END)

            # Insert error output into `correction_area`.
            correction_area.insert(END, result.stderr, "correction")
            correction_area.configure(state='disabled')  # Make `correction_area` read-only.
            correction_area.tag_config("correction", foreground="green")  # Set green text color.

            # Parse the error output to find line numbers.
            errors = []  # List to store line numbers with errors.
            for line in result.stderr.splitlines():
                # Extract line numbers using a regex.
                match = re.search(r"ligne (\d+)", line, re.IGNORECASE)
                if match:
                    errors.append(int(match.group(1)))  # Add the line number to the list.

            # Highlight erroneous lines in `text_area`.
            for line_number in errors:
                start_idx = f"{line_number}.0"  # Start of the line.
                end_idx = f"{line_number}.end"  # End of the line.
                text_area.tag_add("err", start_idx, end_idx)  # Add an "err" tag to the line.
                text_area.tag_config("err", underline=True, underlinefg="red")  # Configure the tag style.

    # Step 6: Handle unexpected exceptions during execution.
    except Exception as e:
        # Temporarily make `correction_area` editable.
        correction_area.configure(state='normal')

        # Clear the `correction_area` and insert the exception details.
        correction_area.delete(1.0, END)
        correction_area.insert(END, f"Failed execution : {e}", "correction")

        # Make `correction_area` read-only and configure the text style.
        correction_area.configure(state='disabled')
        correction_area.tag_config("correction", foreground="green")



# Sidebar Configuration
#
# This section creates and configures a sidebar (vertical navigation area) for the application.
# The sidebar is positioned on the left side of the window and serves as a container
# for widgets like labels, buttons, or other UI components.
#
# Components:
# - `sidebar`: A `Frame` widget used as the main container for the sidebar.
# - Sidebar title: A `Label` widget displaying the title "Draw++" in bold text.
#
# Logic:
# 1. Create a `Frame` for the sidebar with a dark background (`#2B2B2B`).
#    - Set a fixed width for the sidebar (200 pixels).
#    - Position the sidebar on the left side of the application window.
# 2. Add a `Label` widget to display the application title:
#    - Use a bold font ("Helvetica", size 18) for better visibility.
#    - Set the text color to white (`fg="white"`) and background to match the sidebar.
#    - Add padding (`pady=20`) to visually separate the title from other widgets.
#
# Notes:
# - The sidebar is designed to organize navigation or control elements for the application.
# - Additional widgets (e.g., buttons, listboxes) can be added to the sidebar for enhanced functionality.
# Step 1: Create a `Frame` widget for the sidebar.
# The sidebar acts as a vertical container for navigation or control widgets.
sidebar = Frame(
    window,  # The parent widget is the main application window (`window`).
    bg="#2B2B2B",  # Dark gray background for the sidebar.
    width=200  # Fixed width of 200 pixels.
)
# Position the sidebar on the left side of the window, filling the vertical space.
sidebar.pack(fill="y", side="left")

# Step 2: Add a title to the sidebar using a `Label` widget.
# This label displays the application title "Draw++" at the top of the sidebar.
Label(
    sidebar,  # The parent widget is the sidebar (`sidebar`).
    text="Draw++",  # Text displayed in the label.
    bg="#2B2B2B",  # Match the background color of the sidebar.
    fg="white",  # Set the text color to white for contrast.
    font=("Helvetica", 18, "bold")  # Use a bold font for better visibility.
).pack(pady=20)  # Add vertical padding (20 pixels) above and below the label.

 
 
# Adding styled buttons to the sidebar.
#
# This section creates and organizes styled buttons in the sidebar for navigation
# or control actions. Each button is dynamically styled and linked to a specific
# command. Buttons are created using the `create_styled_button` function and added
# to a container frame within the sidebar.
#
# Components:
# - `create_styled_button`: A utility function to generate consistently styled buttons.
# - `button_frame`: A `Frame` widget to organize the buttons vertically in the sidebar.
# - Buttons: Represent individual actions (e.g., "Run", "Save", "Open File").
#
# Logic:
# 1. Define a helper function (`create_styled_button`) to create buttons with consistent styles:
#    - Takes parameters for the parent container, button text, and associated command.
#    - Applies a green theme (`bg="#4CAF50"`) with hover effects.
# 2. Create a container frame (`button_frame`) to group the buttons in the sidebar.
#    - Positioned to expand and center the buttons vertically.
# 3. Dynamically generate buttons for a predefined list of actions:
#    - Uses the helper function to create buttons with specific text and commands.
#    - Adds padding and alignment to ensure a clean and centered layout.
#
# Notes:
# - Buttons are styled for consistency and interactivity, using hover effects and hand cursors.
# - This approach is modular, allowing additional buttons to be added easily.
# Step 1: Define a helper function to create styled buttons.
def create_styled_button(parent, text, command):
    """
    Create a styled button with a green theme and hover effects.
    
    Parameters:
    - parent: The container (e.g., a Frame) where the button will be placed.
    - text: The text displayed on the button.
    - command: The function to execute when the button is clicked.

    Returns:
    - A styled Button widget.
    """
    return Button(
        parent,  # Parent container for the button.
        text=text,  # Displayed text.
        command=command,  # Command to execute on click.
        bg="#4CAF50",  # Green background.
        fg="white",  # White text color.
        font=("Helvetica", 12, "bold"),  # Bold font for better visibility.
        bd=0,  # No border for a flat look.
        relief="flat",  # Flat button style.
        padx=10, pady=5,  # Internal padding for a larger clickable area.
        activebackground="#45a049",  # Slightly darker green on hover.
        cursor="hand2",  # Hand cursor on hover.
        highlightthickness=0  # No additional border highlighting.
    )

# Step 2: Create a container frame to organize the buttons.
button_frame = Frame(
    sidebar,  # Parent container is the sidebar.
    bg="#2B2B2B"  # Match the background color of the sidebar.
)
# Position the button frame to expand vertically and center its content.
button_frame.pack(expand=True)

# Step 3: Dynamically generate buttons for predefined actions.
# Define a list of button labels and associated commands.
for btn_text, cmd in [
    ("Run", run_code),  # Run the lexer/parser.
    ("Save", save),  # Save the current file.
    ("Save As", save_as),  # Save the current file as a new file.
    ("Open File", open_file),  # Open a file.
    ("New File", create_new_file)  # Create a new file.
]:
    # Use the helper function to create a button for each action.
    button = create_styled_button(button_frame, btn_text, cmd)
    # Add the button to the frame with vertical padding and horizontal alignment.
    button.pack(
        pady=10,  # Add vertical spacing between buttons.
        fill="x",  # Stretch the button horizontally to match the frame width.
        padx=10  # Add horizontal padding inside the frame.
    )

 

# Configuration for the main text area, line numbers, and correction area.
#
# This section initializes and organizes the primary widgets of the application:
# - `line_numbers`: Displays the line numbers for the visible portion of `text_area`.
# - `text_area`: The main text editor area where the user can type or edit content.
# - `correction_area`: Displays the results or errors generated by code execution.
#
# Logic:
# 1. Create a container (`text_area_container`) to hold `line_numbers` and `text_area`.
# 2. Add a bordered frame for `line_numbers` to simulate a white border.
# 3. Configure and place `line_numbers` within the bordered frame.
# 4. Configure and place `text_area` in the container, filling the remaining space.
# 5. Configure `correction_area` to display below the main text editor.
# 6. Bind events to `text_area` to synchronize scrolling, resizing, and line number updates.
# 7. Initialize the line numbers to match the content of `text_area`.
#
# Notes:
# - The `correction_area` is initially set to read-only (`state='disabled'`) to prevent user input.
# - Scrolling in `text_area` and `line_numbers` is synchronized using `on_scroll`.
#
# Example Usage:
# - Type in `text_area` to see line numbers dynamically update.
# - Resize the window to trigger line number updates and maintain layout consistency.
# Step 1: Create a container for `line_numbers` and `text_area`.
text_area_container = Frame(
    window,  # The parent widget is the main application window (`window`).
    bg="#1E1E1E"  # Background color matching the application's dark theme.
)
# Position the container at the top of the application window.
text_area_container.pack(side="top", fill="both", expand=True)

# Step 2: Create a bordered frame for `line_numbers`.
line_numbers_border = Frame(
    text_area_container,  # The parent widget is the `text_area_container`.
    bg="white",  # Simulated white border for `line_numbers`.
    padx=1, pady=1  # Padding to create the border effect.
)
# Position the bordered frame on the left side of the container, filling vertically.
line_numbers_border.pack(side="left", fill="y")

# Step 3: Add the `line_numbers` widget inside the bordered frame.
line_numbers = CTkTextbox(
    line_numbers_border,  # The parent widget is the bordered frame.
    width=40,  # Fixed width for line numbers.
    border_width=0,  # No additional border.
    takefocus=0,  # Prevents the widget from receiving focus.
    bg_color="#333333",  # Dark gray background.
    fg_color="#333333",  # Matching background for seamless integration.
    text_color="#AAAAAA",  # Light gray text for line numbers.
    font=("Consolas", 15),  # Monospaced font for better alignment.
    state='disabled',  # Read-only to prevent user interaction.
    activate_scrollbars=False  # No internal scrollbars for this widget.
)
# Fill the bordered frame entirely to align properly with the text area.
line_numbers.pack(fill="both", expand=True)

# Step 4: Add the `text_area` widget to the container.
text_area = CTkTextbox(
    text_area_container,  # The parent widget is the `text_area_container`.
    undo=True,  # Enable undo functionality.
    wrap="word",  # Wrap lines at word boundaries.
    bg_color="#1E1E1E",  # Background color matching the dark theme.
    fg_color="#1E1E1E",  # Same background color for consistency.
    text_color="#FFFFFF",  # White text for better visibility.
    font=("Consolas", 15),  # Monospaced font for text editing.
    border_width=0  # No additional border.
)
# Position the `text_area` on the right, filling the remaining space.
text_area.pack(side="right", fill="both", expand=True)

# Step 5: Add the `correction_area` widget below the main editor.
correction_area = CTkTextbox(
    window,  # The parent widget is the main application window (`window`).
    wrap="word",  # Wrap lines at word boundaries.
    state='disabled',  # Read-only to prevent user input.
    bg_color="#1E1E1E",  # Background color matching the dark theme.
    fg_color="#1E1E1E",  # Same background color for consistency.
    text_color="#78c449",  # Green text for corrections or results.
    height=100,  # Fixed height for the correction area.
    border_width=0  # No additional border.
)
# Position the `correction_area` at the bottom of the application window.
correction_area.pack(side="bottom", fill="x", padx=1, pady=1)

# Step 6: Bind events to synchronize scrolling, resizing, and line number updates.

# Update line numbers when keys are released in `text_area`.
text_area.bind("<KeyRelease>", update_line_numbers)

# Update line numbers and layout when the window is resized.
text_area.bind("<Configure>", on_resize)

# Update line numbers as the user types.
text_area.bind("<KeyPress>", update_line_numbers)

# Step 7: Synchronize scrolling between `text_area` and `line_numbers`.
text_area.configure(yscrollcommand=on_scroll)  # Tie vertical scrolling to `on_scroll`.
line_numbers.configure(yscrollcommand=on_scroll)  # Same for `line_numbers`.

# Step 8: Perform an initial update of the line numbers.
update_line_numbers()

# Step 9: Launch the application.
window.mainloop()  # Start the Tkinter event loop.

 