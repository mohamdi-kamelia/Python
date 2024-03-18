from Case import Case
import random

class Plateau:
    def __init__(self, lignes, colonnes, mines):
        self.lignes = lignes
        self.colonnes = colonnes
        self.mines = mines        

    def creerPlateau(self):
        self.grille = [[Case() for i in range(self.colonnes)] for j in range(self.lignes)]

    def cliquer(self, x, y):
        coordonnes = []        
        case = self.grille[x][y]
        case.revele = True
        if case.mine:
            print("Perdu")
        else:
            minesAdjacentes = self.verifierVoisins(x, y)
            case.minesAdjacentes = minesAdjacentes
            if minesAdjacentes == 0:
                coordonnes = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
                for coordonne in coordonnes:
                    if coordonne[0] >= 0 and coordonne[0] < self.lignes and coordonne[1] >= 0 and coordonne[1] < self.colonnes:
                        case = self.grille[coordonne[0]][coordonne[1]]
                        if not case.revele:
                            self.cliquer(coordonne[0], coordonne[1])                
        
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
                if case.revele:
                    print(case.minesAdjacentes, end="")
                elif case.mine:
                    print("*", end="")
                else:
                    print("-", end="")
            print()
    
    def placerMine(self, x, y):
        self.grille[x][y].mine = True

    def placerMines(self):
        for i in range(self.mines):
            x = random.randint(0, self.lignes-1)
            y = random.randint(0, self.colonnes-1)
            if not self.grille[x][y].mine and not self.grille[x][y].revele:
                self.placerMine(x, y)
            else:
                i -= 1
        

if __name__ == "__main__":
    plateau = Plateau(10, 10, 10)
    plateau.creerPlateau()
    plateau.placerMines()
    plateau.cliquer(0, 0)
    plateau.afficher()