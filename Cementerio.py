from enum import Enum
class TipoMonstruo(Enum):
    LANZADOR_DE_CONJUROS = "L"
    DRAGON = "D"
    ZOMBI = "Z"
    GUERRERO = "G"
    BESTIA = "B"
    DEMONIO = "D"

class Atributo(Enum):
    OSCURIDAD = "OSCURIDAD"
    LUZ = "LUZ"
    TIERRA = "TIERRA"
    AGUA = "AGUA"
    FUEGO = "FUEGO"
    VIENTO = "VIENTO"

class Cementerio:
    def __init__(self):
        self.jugador_cementerio = []  # Cartas del jugador
        self.maquina_cementerio = []  # Cartas de la máquina

    def agregar_carta(self, carta, jugador=True):
        if jugador:
            self.jugador_cementerio.append(carta)
        else:
            self.maquina_cementerio.append(carta)

    def mostrar_cementerio(self):
        print("\nTablero-Monstruo del jugador:")
        for carta in self.jugador_cementerio:
          if carta.tipo == "Monstruo":
            print(f"[{carta.nombre} ({carta.tipo}) | ATK: {carta.ataque} | DEF: {carta.defensa}]")
          else:
            print(f"[{carta.nombre} ({carta.tipo})]")

        print("\nTablero-Monstruo de la máquina:")
        for carta in self.maquina_cementerio:
          if carta.tipo == "Monstruo":
            print(f"[{carta.nombre} ({carta.tipo}) | ATK: {carta.ataque} | DEF: {carta.defensa}]")
          else:
              print(f"[{carta.nombre} ({carta.tipo})]")