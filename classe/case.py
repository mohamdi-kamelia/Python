import tkinter as tk
import random
from collections import deque

class MineSweeperGUI:
    def __init__(self, master, rows, cols, difficulty):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.difficulty = difficulty
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        self.mines = set()  # Utilisé pour stocker les positions des mines
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.master, width=6, height=3, command=lambda r=row, c=col: self.button_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

        self.place_mines()

    def place_mines(self):
        num_mines = 0
        if self.difficulty == "facile":
            num_mines = random.randint(6, 8)
        elif self.difficulty == "moyen":
            num_mines = random.randint(8, 10)
        elif self.difficulty == "difficile":
            num_mines = random.randint(10, 12)

        mines_placed = 0
        while mines_placed < num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in self.mines:
                self.mines.add((row, col))
                mines_placed += 1

    def button_click(self, row, col):
        if (row, col) in self.mines:
            self.buttons[row][col].config(bg="red")  # Affiche une couleur de fond rouge si une mine est trouvée
            print("Vous avez cliqué sur une mine !")
        else:
            self.buttons[row][col].config(text="O", bg="green")  # Affiche un cercle vert sinon

            # Algorithme de file pour révéler les cases vides adjacentes
            queue = deque([(row, col)])
            revealed = set()  # Utilisé pour stocker les cases déjà révélées
            while queue:
                r, c = queue.popleft()
                if (r, c) in revealed:
                    continue
                revealed.add((r, c))
                minesAdjacentes = self.verifierVoisins(r, c)
                if minesAdjacentes == 0:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in revealed:
                                queue.append((nr, nc))
                self.reveal_button(r, c, minesAdjacentes)

    def verifierVoisins(self, row, col):
        minesAdjacentes = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) in self.mines:
                    minesAdjacentes += 1
        return minesAdjacentes

    def reveal_button(self, row, col, minesAdjacentes):
        if minesAdjacentes > 0:
            self.buttons[row][col].config(text=str(minesAdjacentes), bg="green")
        else:
            self.buttons[row][col].config(bg="green")
            self.auto_reveal_adjacent_buttons(row, col)

    def auto_reveal_adjacent_buttons(self, row, col):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.buttons[nr][nc]["bg"] != "red" and self.buttons[nr][nc]["text"] == "":
                        self.buttons[nr][nc].invoke()  # Clique automatiquement sur le bouton
                        self

def main():
    root = tk.Tk()
    root.title("Démineur")
    root.geometry("800x600")  # Redimensionner la fenêtre à la même taille que la fenêtre des bombes
    
    rows = 10
    cols = 10
    difficulty = "difficile"  # Changez cela en "moyen" ou "difficile" selon le niveau de difficulté
    
    minesweeper_gui = MineSweeperGUI(root, rows, cols, difficulty)
    
    root.mainloop()

if __name__ == "__main__":
    main()
