
from ProyectoYugioh import Cementerio, procesar_cartas
import random

class Juego:
    def __init__(self):
        self.jugador_puntos = 4000
        self.maquina_puntos = 4000
        self.jugador_tablero = {"monstruos": [], "magicas_trampas": []}
        self.maquina_tablero = {"monstruos": [], "magicas_trampas": []}
        self.jugador_mano = []
        self.maquina_mano = []
        self.cartas = []
        self.turno_contador = 0
        self.cementerio = Cementerio() 

    def mostrar_puntajes(self):
        print("\nPuntajes actuales:")
        print(f"Jugador: {self.jugador_puntos} puntos")
        print(f"Máquina: {self.maquina_puntos} puntos")

    def cargar_cartas(self, archivo):
        with open(archivo, "r") as file:
            contenido = file.readlines()
        self.cartas = procesar_cartas(contenido)

    def construir_mazo(self):
        mazo = random.sample(self.cartas, 30)  
        return mazo

    def iniciar_juego(self):
        print("Iniciando juego..")
        mazo_jugador = self.construir_mazo()
        mazo_maquina = self.construir_mazo()
        self.jugador_mano = mazo_jugador[:4]
        self.maquina_mano = mazo_maquina[:4]
        self.jugador_mazo = mazo_jugador[4:]
        self.maquina_mazo = mazo_maquina[4:]
        turno = random.choice(["Jugador", "Máquina"])
        print(f"El {turno} empieza jugando.")
        return turno

    def tomar_carta(self, turno):
        if turno == "Jugador" and self.jugador_mazo:
            carta = self.jugador_mazo.pop(0)
            self.jugador_mano.append(carta)
            print(f"El jugador robó: {carta.nombre}")
        elif turno == "Máquina" and self.maquina_mazo:
            carta = self.maquina_mazo.pop(0)
            self.maquina_mano.append(carta)
            print("La máquina robó una carta.")

    def realizar_ataque(self):
                if not self.jugador_tablero["monstruos"]:
                    print("No tienes monstruos en el tablero para atacar.")
                    return
                if not self.maquina_tablero["monstruos"]:
                    print("La máquina no tiene monstruos en el tablero. Puedes atacar directamente sus puntos de vida.")
                    atacante = self.jugador_tablero["monstruos"][0]  # Elige el primer monstruo del jugador por simplicidad
                    print(f"\nAtacas directamente con {atacante.nombre} ({atacante.ataque} ATK).")
                    self.maquina_puntos -= atacante.ataque
                    print(f"La máquina pierde {atacante.ataque} puntos.")
                    return

                print("\nElige el monstruo de la máquina al que quieres atacar:")
                for i, monstruo in enumerate(self.maquina_tablero["monstruos"]):
                    print(f"{i + 1}. {monstruo.nombre} | ATK: {monstruo.ataque}, DEF: {monstruo.defensa}")
                intentos = 3
                while intentos>0:
                    try:
                        eleccion = int(input("Selecciona el número del monstruo para atacar: ")) - 1
                        if 0 <= eleccion < len(self.maquina_tablero["monstruos"]):
                            defensor = self.maquina_tablero["monstruos"][eleccion]
                            break
                        else:
                            intentos-=1
                            print(f"Número inválido. Te quedan {intentos} intentos.")
                            if intentos == 0:
                                print("Se acabaron los intentos. El turno termina.")
                                return
                    except ValueError:
                        intentos-=1
                        print(f"Entrada inválida. Te quedan {intentos} intentos.")
                        if intentos == 0:
                            print("Se acabaron los intentos. El turno termina.")
                            return

                atacante = self.jugador_tablero["monstruos"][0]  # Por simplicidad, el primer monstruo

                print(f"\nEl jugador ataca con {atacante.nombre} ({atacante.ataque} ATK).")
                print(f"La máquina defiende con {defensor.nombre} ({defensor.defensa} DEF).")

                if atacante.ataque > defensor.defensa:
                    puntos_perdidos = atacante.ataque - defensor.defensa
                    self.maquina_puntos = max(0, self.maquina_puntos - puntos_perdidos)
                    print(f"La máquina pierde {puntos_perdidos} puntos.")
                    self.cementerio.agregar_carta(defensor, jugador=False)  # Carta al cementerio
                    self.maquina_tablero["monstruos"].remove(defensor)
                elif atacante.ataque < defensor.defensa:
                    puntos_perdidos = defensor.defensa - atacante.ataque
                    self.jugador_puntos = max(0, self.jugador_puntos - puntos_perdidos)
                    print(f"El jugador pierde {puntos_perdidos} puntos.")
                    self.cementerio.agregar_carta(atacante, jugador=True)  # Carta al cementerio
                    self.jugador_tablero["monstruos"].remove(atacante)
                else:
                    print("Ambos monstruos son destruidos.")
                    self.cementerio.agregar_carta(atacante, jugador=True)
                    self.cementerio.agregar_carta(defensor, jugador=False)
                    self.jugador_tablero["monstruos"].remove(atacante)
                    self.maquina_tablero["monstruos"].remove(defensor)



    def mostrar_cementerio(self):
        self.cementerio.mostrar_cementerio()

    def verificar_ganador(self):
        if self.jugador_puntos <= 0:
            print("\nTerminó el juego. La máquina gana con 0 puntos de vida restantes del jugador.")
            return True
        elif self.maquina_puntos <= 0:
            print("\nTerminó el juego. El jugador gana con 0 puntos de vida restantes de la máquina.")
            return True
        return False

    def jugar(self):
        turno = self.iniciar_juego()
        while not(self.verificar_ganador()):
            self.jugar_turno(turno)
            if self.verificar_ganador():
              break
            self.realizar_ataque()  
            if self.verificar_ganador():
              break
            self.mostrar_puntajes() 
            self.mostrar_cementerio()
            turno = "Jugador" if turno == "Máquina" else "Máquina"

    def jugar_turno(self, turno):
        print(f"\nTurno de {turno}")
        self.tomar_carta(turno)
        if self.turno_contador>2:
            if turno =="Jugador":
                self.realizar_ataque()
                self.mostrar_puntajes()
        else:
            print("No se puede atacar en la primera batalla. ")

        if turno == "Jugador":
            print("Tu mano:")
            for i, carta in enumerate(self.jugador_mano):
                if carta.tipo == "Monstruo":
                    print(f"{i + 1}. {carta.nombre} ({carta.tipo}) - {carta.descripcion} | ATK: {carta.ataque}, DEF: {carta.defensa}")
                else:
                    print(f"{i + 1}. {carta.nombre} ({carta.tipo}) - {carta.descripcion}")
            eleccion = int(input("Selecciona una carta para jugar (1-5): ")) - 1
            carta_jugada = self.jugador_mano.pop(eleccion)

            if carta_jugada.tipo == "Monstruo":
                posicion = input("¿Quieres jugar esta carta en ataque (boca arriba) o defensa (boca abajo)? (ataque/defensa): ").lower()
                carta_jugada.posicion = "ataque" if posicion == "ataque" else "defensa"
                self.jugador_tablero["monstruos"].append(carta_jugada)
                estado = "boca arriba" if carta_jugada.posicion == "ataque" else "boca abajo"
                print(f"Has jugado el monstruo {carta_jugada.nombre} en {estado}.")
                cambiar_posicion = input("¿Quieres cambiar la posición de algún monstruo en el tablero? (s/n): ").lower()
                if cambiar_posicion == "s":
                  self.cambiar_posicion()
            elif carta_jugada.tipo == "Magica":
                self.jugador_tablero["magicas_trampas"].append(carta_jugada)
                print(f"Has jugado la carta mágica: {carta_jugada.nombre}")
                self.activar_efecto_magico(carta_jugada)
            elif carta_jugada.tipo == "Trampa":
                self.jugador_tablero["magicas_trampas"].append(carta_jugada)
                print(f"Has jugado la carta trampa: {carta_jugada.nombre}")
                self.activar_efecto_trampa(carta_jugada)

        else:
            if self.maquina_mano:
                carta_jugada = self.maquina_mano.pop(0)
                if carta_jugada.tipo == "Monstruo":
                    carta_jugada.posicion = "ataque"  
                    self.maquina_tablero["monstruos"].append(carta_jugada)
                    print(f"La máquina jugó el monstruo {carta_jugada.nombre} en ataque.")
                elif carta_jugada.tipo in ["Magica", "Trampa"]:
                    self.maquina_tablero["magicas_trampas"].append(carta_jugada)
                    print(f"La máquina jugó una carta {carta_jugada.tipo.lower()}: {carta_jugada.nombre}.")
        self.turno_contador+=1

    def activar_efecto_magico(self, carta):
      print(f"Activando el efecto de la carta mágica: {carta.nombre}")
      if carta.incremento and carta.afectado:
          print(f"Aplicando un incremento de {carta.incremento} a monstruos del tipo {carta.afectado}.")
          for monstruo in self.jugador_tablero["monstruos"]:
              if monstruo.tipo_monstruo == carta.afectado:
                  monstruo.ataque += carta.incremento
                  print(f"{monstruo.nombre} ahora tiene {monstruo.ataque} ATK.")
      elif carta.incremento and not carta.afectado:
          print("La carta mágica no tiene un tipo afectado válido.")

    def activar_efecto_trampa(self, carta):
      print(f"Activando el efecto de la carta trampa: {carta.nombre}")
      if carta.atributo:
          print(f"Bloqueando ataques de monstruos con el atributo {carta.atributo}.")
          monstruos_bloqueados = [
              monstruo for monstruo in self.maquina_tablero["monstruos"]
              if monstruo.atributo == carta.atributo
          ]
          if monstruos_bloqueados:
              print("Los siguientes monstruos de la máquina no pueden atacar:")
              for monstruo in monstruos_bloqueados:
                  print(f"{monstruo.nombre}")
          else:
              print("No hay monstruos en el tablero de la máquina con ese atributo.")