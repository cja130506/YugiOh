import random
from enum import Enum

class TipoMonstruo(Enum):
    Lanzador_conjuros = "L"
    Dragon = "D"
    Zombi = "Z"
    Guerrero = "G"
    Bestia = "B"
    Demonio = "D"

class Atributo(Enum):
    Oscuridad = "O"
    Luz = "L"
    Tierra = "T"
    Agua = "A"
    Fuego = "F"
    Viento = "V"

class Carta:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

class CartasMonstruo(Carta):
    def __init__(self, nombre, descripcion, ataque, defensa, tipo: TipoMonstruo, atributo: Atributo):
        super().__init__(nombre, descripcion)
        self.ataque = ataque
        self.defensa = defensa
        self.tipo = tipo
        self.atributo = atributo

class CartasMagicas(Carta):
    def __init__(self, nombre, descripcion, efecto):
        super().__init__(nombre, descripcion)
        self.efecto = efecto

class CartaTrampa(Carta):
    def __init__(self, nombre, descripcion, efecto, atributo_elegido: Atributo):
        super().__init__(nombre, descripcion)
        self.efecto = efecto
        self.atributo_elegido = atributo_elegido

    def activar(self, monstruo_atacante):
        if monstruo_atacante.atributo == self.atributo_elegido:
            return True
        else:
            return False

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntosDeVida = 4000
        self.mazo = []
        self.mano = []
        self.tablero = {"monstruos": [None] * 3, "magicas_trampa": [None] * 3}

    def robarCarta(self):
        if len(self.mazo) > 0:
            carta = self.mazo[0]
            del self.mazo[0]
            self.mano.append(carta)

    def jugarCarta(self, indice, posicion):
        if 0 <= indice < len(self.mano):
            carta = self.mano[indice]
            del self.mano[indice]
            if isinstance(carta, CartasMonstruo):
                if 0 <= posicion < len(self.tablero["monstruos"]) and self.tablero["monstruos"][posicion] is None:
                    self.tablero["monstruos"][posicion] = carta
            elif isinstance(carta, (CartasMagicas, CartaTrampa)):
                if 0 <= posicion < len(self.tablero["magicas_trampa"]) and self.tablero["magicas_trampa"][posicion] is None:
                    self.tablero["magicas_trampa"][posicion] = carta

    def mostrarEstado(self):
        print(f"{self.nombre}: {self.puntosDeVida} Puntos de Vida")
        print("Mano:")
        for i in range(len(self.mano)):
            carta = self.mano[i]
            print(f"{i}: {carta.nombre} - {carta.descripcion}")
        print("Tablero (Monstruos):")
        for i in range(len(self.tablero["monstruos"])):
            carta = self.tablero["monstruos"][i]
            if carta is not None:
                print(carta.nombre)
            else:
                print("Vacío")
        print("Tablero (Mágicas/Trampas):")
        for i in range(len(self.tablero["magicas_trampa"])):
            carta = self.tablero["magicas_trampa"][i]
            if carta is not None:
                print(carta.nombre)
            else:
                print("Vacío")

class Juego:
    def __init__(self, jugador1, jugador2):
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.turnoJugador = random.choice([True, False])

    def faseRobo(self):
        if self.turnoJugador:
            jugador = self.jugador1
        else:
            jugador = self.jugador2
        jugador.robarCarta()

    def fasePrincipal(self):
        if self.turnoJugador:
            jugador = self.jugador1
            jugador.mostrarEstado()
            print("\nElige una carta para jugar (índice de la mano) o -1 para pasar:")
            opcion = input()
            if opcion.isdigit():
                indice = int(opcion)
                if indice == -1:
                    print("Has decidido no jugar ninguna carta.")
                elif 0 <= indice < len(jugador.mano):
                    print("Elige una posición en el tablero:")
                    posicion = input()
                    if posicion.isdigit():
                        posicion = int(posicion)
                        if 0 <= posicion < len(jugador.tablero["monstruos"]):
                            jugador.jugarCarta(indice, posicion)
                        else:
                            print("Posición no válida.")
                    else:
                        print("Entrada no válida.")
                else:
                    print("Índice no válido.")
            else:
                print("Entrada no válida.")
        else:
            jugador = self.jugador2
            i = 0
            while i < len(jugador.mano):
                carta = jugador.mano[i]
                if isinstance(carta, CartasMonstruo):
                    jugador.jugarCarta(i, 0)
                    i = len(jugador.mano)  # Finalizar ciclo
                i += 1

    def faseBatalla(self):
        if self.turnoJugador:
            atacante = self.jugador1
            defensor = self.jugador2
        else:
            atacante = self.jugador2
            defensor = self.jugador1

        i = 0
        while i < len(atacante.tablero["monstruos"]):
            carta = atacante.tablero["monstruos"][i]
            if carta is not None:
                monstruos_defensor = False
                j = 0
                while j < len(defensor.tablero["monstruos"]):
                    if defensor.tablero["monstruos"][j] is not None:
                        monstruos_defensor = True
                    j += 1
                if monstruos_defensor:
                    defensor.puntosDeVida -= carta.ataque // 2
                else:
                    defensor.puntosDeVida -= carta.ataque
            i += 1

    def cambiarTurno(self):
        if self.turnoJugador:
            self.turnoJugador = False
        else:
            self.turnoJugador = True

    def jugar(self):
        while self.jugador1.puntosDeVida > 0 and self.jugador2.puntosDeVida > 0:
            if self.turnoJugador:
                print("\nTurno de Jugador 1")
            else:
                print("\nTurno de Jugador 2")
            self.faseRobo()
            self.fasePrincipal()
            if not self.turnoJugador:
                self.faseBatalla()
            self.cambiarTurno()
        if self.jugador1.puntosDeVida > 0:
            print("\n¡Jugador 1 ha ganado!")
        else:
            print("\n¡Jugador 2 ha ganado!")

if __name__ == "__main__":
    jugador1 = Jugador("Jugador 1")
    jugador2 = Jugador("Jugador 2")

    carta_monstruo_1 = CartasMonstruo("Dragón Blanco de Ojos Azules", "Un dragón legendario.", 3000, 2500, TipoMonstruo.Dragon, Atributo.Luz)
    carta_monstruo_2 = CartasMonstruo("Mago Oscuro", "Un mago oscuro poderoso.", 2500, 2100, TipoMonstruo.Lanzador_conjuros, Atributo.Oscuridad)
    carta_magica = CartasMagicas("Espadas de Luz Reveladora", "Evita ataques por 3 turnos.", "Evita ataques")
    carta_trampa = CartaTrampa("Cilindro Mágico", "Refleja daño.", "Refleja daño", Atributo.Luz)

    jugador1.mazo = [carta_monstruo_1, carta_magica, carta_trampa] * 5
    jugador2.mazo = [carta_monstruo_2, carta_magica] * 5

    juego = Juego(jugador1, jugador2)
    juego.jugar()