from Cartas import Carta
from CartasMonstruos import Monstruo
class CartaMagica(Carta):
    def __init__(self, nombre, descripcion, tipo_monstruo , efecto, incremento):
        super().__init__(nombre, descripcion)
        self.tipo_monstruo = tipo_monstruo
        self.efecto = efecto  
        self.incremento = incremento 
    def aplicar_a(self, monstruo:Monstruo):
        pass
        