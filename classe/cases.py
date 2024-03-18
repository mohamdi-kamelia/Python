import tkinter as tk
import random

class MineSweeperGUI:
    def __init__(self, master, rows, cols):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.remaining_time = 120  # Temps total en secondes

        # Frame pour le chronomètre et les boutons
        self.top_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, column=0, columnspan=cols, sticky="ew")

        # Bouton "Retour"
        self.back_button = tk.Button(self.top_frame, text="Retour")
        self.back_button.grid(row=0, column=0, padx=(10, 0))  # Aligner le bouton à gauche

        # Label pour afficher le chronomètre (au milieu)
        self.timer_label = tk.Label(self.top_frame, text="00:00", font=("Helvetica", 18, "bold"))
        self.timer_label.place(relx=0.5, rely=0.5, anchor="center")  # Placer le chronomètre au milieu

        # Bouton "Rejouer"
        self.reset_button = tk.Button(self.top_frame, text="Rejouer")
        self.reset_button.place(relx=0.9, rely=0.5, anchor="e")   # Placer le bouton à droite du chronomètre

        # Ajout d'une rangée vide en dessous des boutons
        tk.Label(self.master).grid(row=1)

        # Créer les boutons de jeu
        self.create_buttons()

        # Démarrer le chronomètre
        self.start_timer()

    def create_buttons(self):
        self.buttons = []
        for row in range(2, self.rows + 2):  # Commencer à partir de la troisième rangée
            button_row = []
            for col in range(self.cols):
                button = tk.Button(self.master, width=6, height=3, command=lambda r=row, c=col: self.button_click(r, c))
                button.grid(row=row, column=col, sticky="nsew")  
                button_row.append(button)
            self.buttons.append(button_row)
        # Configurer les poids de colonne et de ligne pour l'expansion
        for i in range(self.rows + 2):  # Augmenter de deux rangées pour inclure les rangées vides et les boutons
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(self.cols):
            self.master.grid_columnconfigure(i, weight=1)

    def button_click(self, row, col):
        self.buttons[row-2][col].grid_forget()  # Réduire la ligne de 2 car les boutons de jeu commencent à la ligne 2

    def start_timer(self):
        if self.remaining_time > 0:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.remaining_time -= 1
            self.master.after(1000, self.start_timer)
        else:
            self.timer_label.config(text="00:00")

def main():
    root = tk.Tk()
    root.title("Démineur")
    root.geometry("800x600")  
    
    rows = 10
    cols = 10
    
    minesweeper_gui = MineSweeperGUI(root, rows, cols)
    
    root.mainloop()

if __name__ == "__main__":
    main()


