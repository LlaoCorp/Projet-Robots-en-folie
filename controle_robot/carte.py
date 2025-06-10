class Carte:
    def __init__(self, position_actuel='base'):
        self.liste_zones = ['base', 'c0', 'c1', 'e0', 's0' 'c2', 'c3', 'e1', 's1', 'c4']
        self.pos = position_actuel

        self.colors = { 'c0': 'jaune',
                        'c1': 'rouge',
                        'c2': 'roze',
                        'c3': 'bleu',
                        'c4': 'vert' }
    
    def get_pos_actuel(self):
        return self.pos
    
    def get_liste_zone(self):
        return self.liste_zones
    
    def get_colors(self):
        return self.colors

    def get_best_container(self):
        if self.pos[0] == 'c':
            pos_int = self.liste_zones.index(self.pos[0])
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
    
    def set_pos_actuel(self, pos):
        self.pos = pos
            

