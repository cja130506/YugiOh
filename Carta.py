class Carta:
    def __init__(self, tipo, nombre, descripcion, ataque=None, defensa=None, tipo_monstruo=None, atributo=None, incremento=None, afectado=None):
        self.tipo = tipo
        self.nombre = nombre
        self.descripcion = descripcion
        self.ataque = ataque
        self.defensa = defensa
        self.tipo_monstruo = tipo_monstruo
        self.atributo = atributo
        self.incremento = incremento
        self.afectado = afectado
        self.posicion = None

def procesar_cartas(contenido):
    cartas = []
    for linea in contenido:
        if linea.startswith("#") or not linea.strip():
            continue  

        partes = linea.strip().split("|")
        if partes[0] == "Monstruo":
            cartas.append(Carta(
                tipo="Monstruo",
                nombre=partes[1],
                descripcion=partes[2],
                ataque=int(partes[3]),
                defensa=int(partes[4]),
                tipo_monstruo=partes[5],
                atributo=partes[6]
            ))
        elif partes[0] == "Magica":
            cartas.append(Carta(
                tipo="Magica",
                nombre=partes[1],
                descripcion=partes[2],
                incremento=int(partes[3]),
                afectado=partes[4]
            ))
        elif partes[0] == "Trampa":
            cartas.append(Carta(
                tipo="Trampa",
                nombre=partes[1],
                descripcion=partes[2],
                atributo=partes[3]
            ))
    return cartas