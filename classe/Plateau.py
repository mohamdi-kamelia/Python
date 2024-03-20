from Case import Case
import random
import tkinter as tk


class Plateau:
    def __init__(self, difficulte):
        self.root = tk.Tk()
        self.difficulte = difficulte
        self.difficultes = {"Facile": (10,10,12), "Moyen": (15,40,45), "Difficile": (20,70,80)}        
        self.lignes, self.colonnes = self.difficultes[difficulte][0], self.difficultes[difficulte][0]
        self.mines = random.randint(self.difficultes[difficulte][1], self.difficultes[difficulte][2])
        self.premierCoup = True
        self.creerPlateau()
        self.root.mainloop()
    def creerPlateau(self):
        self.grille = [[Case() for i in range(self.colonnes)] for j in range(self.lignes)]
        self.buttons = []
        for row in range(self.lignes):
            button_row = []
            for col in range(self.colonnes):
                button = tk.Button(self.root, width=6, height=3,font=("Arial", 16),bg="white", command=lambda r=row, c=col: self.cliquer(r, c))
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
            button.config(text="💣", bg="red")
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    if self.grille[i][j].mine:
                        self.buttons[i][j].config(text="💣", bg="red")
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