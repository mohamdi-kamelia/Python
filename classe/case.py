import tkinter as tk
import random

class Case:
    def __init__(self, master, rows, cols):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.master, width=6, height=3, command=lambda r=row, c=col: self.button_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def button_click(self, row, col):
        self.buttons[row][col].grid_forget()

def main():
    root = tk.Tk()
    root.title("Démineur")
    root.geometry("800x600")  # Redimensionner la fenêtre à la même taille que la fenêtre des bombes
    
    rows = 10
    cols = 10
    
    minesweeper_gui = Case(root, rows, cols)
    
    root.mainloop()

if __name__ == "__main__":
    main()
