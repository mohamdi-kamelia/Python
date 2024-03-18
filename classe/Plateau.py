from Case import Case

class Plateau:
    def __init__(self, lignes, colonnes, mines):
        self.lignes = lignes
        self.colonnes = colonnes
        self.mines = mines
        

    def creerPlateau(self):
        self.grille = [[Case() for i in range(self.colonnes)] for j in range(self.lignes)]

    def cliquer(self, x, y):        
        case = self.grille[x][y]
        case.revele = True
        if case.mine:
            print("Perdu")
        if self.verifierVoisins(x, y) == 0:
            self.cliquerVoisins(x, y)
        else:
            
        
    def verifierVoisins(self, x, y):
        casesAdjacentes = []
        minesAdjacentes = 0
        coordonnes = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
        for coordonne in coordonnes:
            if coordonne[0] >= 0 and coordonne[0] < self.lignes and coordonne[1] >= 0 and coordonne[1] < self.colonnes:
                case = self.grille[coordonne[0]][coordonne[1]]
                casesAdjacentes.append(case)
                if case.mine:
                    minesAdjacentes += 1
        return minesAdjacentes


    def afficher(self):
        for ligne in self.grille:
            for case in ligne:
                if case.revele:
                    print("X", end="")
                else:
                    print("-", end="")
            print()
    
    def placerMine(self, x, y):
        self.grille[x][y].mine = True
        

if __name__ == "__main__":
    plateau = Plateau(10, 10, 10)
    plateau.creerPlateau()
    plateau.placerMine(2, 3)
    plateau.placerMine(2, 5)
    plateau.cliquer(2, 4)
    plateau.afficher()