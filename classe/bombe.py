import tkinter as tk
import random

class BombeGUI:
    def __init__(self, master, niveau_difficulte):
        self.master = master
        self.niveau_difficulte = niveau_difficulte
        
        self.create_grid()
        self.create_bombes()

    def create_grid(self):
        self.cells = []
        for row in range(10):
            row_cells = []
            for col in range(10):
                cell = tk.Frame(self.master, width=80, height=60, borderwidth=0.5, relief="solid")
                cell.grid(row=row, column=col)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def create_bombes(self):
        num_bombes = 0
        if self.niveau_difficulte == "facile":
            num_bombes = random.randint(6, 8)
        elif self.niveau_difficulte == "moyen":
            num_bombes = random.randint(8, 10)
        elif self.niveau_difficulte == "difficile":
            num_bombes = random.randint(10, 12)
        
        for _ in range(num_bombes):
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            cell = self.cells[row][col]
            img = tk.PhotoImage(file="images/bombe.png")  # Assurez-vous que bombe.png est dans le même répertoire que votre script
            img = img.subsample(3, 3)  # Redimensionner l'image à un tiers de sa taille d'origine
            label = tk.Label(cell, image=img)
            label.image = img
            label.place(relx=0.5, rely=0.5, anchor="center")  # Positionner l'image au centre de la cellule

def main():
    root = tk.Tk()
    root.title("Bombe")
    root.geometry("800x600")  # Redimensionner la fenêtre à 800x600 pixels

    niveau_difficulte = "facile"  # Changez cela en "moyen" ou "difficile" selon le niveau de difficulté

    bombe_gui = BombeGUI(root, niveau_difficulte)
    
    root.mainloop()

if __name__ == "__main__":
    main()
