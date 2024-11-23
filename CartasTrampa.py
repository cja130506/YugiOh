from Cartas import Carta
from CartasMonstruos import Monstruo
class Trampa(Carta):
    def __init__(self, nombre, descripcion, atributo):
        super().__init__(self, nombre, descripcion)
        self.atributo = atributo
    def activar(self, monstruo_atacante: Monstruo):
        pass