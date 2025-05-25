import tkinter

import customtkinter
from PIL import Image
from PIL import ImageGrab
from pynput.mouse import Controller, Button
import time

error_label = None


def destroyColRowInput():
    global error_label

    col_val = colum_var.get()
    row_val = row_var.get()
    mine_val = mine_var.get()

    error_message = None

    # Check if inputs are empty
    if col_val == "" or row_val == "" or mine_val == "":
        error_message = "Please enter both row, column, and mine values."
    # Check if inputs are not integers
    elif not col_val.isdigit() or not row_val.isdigit() or not mine_val.isdigit():
        error_message = "Row, column, and mine number must be integers."

    if error_message:
        if error_label is None:
            error_label = customtkinter.CTkLabel(app, text=error_message, text_color="red")
            error_label.pack(padx=10, pady=10)
        else:
            error_label.configure(text=error_message)
        return

    # If valid input, remove error label (if it exists)
    if error_label is not None:
        error_label.destroy()
        error_label = None

    # Hide the row and column input fields
    nuRow.destroy()
    nuColumn.destroy()
    titleRow.destroy()
    titleColumn.destroy()
    title.destroy()
    setValues.destroy()
    mineTitle.destroy()
    nuMine.destroy()
    # Start second step

    secondStart()


# System preferences
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("700x500")
app.title("Test")

######## UI Elements for the first step

# Title first step, get the row and columns number
title = customtkinter.CTkLabel(app, text="Choose the box size:", font=("Arial", 24))
title.pack(padx=10, pady=10)

# Column input
titleColumn = customtkinter.CTkLabel(app, text="Number of columns:", font=("Arial", 16))
titleColumn.pack(padx=10, pady=10)

colum_var = tkinter.StringVar()
nuColumn = customtkinter.CTkEntry(app, textvariable=colum_var, placeholder_text="Number of columns")
nuColumn.pack(padx=10, pady=10)

# Row input
titleRow = customtkinter.CTkLabel(app, text="Number of rows:", font=("Arial", 16))
titleRow.pack(padx=10, pady=10)

row_var = tkinter.StringVar()
nuRow = customtkinter.CTkEntry(app, textvariable=row_var, placeholder_text="Number of rows")
nuRow.pack(padx=10, pady=10)

# Mine no input
mineTitle = customtkinter.CTkLabel(app, text="Number of mines:", font=("Arial", 16))
mineTitle.pack(padx=10, pady=10)

mine_var = tkinter.StringVar()
nuMine = customtkinter.CTkEntry(app, textvariable=mine_var, placeholder_text="Number of mines")
nuMine.pack(padx=10, pady=10)


# Set button
setValues = customtkinter.CTkButton(app, text="Set values", command=destroyColRowInput)
setValues.pack(padx=10, pady=10)

########UI Elements for the second step

topLeftPosition = None
bottomRightPosition = None


def secondStart():
    # Title
    windowTitle = customtkinter.CTkLabel(app, text="Now you will need to choose the window size:", font=("Arial", 24))
    windowTitle.pack(padx=10, pady=10)

    # Example image to show the window size
    image_path = "Images/imageMineSweeper.png"
    pil_image = Image.open(image_path)
    exampleImage = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image,
                                          size=(300, 300))  # You can set size
    imageLabel = customtkinter.CTkLabel(app, text="", image=exampleImage)
    imageLabel.pack(padx=10, pady=10)

    # Window size input
    explanationText = customtkinter.CTkLabel(app,
                                             text="Guide: \n 1. Hover your mouse over the top left, like in the image \n"
                                                  " 2. When your ready, press S on your keyboard \n 3. Hover your mouse "
                                                  "over the bottom right, like in the image \n 4. When your ready, press "
                                                  "S on your keyboard",
                                             font=("Arial", 16))
    explanationText.pack(padx=10, pady=10)
    warningText = customtkinter.CTkLabel(app, text="DO NOT MOVE YOUR MINESWEEPER WINDOW AFTER THIS STEP",
                                         font=("Arial", 16), text_color="red")
    warningText.pack(padx=10, pady=10)

    # Set the size of the window

    def on_key_press(event):
        global topLeftPosition, bottomRightPosition
        if (event.keysym == "s" or event.keysym == "S") and (topLeftPosition is None):
            mouse_controller = Controller()
            topLeftPosition = mouse_controller.position
            #Debug
            #print(f"Top left position: {topLeftPosition}")

        elif (event.keysym == "s" or event.keysym == "S") and (topLeftPosition is not None):
            mouse_controller = Controller()
            bottomRightPosition = mouse_controller.position
            #Debug
            #print(f"Bottom right position: {bottomRightPosition}")


            # Disable the key press event after capturing both positions
            app.unbind("<KeyPress-s>")
            app.unbind("<KeyPress-S>")
            # Call the function to start the next step
            finalStep()
            windowTitle.destroy()
            imageLabel.destroy()
            explanationText.destroy()
            warningText.destroy()

    # Bind the "S" key to the app
    app.bind("<KeyPress-s>", on_key_press)
    app.bind("<KeyPress-S>", on_key_press)




def finalStep():
    global grid_centers
    createGrid()
    mouse = Controller()
    mouse.position = grid_centers[0][0]
    mouse.click(Button.left, 1)

    time.sleep(0.1)
    printBoxColors()
    turnColorToNo()

    solveMineSweeper()

def solveMineSweeper():
    global value_grid

    # If the value_gripd is empty, print an error message
    if not value_grid:
        print("No values to solve.")
        return
    #Logic part now to solve the minesweeper

    #Rule 0: Repeat until all mines are found, from the user input at the beginning.
    #Rule 1: If a box has a value of X, and only has X non-opened-neighbor, that neighbor is a mine.

    #Rule 2: If a box has a value of X, and we already know that it has neighboring "X" mines,
    # click all other non-opened-neighbors of that box that is not a mine

def turnColorToNo():
    global grid_colors

    if not grid_colors:
        print("No colors to convert.")
        return

    global value_grid
    value_grid = []
    for r, row in enumerate(grid_colors):
        value_row = []
        for c, rgb in enumerate(row):
            if rgb == "unopened":
                value_row.append(0)
            else:
                value_row.append(classify_color(rgb))
        value_grid.append(value_row)

    for r, row in enumerate(value_grid):
        for c, value in enumerate(row):
            print(f"Box [{r}][{c}] has value: {value}")



def createGrid():
    global grid_centers

    # Grid dimensions
    gridWidth = bottomRightPosition[0] - topLeftPosition[0]
    gridHeight = bottomRightPosition[1] - topLeftPosition[1]

    # Number of rows and columns
    num_cols = int(colum_var.get())
    num_rows = int(row_var.get())

    # Size of each box
    boxWidth = gridWidth / num_cols
    boxHeight = gridHeight / num_rows
    """
    # Print grid and box dimensions
    print(f"Grid Width: {gridWidth}, Grid Height: {gridHeight}")
    print(f"Box Width: {boxWidth}, Box Height: {boxHeight}")
    """
    global grid_centers
    # Build grid with center positions
    grid_centers = []

    for row in range(num_rows):
        row_centers = []
        for col in range(num_cols):
            center_x = int(topLeftPosition[0] + (boxWidth / 2) + (col * boxWidth))
            center_y = int(topLeftPosition[1] + (boxHeight / 2) + (row * boxHeight))
            row_centers.append((center_x, center_y))
        grid_centers.append(row_centers)

    """""
    # Debug print
    for r in range(num_rows):
        for c in range(num_cols):
              print(f"Center of box [{r}][{c}]: {grid_centers[r][c]}")
    """""


def printBoxColors():
    global grid_colors

    if not grid_centers:
        print("Grid not initialized yet.")
        return

    grid_colors = []  # Initialize the 2D array to store colors
    screenshot = ImageGrab.grab()  # Take screenshot once for performance

    num_rows = len(grid_centers)
    num_cols = len(grid_centers[0])
    box_height = (bottomRightPosition[1] - topLeftPosition[1]) / num_rows

    white_edge_offset = int(box_height * 0.08)

    for r, row in enumerate(grid_centers):
        color_row = []
        for c, (x, y) in enumerate(row):
            # Sample the top edge to detect the white stripe
            top_edge_y = int(y - (box_height / 2) + white_edge_offset)
            top_edge_color = screenshot.getpixel((x, top_edge_y))

            center_color = screenshot.getpixel((x, y))

            if top_edge_color == (255, 255, 255):  # Detect white edge
                print(f"Box [{r}][{c}] is UNOPENED (has white top edge)")
                color_row.append("unopened")
            else:
                color_row.append(center_color)
                print(f"Box [{r}][{c}] at ({x}, {y}) has color: {center_color}")

        grid_colors.append(color_row)



def classify_color(rgb):
    r, g, b = rgb

    if 185 < r < 195 and 185 < g < 195 and 185 < b < 195:
        return None  # Gray
    elif r > 200:
        return 3  # Red
    elif g > 120:
        return 2  # Green
    elif b > 200:
        return 1  # Blue






# Run app
app.mainloop()
