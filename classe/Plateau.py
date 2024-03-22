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
        self.difficultes = {"Facile": (10,10,12), "Moyen": (14,20,25), "Difficile": (20,40,60)}        
        self.lignes, self.colonnes = self.difficultes[difficulte][0], self.difficultes[difficulte][0]
        self.mines = random.randint(self.difficultes[difficulte][1], self.difficultes[difficulte][2])
        self.son_bombe = "images/EXPLReal_Explosion 2 (ID 1808)_LS.wav" 
        self.fenetre = tk.Tk()        
        self.premier_coup = True
        self.drapeaux = 0
        self.interrogations = 0
        self.chrono = 0
        self.creer_plateau()
        self.fenetre.mainloop()
        
        
    def creer_plateau(self):
        # Création d'un frame principal avec fond noir
        self.cadre_principal = tk.Frame(self.fenetre, bg="white")
        self.cadre_principal.pack(expand=True, fill="both", padx=10, pady=10)

        # Création de cadres noirs pour entourer la grille
        cadre_gauche = tk.Frame(self.cadre_principal, bg="black")
        cadre_gauche.grid(row=0, column=0, rowspan=self.lignes, sticky="nsew")

        cadre_droit = tk.Frame(self.cadre_principal, bg="black")
        cadre_droit.grid(row=0, column=self.colonnes + 1, rowspan=self.lignes, sticky="nsew")

        cadre_haut = tk.Frame(self.cadre_principal, bg="black")  # Changement ici
        cadre_haut.grid(row=0, column=0, columnspan=self.colonnes + 2, sticky="nsew")


        # Création de la grille
        self.grille = [[Case() for i in range(self.colonnes)] for j in range(self.lignes)]
        self.boutons = []

        for ligne in range(self.lignes):
            ligne_boutons = []
            for colonne in range(self.colonnes):
                bouton = tk.Button(self.cadre_principal, width=6, height=3,bg="white", command=lambda r=ligne, c=colonne: self.cliquer(r, c))
                bouton.grid(row=ligne, column=colonne + 1, sticky="nsew")  # Changement de la colonne
                ligne_boutons.append(bouton)
            self.boutons.append(ligne_boutons)

        for ligne in range(self.lignes):
            self.cadre_principal.grid_rowconfigure(ligne, weight=1)

        for colonne in range(self.colonnes):
            self.cadre_principal.grid_columnconfigure(colonne + 1, weight=1)  # Changement de la colonne

        for ligne in range(self.lignes):
            for colonne in range(self.colonnes):
                self.boutons[ligne][colonne].bind("<Button-3>", lambda evenement, r=ligne, c=colonne: self.clic_droit(evenement, r, c))

        # Création d'un frame pour les boutons en bas
        cadre_bas = tk.Frame(self.cadre_principal, bg="white")
        cadre_bas.grid(row=self.lignes, column=0, columnspan=self.colonnes + 2, sticky="nsew")

        self.bouton_rejouer = tk.Button(cadre_bas, text="🙂", command=self.rejouer, font=("Helvetica", 24))
        self.bouton_rejouer.place(relx=0.5, rely=0.5, anchor="center")
        self.bouton_rejouer.config(bg="white")
        self.bouton_rejouer.config(width=6, height=3) 

        self.chrono_label = tk.Label(cadre_bas, text="0:00", font=("Helvetica", 18, "bold"))
        self.chrono_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.chrono_label.config(bg="white")

        self.drapeaux_label = tk.Label(cadre_bas, text=f"🚩: {self.drapeaux}", font=("Helvetica", 18, "bold"))
        self.drapeaux_label.place(relx=0.8, rely=0.5, anchor="w") 
        self.drapeaux_label.config(bg="gray")

        self.interrogations_label = tk.Label(cadre_bas, text=f"❓: {self.interrogations}", font=("Helvetica", 18, "bold"))
        self.interrogations_label.place(relx=0.73, rely=0.5, anchor="w") 
        self.interrogations_label.config(bg="gray")

        self.mines_label = tk.Label(cadre_bas, text=f"💣: {self.mines}", font=("Helvetica", 18, "bold"))
        self.mines_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.mines_label.config(bg="red")



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
            self.arreter_chrono()
            self.defaite()
        else:
            if self.premier_coup:
                self.premier_coup = False
                self.placer_mines()
                self.afficher()
                self.lancer_chrono()
            mines_adjacentes = self.verifier_voisins(x, y)
            if mines_adjacentes == 0:
                bouton.config(text="", bg="lightgray")
                coordonnes = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
                for coordonne in coordonnes:
                    if coordonne[0] >= 0 and coordonne[0] < self.lignes and coordonne[1] >= 0 and coordonne[1] < self.colonnes:
                        case = self.grille[coordonne[0]][coordonne[1]]
                        if not case.revele:
                            self.cliquer(coordonne[0], coordonne[1])
            elif mines_adjacentes > 0:
                bouton.config(text=mines_adjacentes, bg="gray")
            if self.verifier_victoire():
                self.arreter_chrono()
                messagebox.showinfo("Gagné", f"Vous avez gagné en {self.chrono // 60} minutes et {self.chrono % 60} secondes !")
                self.fenetre.destroy()

    def verifier_voisins(self, x, y):
        mines_adjacentes = 0
        coordonnes = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
        for coordonne in coordonnes:
            if coordonne[0] >= 0 and coordonne[0] < self.lignes and coordonne[1] >= 0 and coordonne[1] < self.colonnes:
                case = self.grille[coordonne[0]][coordonne[1]]
                if case.mine:
                    mines_adjacentes += 1
        return mines_adjacentes

    def afficher(self):
        for ligne in self.grille:
            for case in ligne:
                if case.mine:
                    print("B", end=" ")
                else:
                    print("-", end=" ")
            print()

    def placer_mines(self):
        for i in range(self.mines):
            place = False
            while not place:
                x = random.randint(0, self.lignes - 1)
                y = random.randint(0, self.colonnes - 1)
                if not self.grille[x][y].mine and not self.grille[x][y].revele:
                    self.grille[x][y].mine = True
                    place = True
    
    def clic_droit(self, evenement, x, y):
        case = self.grille[x][y]
        bouton = self.boutons[x][y]

        if not case.revele:
            case.changer_etat()
            if case.drapeau:
                bouton.config(text="🚩", bg="orange")
                self.drapeaux += 1
                self.drapeaux_label.config(text=f"🚩: {self.drapeaux}")
            elif case.interrogation:
                bouton.config(text="❓", bg="yellow")
                self.drapeaux -= 1
                self.interrogations += 1
                self.drapeaux_label.config(text=f"🚩: {self.drapeaux}")
                self.interrogations_label.config(text=f"❓: {self.interrogations}")
            else:
                bouton.config(text="", bg="white")
                self.interrogations -= 1
                self.interrogations_label.config(text=f"❓: {self.interrogations}")

    def defaite(self):
        winsound.PlaySound(self.son_bombe, winsound.SND_FILENAME)
        messagebox.showinfo("Perdu", "Vous avez perdu !")
        self.fenetre.destroy()

    def verifier_victoire(self):
        for ligne in self.grille:
            for case in ligne:
                if not case.mine and not case.revele:
                    return False
        self.sauvegarder_scores() 
        return True
    
    def rejouer(self):
        self.fenetre.destroy()
        plateau = Plateau(self.difficulte)

    def lancer_chrono(self):
        self.chrono += 1
        minutes = self.chrono // 60
        secondes = self.chrono % 60
        self.chrono_label.config(text=f"{minutes:02d}:{secondes:02d}")
        self.fenetre.after(1000, self.lancer_chrono)

    def arreter_chrono(self):
        self.fenetre.after_cancel(self.lancer_chrono)
        self.chrono_label.destroy()

    def sauvegarder_scores(self):
        score_data = {
            "pseudo": self.pseudo,
            "difficulte": self.difficulte,
            "temps": f"{self.chrono // 60} minutes et {self.chrono % 60} secondes"
        }

        with open ("scores.json", "r") as file:
            scores = json.load(file)

        scores.append(score_data)

        with open("scores.json", "w") as file:
            json.dump(scores, file, indent=4)

    
            
if __name__ == "__main__":
    plateau = Plateau("Facile")