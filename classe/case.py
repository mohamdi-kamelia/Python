class Case:
    def __init__(self, revele=False, mine=False, minesAdjacentes=0, drapeau=False, interrogation=False):
        self.revele = revele
        self.mine = mine
        self.minesAdjacentes = minesAdjacentes
        self.drapeau = drapeau
        self.interrogation = interrogation

    def changerEtat(self):
        if not self.revele:
            if self.drapeau:
                self.drapeau = False
                self.interrogation = True
            elif self.interrogation:
                self.interrogation = False
            else:
                self.drapeau = True   
    