from Case import Case
import random
import tkinter as tk
from tkinter import messagebox

class ChoixMode:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Choix du mode de difficulté")
        
        label = tk.Label(self.root, text="Choisissez le mode de difficulté :")
        label.pack()

        facile_button = tk.Button(self.root, text="Facile", command=lambda: self.choisir_mode("facile"))
        facile_button.pack()

        moyen_button = tk.Button(self.root, text="Moyen", command=lambda: self.choisir_mode("moyen"))
        moyen_button.pack()

        difficile_button = tk.Button(self.root, text="Difficile", command=lambda: self.choisir_mode("difficile"))
        difficile_button.pack()

    def choisir_mode(self, mode):
        self.mode = mode
        self.root.destroy()

class Plateau:
    def __init__(self, lignes=10, colonnes=10, mode="moyen"):
        self.root = tk.Tk()
        self.mode = mode
        if self.mode == "facile":
            self.lignes = 8
            self.colonnes = 8
            self.mines = 10
        elif self.mode == "moyen":
            self.lignes = 10
            self.colonnes = 10
            self.mines = 20
        elif self.mode == "difficile":
            self.lignes = 12
            self.colonnes = 12
            self.mines = 30
        else:
            raise ValueError("Mode de difficulté non valide")
        self.premierCoup = True
        self.creerPlateau()
        self.root.mainloop()

    def creerPlateau(self):
        self.grille = [[Case() for i in range(self.colonnes)] for j in range(self.lignes)]
        self.buttons = []
        for row in range(self.lignes):
            button_row = []
            for col in range(self.colonnes):
                button = tk.Button(self.root, width=6, height=3,bg="white", command=lambda r=row, c=col: self.cliquer(r, c))
                button.grid(row=row, column=col, sticky="nsew")
                button_row.append(button)
            self.buttons.append(button_row)
        for i in range(self.lignes):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(self.colonnes):
            self.root.grid_columnconfigure(i, weight=1)
        for row in range(self.lignes):
            for col in range(self.colonnes):
                # Bind right-click event to the right_click method with lambda to pass arguments
                self.buttons[row][col].bind("<Button-3>", lambda event, r=row, c=col: self.right_click(event, r, c))

    def cliquer(self, x, y):
        coordonnes = []        
        case = self.grille[x][y]
        case.revele = True
        button = self.buttons[x][y]
        if case.mine:
            button.config(text="BOMBE", bg="red")
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    if self.grille[i][j].mine:
                        self.buttons[i][j].config(text="BOMBE", bg="red")
        else:
            if self.premierCoup:
                self.premierCoup = False
                self.placerMines()
                self.afficher()
            minesAdjacentes = self.verifierVoisins(x, y)
            if minesAdjacentes == 0:
                button.config(text="", bg="lightgray")
                coordonnes = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
                for coordonne in coordonnes:
                    if coordonne[0] >= 0 and coordonne[0] < self.lignes and coordonne[1] >= 0 and coordonne[1] < self.colonnes:
                        case = self.grille[coordonne[0]][coordonne[1]]
                        if not case.revele:
                            self.cliquer(coordonne[0], coordonne[1])
            elif minesAdjacentes > 0:
                button.config(text=minesAdjacentes, bg="gray")                    
        
    def verifierVoisins(self, x, y):
        minesAdjacentes = 0
        coordonnes = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
        for coordonne in coordonnes:
            if coordonne[0] >= 0 and coordonne[0] < self.lignes and coordonne[1] >= 0 and coordonne[1] < self.colonnes:
                case = self.grille[coordonne[0]][coordonne[1]]
                if case.mine:
                    minesAdjacentes += 1
        return minesAdjacentes

    def afficher(self):
        for ligne in self.grille:
            for case in ligne:
                if case.mine:
                    print("B", end=" ")
                else:
                    print("0", end=" ")
            print()
    
    def placerMine(self, x, y):
        self.grille[x][y].mine = True

    def placerMines(self):
        for i in range(self.mines):
            placed = False
            while not placed:
                x = random.randint(0, self.lignes - 1)
                y = random.randint(0, self.colonnes - 1)
                if not self.grille[x][y].mine and not self.grille[x][y].revele:
                    self.placerMine(x, y)
                    placed = True
    
    def right_click(self, event, x, y):
        case = self.grille[x][y]
        button = self.buttons[x][y]
        if not case.revele:
            if case.interrogation:
                # Remove question mark
                case.interrogation = False
                button.config(text="", bg="white")               
                
            elif case.drapeau:
                # Remove flag
                button.config(text="?", bg="yellow")
                case.drapeau = False
                case.interrogation = True

            else:
                # Place flag
                button.config(text="🚩", bg="orange")
                case.drapeau = True

if __name__ == "__main__":
    choix = ChoixMode()
    choix.root.mainloop()

    if choix.mode:
        plateau = Plateau(mode=choix.mode)
    else:
        messagebox.showerror("Erreur", "Aucun mode de difficulté sélectionné. Le jeu va se fermer.")