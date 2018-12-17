import random

TrucoLevels = {
    0 : 'Base',
    1 : 'Truco',
    2 : 'Re truco',
    3 : 'Vale 4'
}

EnvidoLevels = {
    0 : 'Sin Envido',
    1 : 'Envido',
    2 : 'Falta Envido'
}

class Player:
    def __init__(self, name):
        self.nombre = name
        self.mano = []
        self.mano_inicial = []

class Partida:

    def __init__(self, players):
        self.players = {}
        for name in players:
            self.players[name] = Player(name)
        self.n_players = len(players)
        self.who_is_turno = 0
        self.truco_state = 0
        self.envido_state = 0
        self.first_turno = True

    def iniciar_partida(self, repartidor):
        self.recojer_mazo()
        self.mezclar_mazo()
        self.repartir()
        self.who_is_turno = list(self.players).index(repartidor)
        self.turno()

    def recojer_mazo(self):
        self.mazo = []
        palos = ['Basto', 'Espada', 'Oro', 'Copa']
        valores = [v for v in [1,2,3,4,5,6,7,10,11,12]]
        self.mazo = [(valor, palo) for palo in palos for valor in valores]

    def mezclar_mazo(self):
        mixed_mazo = []
        while len(self.mazo) > 0:
            carta = random.choice(self.mazo)
            mixed_mazo.append(carta)
            self.mazo.remove(carta)
        self.mazo = mixed_mazo

    def repartir(self):
        n = 0
        for player in self.players:
            self.players[player].mano = self.mazo[n:3+n]
            n = n + 3
            self.players[player].mano_inicial = self.players[player].mano.copy()

    def mostrar_mano(self, player):
        return self.players[player].mano_inicial

    def mano_actual(self, player):
        return self.players[player].mano

    def turno(self):
        self.who_is_turno = (self.who_is_turno + 1)%self.n_players
        return list(self.players)[self.who_is_turno]

    def get_state(self):
        return [self.truco_state, self.envido_state]

    def cantar(self, envido, truco):
        self.truco_state = TrucoLevels[truco]
        self.envido_state = EnvidoLevels[envido]

    def jugar_carta(self, player, carta):
        carta_jugada = self.players[player].mano[carta]
        self.players[player].mano[carta] = (0,0)
        return carta_jugada

    def quitar_jugador(self, player):
        self.players.pop(player, None)