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
        self.label_bienvenue = tk.Label(self.canvas, text="Bienvenue au démineur", font=("Times New Roman", 30, "italic bold"), fg="white", bg="black")
        self.label_bienvenue.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        # Positionnement des boutons
        y_coord = 0.45
        button_spacing = 0.12

        self.bouton_demarrer = tk.Button(self.canvas, text="Mode Facile", command=self.demarrer_jeu, font=("Times New Roman", 18, "bold"), fg="white", bg="black")
        self.bouton_difficultes = tk.Button(self.canvas, text='Mode Difficile', command=self.mode_difficultes, font=("Times New Roman", 18, "bold"), fg="white", bg="black")
        self.bouton_quitter = tk.Button(self.canvas, text="Quitter", command=self.quitter_jeu, font=("Times New Roman", 18, "bold"), fg="white", bg="black")
        self.bouton_mode_moyen = tk.Button(self.canvas , text="Mode Moyen", command=self.mode_moyen , font=("Times New Roman", 18, "bold"), fg="white", bg="black" )
    
        self.bouton_demarrer.place(relx=0.5, rely=y_coord, anchor=tk.CENTER)
        self.bouton_difficultes.place(relx=0.5 ,rely=y_coord + 2 * button_spacing, anchor =tk.CENTER)
        self.bouton_quitter.place(relx=0.5, rely=y_coord + 3 * button_spacing, anchor=tk.CENTER)
        self.bouton_mode_moyen.place(relx=0.5, rely=y_coord + button_spacing, anchor=tk.CENTER)
    def mode_difficultes(self):
        self.destroy()
        plateau = Plateau("Difficile") 

    def mode_moyen(self):
        self.destroy()
        plateau = Plateau("Moyen")  

    def quitter_jeu(self):
        self.destroy()

    def demarrer_jeu(self):
        self.destroy()
        plateau = Plateau("Facile")  
if __name__ == "__main__":
    page_accueil = PageAccueil()
    page_accueil.mainloop()
