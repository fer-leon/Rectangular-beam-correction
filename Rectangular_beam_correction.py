import re
import tkinter as tk
from tkinter import filedialog, simpledialog

# Function to adjust the feed rate in the GCODE based on the specified factor and axis
def adjust_feed_rate(gcode, factor=0.5, axis='Y'):
    adjusted_gcode = []
    current_feed_rate = None
    last_x = None
    last_y = None

    for line in gcode.splitlines():
        # Extract the current feed rate if present
        if 'F' in line:
            match = re.search(r'F(\d+\.?\d*)', line)
            if match:
                current_feed_rate = float(match.group(1))

        # Extract the last known positions for X and Y
        x_match = re.search(r'X(-?\d+\.?\d*)', line)
        y_match = re.search(r'Y(-?\d+\.?\d*)', line)
        
        if x_match or y_match:
            x_value = float(x_match.group(1)) if x_match else last_x
            y_value = float(y_match.group(1)) if y_match else last_y
            
            if line.startswith('G1') and last_x is not None and last_y is not None:
                # Calculate the movement in X and Y
                delta_x = x_value - last_x
                delta_y = y_value - last_y

                # Calculate the proportion of movement in the selected axis
                total_movement = abs(delta_x) + abs(delta_y)
                if total_movement != 0:
                    if axis == 'Y':
                        proportion = abs(delta_y) / total_movement
                    else:
                        proportion = abs(delta_x) / total_movement
                else:
                    proportion = 0

                # Adjust the feed rate based on the selected axis proportion
                if current_feed_rate is not None:
                    adjusted_feed_rate = current_feed_rate * (1 + (factor - 1) * proportion)
                    # Add the adjusted feed rate to the line
                    if 'F' in line:
                        line = re.sub(r'F\d+\.?\d*', f'F{adjusted_feed_rate:.2f}', line)
                    else:
                        line += f' F{adjusted_feed_rate:.2f}'

            # Update last_x and last_y
            last_x = x_value
            last_y = y_value
        
        adjusted_gcode.append(line)

    return '\n'.join(adjusted_gcode)

# Function to center a Tkinter window on the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to open a file dialog and read the selected GCODE file
def open_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("GCODE files", "*.gcode"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            gcode = file.read()
        
        axis_selection_window = tk.Toplevel(root)
        axis_selection_window.title("Laser Beam Correction")
        axis_selection_window.configure(bg='#2e2e2e')
        axis_selection_window.minsize(400, 300)

        tk.Label(axis_selection_window, text="Enter correction factor:", bg='#2e2e2e', fg='white', font=('Helvetica', 14)).pack(pady=10)
        factor_entry = tk.Entry(axis_selection_window, font=('Helvetica', 12))
        factor_entry.pack(pady=10)

        status_label = tk.Label(axis_selection_window, text="", bg='#2e2e2e', fg='white', font=('Helvetica', 12))
        status_label.pack()

        tk.Label(axis_selection_window, text="Select an axis to correct:", bg='#2e2e2e', fg='white', font=('Helvetica', 14)).pack(pady=10)
        
        button_frame = tk.Frame(axis_selection_window, bg='#2e2e2e')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="X", command=lambda: select_axis('X'), bg='#4a4a4a', fg='white', font=('Helvetica', 12), padx=20, pady=10).pack(side=tk.LEFT, padx=20)
        tk.Button(button_frame, text="Y", command=lambda: select_axis('Y'), bg='#4a4a4a', fg='white', font=('Helvetica', 12), padx=20, pady=10).pack(side=tk.RIGHT, padx=20)

        # Function to handle axis selection and perform GCODE adjustments
        def select_axis(axis):
            try:
                factor = float(factor_entry.get())
            except ValueError:
                status_label.config(text="Invalid factor. Please enter a number.")
                return

            status_label.config(text="Performing corrections...")
            axis_selection_window.update_idletasks()
            adjusted_gcode = adjust_feed_rate(gcode, factor=factor, axis=axis)
            status_label.config(text="")
            axis_selection_window.destroy()
            print(adjusted_gcode)  # Print the adjusted GCODE to the console
            save_file(adjusted_gcode)

        center_window(axis_selection_window)
        root.wait_window(axis_selection_window)

# Function to save the adjusted GCODE to a file
def save_file(adjusted_gcode):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(defaultextension=".gcode", filetypes=[("GCODE files", "*.gcode"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(adjusted_gcode)

if __name__ == "__main__":
    open_file()