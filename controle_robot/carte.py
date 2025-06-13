class Carte:
    def __init__(self, objectif='c3', position_actuel='base'):
        self.liste_zones = ['base', 'c0', 'c1', 'e0', 's0', 'c2', 'c3', 'e1', 's1', 'c4']
        self.pos = position_actuel
        self.reversed = False
        self.objectif = objectif

        self.colors = { 'c0': 'jaune',
                        'c1': 'rouge',
                        'c2': 'roze',
                        'c3': 'bleu',
                        'c4': 'vert' }
    
    def get_pos(self):
        return self.pos

    def get_reversed(self):
        return self.reversed
    
    def get_objectif(self):
        return self.objectif
    
    def get_liste_zone(self):
        return self.liste_zones
    
    def get_colors(self):
        return self.colors

    def get_best_container(self):
        if self.pos[0] == 'c':
            pos_int = self.liste_zones.index(self.pos)
            if self.liste_zones[pos_int - 1][0] == 's':
                # Si la première lettre de l'élément précendent l'élément actuel est égale à s (sortie)
                # alors, prendre cette sortie
                return self.liste_zones[pos_int - 1]
            elif self.liste_zones[pos_int - 1] == 'base':
                return 'e0'
            else :
                return self.liste_zones[pos_int + 1]
        elif self.pos == 'base':
            return 's1'
        else :
            return 'already'
    
    def set_pos(self, _pos):
        self.pos = _pos
    
    def set_reversed(self, _reversed):
        self.reversed = _reversed

    def set_objectif(self, _objectif):
        self.objectif = _objectif
        print('objectif : ' + _objectif)
    
    def increase_pos(self):
        pos_int = self.liste_zones.index(self.pos)
        if pos_int >= (len(self.liste_zones) - 1):
            self.pos = self.liste_zones[0]
        else:
            self.pos = self.liste_zones[pos_int + 1]
        print(self.pos, pos_int)
    
    def decrease_pos(self):
        pos_int = self.liste_zones.index(self.pos)
        if pos_int == 0:
            self.pos = self.liste_zones[len(self.liste_zones) - 1]
        else:
            self.pos = self.liste_zones[pos_int - 1]

