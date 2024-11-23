from Cartas import Carta

class Monstruo(Carta):
    def __ini__ (self, nombre, descripcion, ataque, defensa, tipo_monstruo, atributo, posicion):
        super().__init__(nombre, descripcion)
        self.ataque = ataque
        self.defensa = defensa
        self.tipo_monstruo = tipo_monstruo
        self.atributo = atributo
        self.posicion = posicion
    def cambiar_posicion(self):
        pass
    def recibir_ataque(self,ataque_oponente: int):
        pass
