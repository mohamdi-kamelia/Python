from Case import Case
import random
import tkinter as tk
from tkinter import messagebox
import winsound
import json
class Plateau:
    def __init__(self, difficulte, pseudo):
        self.difficulte = difficulte
        self.pseudo = pseudo
        self.difficultes = {"Facile": (10,10,12), "Moyen": (14,40,45), "Difficile": (20,70,80)}        
        self.lignes, self.colonnes = self.difficultes[difficulte][0], self.difficultes[difficulte][0]
        self.mines = random.randint(self.difficultes[difficulte][1], self.difficultes[difficulte][2])
        self.son_bombe = "images/EXPLReal_Explosion 2 (ID 1808)_LS.wav" 
        self.fenetre = tk.Tk()        
        self.premierCoup = True
        self.drapeaux = 0
        self.interrogations = 0
        self.chrono = 0
        self.creerPlateau()
        self.fenetre.mainloop()
        
        
    def creerPlateau(self):
        # Création d'un frame principal avec fond noir
        self.main_frame = tk.Frame(self.fenetre, bg="white")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Création de cadres noirs pour entourer la grille
        left_side_frame = tk.Frame(self.main_frame, bg="black")
        left_side_frame.grid(row=0, column=0, rowspan=self.lignes, sticky="nsew")

        right_side_frame = tk.Frame(self.main_frame, bg="black")
        right_side_frame.grid(row=0, column=self.colonnes + 1, rowspan=self.lignes, sticky="nsew")

        top_frame = tk.Frame(self.main_frame, bg="black")  # Changement ici
        top_frame.grid(row=0, column=0, columnspan=self.colonnes + 2, sticky="nsew")


        # Création de la grille
        self.grille = [[Case() for i in range(self.colonnes)] for j in range(self.lignes)]
        self.boutons = []

        for ligne in range(self.lignes):
            ligne_boutons = []
            for colonne in range(self.colonnes):
                bouton = tk.Button(self.main_frame, width=6, height=3,bg="white", command=lambda r=ligne, c=colonne: self.cliquer(r, c))
                bouton.grid(row=ligne, column=colonne + 1, sticky="nsew")  # Changement de la colonne
                ligne_boutons.append(bouton)
            self.boutons.append(ligne_boutons)

        for ligne in range(self.lignes):
            self.main_frame.grid_rowconfigure(ligne, weight=1)

        for colonne in range(self.colonnes):
            self.main_frame.grid_columnconfigure(colonne + 1, weight=1)  # Changement de la colonne

        for ligne in range(self.lignes):
            for colonne in range(self.colonnes):
                self.boutons[ligne][colonne].bind("<Button-3>", lambda evenement, r=ligne, c=colonne: self.clicDroit(evenement, r, c))

        # Création d'un frame pour les boutons en bas
        bottom_frame = tk.Frame(self.main_frame, bg="white")
        bottom_frame.grid(row=self.lignes, column=0, columnspan=self.colonnes + 2, sticky="nsew")

        self.boutonRejouer = tk.Button(bottom_frame, text="🙂", command=self.rejouer, font=("Helvetica", 24))
        self.boutonRejouer.place(relx=0.5, rely=0.5, anchor="center")
        self.boutonRejouer.config(bg="white")
        self.boutonRejouer.config(width=6, height=3) 

        self.chronoLabel = tk.Label(bottom_frame, text="0:00", font=("Helvetica", 18, "bold"))
        self.chronoLabel.pack(side=tk.LEFT, padx=5, pady=5)
        self.chronoLabel.config(bg="white")

        self.drapeauxLabel = tk.Label(bottom_frame, text=f"🚩: {self.drapeaux}", font=("Helvetica", 18, "bold"))
        self.drapeauxLabel.place(relx=0.8, rely=0.5, anchor="w") 
        self.drapeauxLabel.config(bg="gray")

        self.interrogationsLabel = tk.Label(bottom_frame, text=f"❓: {self.interrogations}", font=("Helvetica", 18, "bold"))
        self.interrogationsLabel.place(relx=0.73, rely=0.5, anchor="w") 
        self.interrogationsLabel.config(bg="gray")

        self.minesLabel = tk.Label(bottom_frame, text=f"💣: {self.mines}", font=("Helvetica", 18, "bold"))
        self.minesLabel.pack(side=tk.LEFT, padx=5, pady=5)
        self.minesLabel.config(bg="red")



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
            self.arreterChrono()
            self.defaite()
        else:
            if self.premierCoup:
                self.premierCoup = False
                self.placerMines()
                self.afficher()
                self.lancerChrono()
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
            if self.verifierVictoire():
                self.arreterChrono()
                messagebox.showinfo("Gagné", f"Vous avez gagné en {self.chrono // 60} minutes et {self.chrono % 60} secondes !")
                self.fenetre.destroy()

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
            self.drapeaux += 1
            self.drapeauxLabel.config(text=f"🚩: {self.drapeaux}")
        elif case.interrogation:
            bouton.config(text="❓", bg="yellow")
            self.drapeaux -= 1
            self.interrogations += 1
            self.drapeauxLabel.config(text=f"🚩: {self.drapeaux}")
            self.interrogationsLabel.config(text=f"❓: {self.interrogations}")
        else:
            bouton.config(text="", bg="white")
            self.interrogations -= 1
            self.interrogationsLabel.config(text=f"❓: {self.interrogations}")

    def defaite(self):
        winsound.PlaySound(self.son_bombe, winsound.SND_FILENAME)
        messagebox.showinfo("Perdu", "Vous avez perdu !")
        self.fenetre.destroy()

    def verifierVictoire(self):
        for ligne in self.grille:
            for case in ligne:
                if not case.mine and not case.revele:
                    return False
        self.sauvegarder_scores() 
        return True
    
    def rejouer(self):
        self.fenetre.destroy()
        plateau = Plateau(self.difficulte)

    def lancerChrono(self):
        self.chrono += 1
        minutes = self.chrono // 60
        seconds = self.chrono % 60
        self.chronoLabel.config(text=f"{minutes:02d}:{seconds:02d}")
        self.fenetre.after(1000, self.lancerChrono)

    def arreterChrono(self):
        self.fenetre.after_cancel(self.lancerChrono)
        self.chronoLabel.destroy()
    def sauvegarder_scores(self):
        score_data = {
            "pseudo": self.pseudo,
            "difficulte": self.difficulte,
            "temps": f"{self.chrono // 60} minutes et {self.chrono % 60} secondes"
        }

        with open("score.json", "a") as f:
            json.dump(score_data, f)
            f.write("\n")
    
            
if __name__ == "__main__":
    plateau = Plateau("Facile")