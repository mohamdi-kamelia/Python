import tkinter as tk
from PIL import Image, ImageTk
from Plateau import *
class PageAccueil(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Démineur - Page d'Accueil")
        self.geometry("800x600")

        # Charger l'image et la redimensionner pour qu'elle corresponde à la taille de la fenêtre
        self.background_image = Image.open("images/backround.jpg")
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

        self.bouton_demarrer = tk.Button(self.canvas, text="Jouer", command=self.demarrer_jeu, font=("Times New Roman", 18, "bold"), fg="red", bg="black")
        self.bouton_difficultes = tk.Button(self.canvas, text='Mode Difficultés', command=self.mode_difficultes, font=("Times New Roman", 18, "bold"), fg="red", bg="black")
        self.bouton_quitter = tk.Button(self.canvas, text="Quitter", command=self.quitter_jeu, font=("Times New Roman", 18, "bold"), fg="red", bg="black")

        self.bouton_demarrer.place(relx=0.5, rely=y_coord, anchor=tk.CENTER)
        self.bouton_difficultes.place(relx=0.5, rely=y_coord + button_spacing, anchor=tk.CENTER)
        self.bouton_quitter.place(relx=0.5, rely=y_coord + 2 * button_spacing, anchor=tk.CENTER)

    def mode_difficultes(self):
        print("Mode difficultés...")

    def quitter_jeu(self):
        self.destroy()

    def demarrer_jeu(self):
        self.destroy()
        choix = ChoixMode()  
        choix.root.mainloop()
        if choix.mode:
            plateau = Plateau(mode=choix.mode)
        else:
            messagebox.showerror("Erreur", "Aucun mode de difficulté sélectionné. Le jeu va se fermer.")
if __name__ == "__main__":
    page_accueil = PageAccueil()
    page_accueil.mainloop()
