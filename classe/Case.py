class Case:
    def __init__(self, revele=False, mine=False, mines_adjacentes=0, drapeau=False, interrogation=False):
        self.revele = revele
        self.mine = mine
        self.mines_adjacentes = mines_adjacentes
        self.drapeau = drapeau
        self.interrogation = interrogation

    def changer_etat(self):
        if not self.revele:
            if self.drapeau:
                self.drapeau = False
                self.interrogation = True
            elif self.interrogation:
                self.interrogation = False
            else:
                self.drapeau = True