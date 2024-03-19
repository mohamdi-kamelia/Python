class Case:
    def __init__(self, revele=False, mine=False, minesAdjacentes=0, drapeau=False, interrogation=False):
        self.revele = revele
        self.mine = mine
        self.minesAdjacentes = minesAdjacentes
        self.drapeau = drapeau
        self.interrogation = interrogation
        
    