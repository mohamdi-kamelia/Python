import tkinter as tk
from PIL import Image, ImageTk
from Plateau import *
import json
from tkinter import messagebox

class PageAccueil(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Démineur - Page d'Accueil")
        self.geometry("800x600")

        # Charger l'image de fond
        self.background_image = Image.open("images/Minimalist Portfolio Cover Page.png")
        self.background_image = self.background_image.resize((800, 600), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Créer un Canvas pour afficher l'image de fond
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Afficher l'image de fond
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Positionnement des boutons
        y_coord = 0.45
        button_spacing = 0.12

        # Boutons pour les niveaux de difficulté
        self.bouton_demarrer = tk.Button(self.canvas, text="Mode Facile", command=self.demarrer_jeu, font=("Times New Roman", 18, "italic bold"), fg="white", bg="black")
        self.bouton_difficultes = tk.Button(self.canvas, text='Mode Difficile', command=self.mode_difficultes, font=("Times New Roman", 18, "italic bold"), fg="white", bg="black")
        self.bouton_mode_moyen = tk.Button(self.canvas , text="Mode Moyen", command=self.mode_moyen , font=("Times New Roman", 18, "italic bold"), fg="white", bg="black" )
        self.bouton_quitter = tk.Button(self.canvas, text="Quitter", command=self.quitter_jeu, font=("Times New Roman", 18, "italic bold"), fg="white", bg="black")

        # Placement des boutons
        self.bouton_demarrer.place(relx=0.5, rely=y_coord, anchor=tk.CENTER)
        self.bouton_mode_moyen.place(relx=0.5, rely=y_coord + button_spacing, anchor=tk.CENTER)
        self.bouton_difficultes.place(relx=0.5, rely=y_coord + 2 * button_spacing, anchor=tk.CENTER)
        self.bouton_quitter.place(relx=0.5, rely=y_coord + 3 * button_spacing, anchor=tk.CENTER)

        # Ajouter un bouton pour afficher les scores
        self.image_scores = Image.open("images/score.png")  # Modifier le chemin d'accès à votre image
        self.image_scores = self.image_scores.resize((80, 50), Image.LANCZOS)
        self.image_scores = ImageTk.PhotoImage(self.image_scores)
        self.bouton_scores = tk.Button(self.canvas, image=self.image_scores, command=self.afficher_scores)
        self.bouton_scores.place(relx=1.0, rely=1.0, anchor=tk.SE)

        # Entrée pour le pseudo
        self.pseudo = tk.Entry(self.canvas, font=("Times New Roman", 18, "bold"), fg="black", bg="white")
        self.pseudo.place(relx=0.5, rely=y_coord - 1 * button_spacing, anchor=tk.CENTER)
        self.pseudo.insert(0, "Entrez votre pseudo")
        self.pseudo.bind("<FocusIn>", self.clear_entry)

    def mode_difficultes(self):
        pseudo = self.pseudo.get()
        self.destroy()
        plateau = Plateau("Difficile", pseudo) 
        page_accueil = PageAccueil()
        page_accueil.mainloop()

    def mode_moyen(self):
        pseudo = self.pseudo.get()
        self.destroy()
        plateau = Plateau("Moyen", pseudo)  
        page_accueil = PageAccueil()
        page_accueil.mainloop()

    def quitter_jeu(self):
        self.destroy()

    def demarrer_jeu(self):
        pseudo = self.pseudo.get()
        self.destroy()
        plateau = Plateau("Facile", pseudo)
        page_accueil = PageAccueil()
        page_accueil.mainloop()
        
    def clear_entry(self, event):
        self.pseudo.delete(0, tk.END)
        self.pseudo.config(fg="black")
        self.pseudo.unbind("<FocusIn>")
        
    def afficher_scores(self):
        # Charge les scores à partir du fichier JSON
        try:
            with open("scores.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            # Si le fichier n'existe pas encore
            messagebox.showinfo("Scores", "Aucun score enregistré.")
            return

        # Affiche les scores dans une boîte de dialogue
        score_text = "Scores :\n"
        for score in scores:
            pseudo = score["pseudo"]
            temps = score["temps"]
            score_text += f"{pseudo}: {temps}\n"

        messagebox.showinfo("Scores", score_text)

if __name__ == "__main__":
    page_accueil = PageAccueil()
    page_accueil.mainloop()
