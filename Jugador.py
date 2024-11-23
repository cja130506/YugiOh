class Jugador():
    def __init__(self, nombre, puntos, deck, mano, tablero):
        self.nombre = nombre
        self.puntos = puntos
        self.deck = deck
        self.mano = mano
        self.tablero = tablero
    def generar_deck(self):
        return self.deck
    def robar_cartas(self, cantidad):
        pass
    