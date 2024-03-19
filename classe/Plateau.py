from Case import Case
import random
import tkinter as tk

class Plateau:
    def __init__(self, difficulte):
        self.difficulte = difficulte
        self.difficultes = {"Facile": (10,10,12), "Moyen": (15,40,45), "Difficile": (20,70,80)}        
        self.lignes, self.colonnes = self.difficultes[difficulte][0], self.difficultes[difficulte][0]
        self.mines = random.randint(self.difficultes[difficulte][1], self.difficultes[difficulte][2])
        self.fenetre = tk.Tk()        
        self.premierCoup = True
        self.creerPlateau()
        self.fenetre.mainloop()
        
    def creerPlateau(self):
        self.grille = [[Case() for i in range(self.colonnes)] for j in range(self.lignes)]
        self.boutons = []
        for ligne in range(self.lignes):
            ligne_boutons = []
            for colonne in range(self.colonnes):
                bouton = tk.Button(self.fenetre, width=6, height=3,bg="white", command=lambda r=ligne, c=colonne: self.cliquer(r, c))
                bouton.grid(row=ligne, column=colonne, sticky="nsew")
                ligne_boutons.append(bouton)
            self.boutons.append(ligne_boutons)
        for i in range(self.lignes):
            self.fenetre.grid_rowconfigure(i, weight=1)
        for i in range(self.colonnes):
            self.fenetre.grid_columnconfigure(i, weight=1)
        for ligne in range(self.lignes):
            for colonne in range(self.colonnes):
                self.boutons[ligne][colonne].bind("<Button-3>", lambda evenement, r=ligne, c=colonne: self.clicDroit(evenement, r, c))

    def cliquer(self, x, y):
        coordonnes = []  
        case = self.grille[x][y]
        case.revele = True
        bouton = self.boutons[x][y]
        if case.mine:
            bouton.config(text="💣", bg="red")
            for i in range(self.lignes):
                for j in range(self.colonnes):
                    if self.grille[i][j].mine:
                        self.boutons[i][j].config(text="💣", bg="red")
        else:
            if self.premierCoup:
                self.premierCoup = False
                self.placerMines()
                self.afficher()
            minesAdjacentes = self.verifierVoisins(x, y)
            if minesAdjacentes == 0:
                bouton.config(text="", bg="lightgray")
                coordonnes = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
                for coordonne in coordonnes:
                    if coordonne[0] >= 0 and coordonne[0] < self.lignes and coordonne[1] >= 0 and coordonne[1] < self.colonnes:
                        case = self.grille[coordonne[0]][coordonne[1]]
                        if not case.revele:
                            self.cliquer(coordonne[0], coordonne[1])
            elif minesAdjacentes > 0:
                bouton.config(text=minesAdjacentes, bg="gray")                    
        
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
                    print("-", end=" ")
            print()
    
    def placerMine(self, x, y):
        self.grille[x][y].mine = True

    def placerMines(self):
        for i in range(self.mines):
            place = False
            while not place:
                x = random.randint(0, self.lignes - 1)
                y = random.randint(0, self.colonnes - 1)
                if not self.grille[x][y].mine and not self.grille[x][y].revele:
                    self.placerMine(x, y)
                    place = True
    
    def clicDroit(self, evenement, x, y):
        case = self.grille[x][y]
        bouton = self.boutons[x][y]

        case.changerEtat()
        if case.drapeau:
            bouton.config(text="🚩", bg="orange")
        elif case.interrogation:
            bouton.config(text="❓", bg="yellow")
        else:
            bouton.config(text="", bg="white")
            
if __name__ == "__main__":
    plateau = Plateau("Difficile")
    