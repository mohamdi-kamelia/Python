import tkinter as tk

class Jeu:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Démineur")
        self.fenetre.geometry("800x600")
        self.CreerBoutons()
        

    def CreerBoutons(self):
        self.boutonRejouer = tk.Button(self.fenetre, text="Rejouer")
        self.boutonQuitter = tk.Button(self.fenetre, text="Quitter", command=self.fenetre.quit)
        self.boutonRejouer.pack()
        self.boutonQuitter.pack()
        self.boutonRejouer.place(x=200, y=500)
        self.boutonQuitter.place(x=600, y=500)

    



if __name__ == "__main__":
    jeu = Jeu()
    jeu.fenetre.mainloop()
    