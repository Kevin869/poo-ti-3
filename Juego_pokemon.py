import random
import time
import os
import json
from abc import ABC, abstractmethod

# ==============================
# CLASE MOVIMIENTO
# ==============================
class Movimiento:
    def __init__(self, nombre, poder, tipo):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo
    
    def atacar(self):
        efecto = random.choice(["normal", "doble", "pierde_turno", "sin_efecto"])
        return efecto

# ==============================
# CLASE POKEMON (PADRE)
# ==============================
class Pokemon(ABC):
    def __init__(self, nombre, tipo, ataque, defensa, hp, habilidad, movimientos, arte_ascii):
        self.nombre = nombre
        self.tipo = tipo
        self.ataque = ataque
        self.defensa = defensa
        self.hp_max = hp
        self.hp_actual = hp
        self.habilidad = habilidad
        self.movimientos = movimientos
        self.arte_ascii = arte_ascii
        self.nivel = 5
    
    def atacar(self, movimiento_idx, oponente):
        if movimiento_idx >= len(self.movimientos):
            return "Movimiento no válido"
        
        movimiento = self.movimientos[movimiento_idx]
        efecto = movimiento.atacar()
        
        # Calcular daño base
        daño_base = movimiento.poder * (self.ataque / 100)
        
        # Efectividad de tipo
        efectividad = self.calcular_efectividad(movimiento.tipo, oponente.tipo)
        
        # STAB (Same Type Attack Bonus)
        stab = 1.5 if movimiento.tipo == self.tipo else 1.0
        
        daño_final = daño_base * efectividad * stab
        
        # Aplicar defensa del oponente
        daño_final *= (100 / (100 + oponente.defensa))
        
        oponente.hp_actual -= max(1, int(daño_final))
        if oponente.hp_actual < 0:
            oponente.hp_actual = 0
        
        mensaje = f"{self.nombre} usa {movimiento.nombre}!"
        
        if efectividad > 1:
            mensaje += " ¡Es super efectivo!"
        elif efectividad < 1:
            mensaje += " No es muy efectivo..."
        
        if efecto == "doble":
            mensaje += " ¡Ataque doble!"
            oponente.hp_actual -= max(1, int(daño_final / 2))
        elif efecto == "pierde_turno":
            mensaje += " ¡El oponente pierde turno!"
            return mensaje, efecto
        elif efecto == "sin_efecto":
            mensaje += " Sin efecto..."
            oponente.hp_actual += daño_final  # Revierte el daño
        
        return mensaje, "normal"
    
    def calcular_efectividad(self, tipo_ataque, tipo_defensa):
        tabla_efectividad = {
            "fuego": {"planta": 2.0, "agua": 0.5, "fuego": 0.5, "normal": 1.0},
            "agua": {"fuego": 2.0, "planta": 0.5, "agua": 0.5, "normal": 1.0},
            "planta": {"agua": 2.0, "fuego": 0.5, "planta": 0.5, "normal": 1.0},
            "normal": {"fuego": 1.0, "agua": 1.0, "planta": 1.0, "normal": 1.0}
        }
        return tabla_efectividad.get(tipo_ataque, {}).get(tipo_defensa, 1.0)
    
    def esta_derrotado(self):
        return self.hp_actual <= 0
    
    def mostrar_estado(self):
        return f"""
{self.arte_ascii}
Nombre: {self.nombre}
Tipo: {self.tipo}
HP: {self.hp_actual}/{self.hp_max}
Ataque: {self.ataque}
Defensa: {self.defensa}
Habilidad: {self.habilidad}
Movimientos: {', '.join([m.nombre for m in self.movimientos])}
        """
    
    @abstractmethod
    def evolucionar(self):
        pass

# ==============================
# CLASES HIJAS DE POKEMON
# ==============================
class PyMon(Pokemon):  # Antes: Flameon
    def __init__(self):
        movimientos = [
            Movimiento("Llamarada", 80, "fuego"),
            Movimiento("Arañazo", 40, "normal"),
            Movimiento("Giro Fuego", 60, "fuego"),
            Movimiento("Descanso", 0, "normal")
        ]
        arte = """
  🔥
 /_/\\
/___\\
"""
        super().__init__("PyMon", "fuego", 65, 60, 70, "Mar Llamas", movimientos, arte)
    
    def evolucionar(self):
        return "¡PyMon evoluciona a PyGor!"

class JavaPup(Pokemon):  # Antes: Aquapup
    def __init__(self):
        movimientos = [
            Movimiento("Pistola Agua", 60, "agua"),
            Movimiento("Burbujas", 40, "agua"),
            Movimiento("Mordisco", 50, "normal"),
            Movimiento("Defensa Acuosa", 0, "agua")
        ]
        arte = """
  💧
 /_/\\
≈≈≈≈
"""
        super().__init__("JavaPup", "agua", 60, 70, 75, "Torrente", movimientos, arte)
    
    def evolucionar(self):
        return "¡JavaPup evoluciona a JavaLeon!"

class JSKitten(Pokemon):  # Antes: Leafkit
    def __init__(self):
        movimientos = [
            Movimiento("Hoja Afilada", 70, "planta"),
            Movimiento("Latigo Cepa", 50, "planta"),
            Movimiento("Síntesis", 0, "planta"),
            Movimiento("Planta Fuerte", 80, "planta")
        ]
        arte = """
  🌿
 /_/\\
/___\\
"""
        super().__init__("JSKitten", "planta", 62, 65, 72, "Clorofila", movimientos, arte)
    
    def evolucionar(self):
        return "¡JSKitten evoluciona a JSLeon!"

class CPlusMouse(Pokemon):  # Antes: Normouse
    def __init__(self):
        movimientos = [
            Movimiento("Hiperrayo", 90, "normal"),
            Movimiento("Ataque Rápido", 40, "normal"),
            Movimiento("Doble Ataque", 50, "normal"),
            Movimiento("Descanso", 0, "normal")
        ]
        arte = """
  🐭
 /_/\\
/___\\
"""
        super().__init__("CPlusMouse", "normal", 55, 55, 65, "Fuga", movimientos, arte)
    
    def evolucionar(self):
        return "¡CPlusMouse evoluciona a SuperMouse!"

class SwiftKit(Pokemon):  # Antes: Sparkit
    def __init__(self):
        movimientos = [
            Movimiento("Chispa", 65, "fuego"),
            Movimiento("Rayo", 70, "normal"),
            Movimiento("Velocidad", 0, "normal"),
            Movimiento("Sobrecarga", 85, "fuego")
        ]
        arte = """
  ⚡
 /_/\\
/___\\
"""
        super().__init__("SwiftKit", "fuego", 68, 58, 68, "Electricidad", movimientos, arte)
    
    def evolucionar(self):
        return "¡SwiftKit evoluciona a ThunderCat!"

class GoPup(Pokemon):  # Antes: Oceapup
    def __init__(self):
        movimientos = [
            Movimiento("Hidrochorro", 75, "agua"),
            Movimiento("Surf", 70, "agua"),
            Movimiento("Buceo", 60, "agua"),
            Movimiento("Ola", 50, "agua")
        ]
        arte = """
  🌊
 /_/\\
≈≈≈≈
"""
        super().__init__("GoPup", "agua", 63, 72, 78, "Nado Rápido", movimientos, arte)
    
    def evolucionar(self):
        return "¡GoPup evoluciona a GoLion!"

class RubyBaby(Pokemon):  # Antes: Bushbaby
    def __init__(self):
        movimientos = [
            Movimiento("Rayo Solar", 100, "planta"),
            Movimiento("Semilla", 40, "planta"),
            Movimiento("Drenadoras", 60, "planta"),
            Movimiento("Síntesis", 0, "planta")
        ]
        arte = """
  🌱
 /_/\\
/___\\
"""
        super().__init__("RubyBaby", "planta", 70, 60, 75, "Espesura", movimientos, arte)
    
    def evolucionar(self):
        return "¡RubyBaby evoluciona a RubyBear!"

class TypeBall(Pokemon):  # Antes: Fluffball
    def __init__(self):
        movimientos = [
            Movimiento("Golpe Cuerpo", 60, "normal"),
            Movimiento("Ataque Furioso", 80, "normal"),
            Movimiento("Defensa", 0, "normal"),
            Movimiento("Hiperrayo", 90, "normal")
        ]
        arte = """
  🐑
 /_/\\
/___\\
"""
        super().__init__("TypeBall", "normal", 58, 62, 80, "Armadura", movimientos, arte)
    
    def evolucionar(self):
        return "¡TypeBall evoluciona a TypeBeast!"

class RustRat(Pokemon):  # Antes: Emberat
    def __init__(self):
        movimientos = [
            Movimiento("Ascuas", 55, "fuego"),
            Movimiento("Fuego Fatuo", 70, "fuego"),
            Movimiento("Picotazo", 45, "normal"),
            Movimiento("Vuelo", 0, "normal")
        ]
        arte = """
  🔥
 /_/\\
/___\\
"""
        super().__init__("RustRat", "fuego", 67, 56, 65, "Llama", movimientos, arte)
    
    def evolucionar(self):
        return "¡RustRat evoluciona a RustOwl!"

class KotlinPup(Pokemon):  # Antes: Wavepup
    def __init__(self):
        movimientos = [
            Movimiento("Hidrobomba", 85, "agua"),
            Movimiento("Rayo Burbuja", 65, "agua"),
            Movimiento("Ataque Arena", 50, "normal"),
            Movimiento("Torbellino", 70, "agua")
        ]
        arte = """
  💦
 /_/\\
≈≈≈≈
"""
        super().__init__("KotlinPup", "agua", 65, 68, 74, "Cura Lluvia", movimientos, arte)
    
    def evolucionar(self):
        return "¡KotlinPup evoluciona a KotlinTide!"

# ==============================
# CLASE PARTIDA
# ==============================
class Partida:
    def __init__(self, nombre_jugador, pokemon_inicial):
        self.nombre_jugador = nombre_jugador
        self.equipo = [pokemon_inicial]
        self.pokemon_actual = 0
        self.historial_combates = []
        self.posicion = [5, 5]
        self.mapa = self.crear_mapa()
    
    def crear_mapa(self):
        mapa = [['.' for _ in range(11)] for _ in range(11)]
        # Colocar Pokémon salvajes en el mapa
        for i in range(3):
            x, y = random.randint(0, 10), random.randint(0, 10)
            if mapa[y][x] == '.':
                mapa[y][x] = random.choice(['🐱', '🐶', '🐭', '🐦'])
        return mapa
    
    def mostrar_mapa(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("╔═════════════════════════╗")
        for i, fila in enumerate(self.mapa):
            linea = " ".join(fila)
            if i == self.posicion[1]:
                linea = linea[:self.posicion[0]*2] + '😀' + linea[self.posicion[0]*2+1:]
            print(linea)
        print("╚═════════════════════════╝")
        print("│WASD-Movimiento │ M - Menu │ V-Volver │ H - Historial")
    
    def mover_jugador(self, direccion):
        x, y = self.posicion
        if direccion == 'w' and y > 0:
            y -= 1
        elif direccion == 's' and y < 10:
            y += 1
        elif direccion == 'a' and x > 0:
            x -= 1
        elif direccion == 'd' and x < 10:
            x += 1
        else:
            return False
        
        self.posicion = [x, y]
        
        # Verificar evento aleatorio (25% de probabilidad de combate)
        if self.mapa[y][x] != '.' and random.random() < 0.25:
            return "combate"
        
        return True

# ==============================
# CLASE JUEGO
# ==============================
class JuegoPokemon:
    def __init__(self):
        self.partida_actual = None
        self.pokemon_disponibles = {
            "1": PyMon(),
            "2": JavaPup(),
            "3": JSKitten()
        }
        self.pokemon_salvajes = [
            CPlusMouse(), SwiftKit(), GoPup(), RubyBaby(),
            TypeBall(), RustRat(), KotlinPup()
        ]
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausa(self, segundos=2):
        """Pausa mejorada con mensaje de progreso"""
        if segundos > 3:
            print(f"\nCargando... ({segundos} segundos)")
            for i in range(segundos):
                print("▓" * (i + 1), end="\r")
                time.sleep(1)
            print()
        else:
            time.sleep(segundos)
    
    def mostrar_mensaje_con_pausa(self, mensaje, segundos=2):
        """Muestra un mensaje y hace una pausa"""
        print(mensaje)
        self.pausa(segundos)
    
    def menu_principal(self):
        while True:
            self.limpiar_pantalla()
            print("🐱🐶 POKÉMON TERMINAL 🐱🐶")
            print("1. Crear Partida")
            print("2. Continuar Partida")
            print("3. Borrar Partida")
            print("4. Salir")
            
            opcion = input("\nSelecciona una opción: ")
            
            if opcion == "1":
                self.crear_partida()
            elif opcion == "2":
                self.continuar_partida()
            elif opcion == "3":
                self.borrar_partida()
            elif opcion == "4":
                print("¡Hasta pronto!")
                self.pausa(1)
                break
            else:
                self.mostrar_mensaje_con_pausa("Opción no válida", 1)
    
    def crear_partida(self):
        self.limpiar_pantalla()
        print("=== CREAR PARTIDA ===")
        nombre = input("Ingresa tu nombre: ")
        
        print("\nElige tu Pokémon inicial:")
        print("1. PyMon (Fuego) - Python")
        print("2. JavaPup (Agua) - Java")
        print("3. JSKitten (Planta) - JavaScript")
        
        while True:
            eleccion = input("\nSelecciona (1-3): ")
            if eleccion in self.pokemon_disponibles:
                pokemon_inicial = self.pokemon_disponibles[eleccion]
                self.partida_actual = Partida(nombre, pokemon_inicial)
                self.mostrar_mensaje_con_pausa(
                    f"¡Bienvenido {nombre}! Tu aventura con {pokemon_inicial.nombre} comienza ahora.", 
                    3
                )
                self.menu_exploracion()
                break
            else:
                self.mostrar_mensaje_con_pausa("Opción no válida", 1)
                self.limpiar_pantalla()
                print("=== CREAR PARTIDA ===")
                print(f"Jugador: {nombre}")
                print("\nElige tu Pokémon inicial:")
                print("1. PyMon (Fuego) - Python")
                print("2. JavaPup (Agua) - Java")
                print("3. JSKitten (Planta) - JavaScript")
    
    def continuar_partida(self):
        # Implementación básica - en una versión completa se cargaría desde archivo
        if self.partida_actual:
            self.mostrar_mensaje_con_pausa("Cargando partida existente...", 2)
            self.menu_exploracion()
        else:
            self.mostrar_mensaje_con_pausa("No hay partida guardada. Creando nueva partida...", 2)
            self.crear_partida()
    
    def borrar_partida(self):
        self.partida_actual = None
        self.mostrar_mensaje_con_pausa("Partida borrada exitosamente", 2)
    
    def menu_estados(self):
        self.limpiar_pantalla()
        print("=== ESTADO DEL EQUIPO ===")
        for i, pokemon in enumerate(self.partida_actual.equipo):
            print(f"\nPokémon {i+1}:")
            print(pokemon.mostrar_estado())
        
        input("\nPresiona Enter para continuar...")
    
    def menu_combate(self, pokemon_salvaje):
        self.limpiar_pantalla()
        print("¡COMBATE POKÉMON!")
        print(f"Te enfrentas a un {pokemon_salvaje.nombre} salvaje!")
        self.pausa(2)
        
        while True:
            pokemon_jugador = self.partida_actual.equipo[self.partida_actual.pokemon_actual]
            
            if pokemon_jugador.esta_derrotado():
                self.mostrar_mensaje_con_pausa(f"¡{pokemon_jugador.nombre} está debilitado!", 2)
                return "derrota"
            
            if pokemon_salvaje.esta_derrotado():
                self.mostrar_mensaje_con_pausa(f"¡{pokemon_salvaje.nombre} salvaje fue derrotado!", 3)
                self.partida_actual.historial_combates.append(f"Victoria vs {pokemon_salvaje.nombre}")
                return "victoria"
            
            print(f"\nTu Pokémon: {pokemon_jugador.nombre} - HP: {pokemon_jugador.hp_actual}/{pokemon_jugador.hp_max}")
            print(f"Oponente: {pokemon_salvaje.nombre} - HP: {pokemon_salvaje.hp_actual}/{pokemon_salvaje.hp_max}")
            
            print("\n1. Luchar")
            print("2. Estado")
            print("3. Huir")
            
            opcion = input("\nElige una opción: ")
            
            if opcion == "1":
                resultado = self.menu_movimientos(pokemon_jugador, pokemon_salvaje)
                if resultado == "huir":
                    return "huida"
                
                # Turno del oponente si no huyó
                if resultado != "huir" and not pokemon_salvaje.esta_derrotado():
                    self.mostrar_mensaje_con_pausa("\n¡Turno del oponente!", 2)
                    movimiento_oponente = random.randint(0, len(pokemon_salvaje.movimientos)-1)
                    mensaje, efecto = pokemon_salvaje.atacar(movimiento_oponente, pokemon_jugador)
                    print(mensaje)
                    self.pausa(3)  # Más tiempo para leer el ataque del oponente
                    
            elif opcion == "2":
                self.menu_estados()
                self.limpiar_pantalla()
                print("¡COMBATE POKÉMON!")
                print(f"Te enfrentas a un {pokemon_salvaje.nombre} salvaje!")
            elif opcion == "3":
                if random.random() < 0.7:  # 70% de probabilidad de huir
                    self.mostrar_mensaje_con_pausa("¡Logras huir del combate!", 2)
                    return "huida"
                else:
                    self.mostrar_mensaje_con_pausa("¡No puedes huir!", 2)
                    # Turno del oponente si no se pudo huir
                    self.mostrar_mensaje_con_pausa("\n¡Turno del oponente!", 2)
                    movimiento_oponente = random.randint(0, len(pokemon_salvaje.movimientos)-1)
                    mensaje, efecto = pokemon_salvaje.atacar(movimiento_oponente, pokemon_jugador)
                    print(mensaje)
                    self.pausa(3)
            else:
                self.mostrar_mensaje_con_pausa("Opción no válida", 1)
    
    def menu_movimientos(self, pokemon_jugador, pokemon_salvaje):
        self.limpiar_pantalla()
        print("Elige un movimiento:")
        for i, movimiento in enumerate(pokemon_jugador.movimientos):
            print(f"{i+1}. {movimiento.nombre} (Poder: {movimiento.poder}, Tipo: {movimiento.tipo})")
        print(f"{len(pokemon_jugador.movimientos)+1}. Volver")
        
        while True:
            try:
                opcion = int(input("\nSelecciona un movimiento: ")) - 1
                if opcion == len(pokemon_jugador.movimientos):
                    return "volver"
                elif 0 <= opcion < len(pokemon_jugador.movimientos):
                    mensaje, efecto = pokemon_jugador.atacar(opcion, pokemon_salvaje)
                    print(mensaje)
                    self.pausa(3)  # Más tiempo para leer el resultado del ataque
                    
                    # Mostrar estado actualizado después del ataque
                    print(f"\nHP de {pokemon_salvaje.nombre}: {pokemon_salvaje.hp_actual}/{pokemon_salvaje.hp_max}")
                    if pokemon_salvaje.esta_derrotado():
                        self.mostrar_mensaje_con_pausa(f"¡{pokemon_salvaje.nombre} está debilitado!", 2)
                    
                    self.pausa(2)  # Pausa adicional antes de continuar
                    return efecto
                else:
                    print("Opción no válida")
            except ValueError:
                print("Por favor ingresa un número")
    
    def menu_exploracion(self):
        while True:
            self.partida_actual.mostrar_mapa()
            accion = input("\n> ").lower()
            
            if accion in ['w', 'a', 's', 'd']:
                resultado = self.partida_actual.mover_jugador(accion)
                if resultado == "combate":
                    pokemon_salvaje = random.choice(self.pokemon_salvajes)
                    resultado_combate = self.menu_combate(pokemon_salvaje)
                    
                    if resultado_combate == "victoria":
                        self.mostrar_mensaje_con_pausa("¡Ganaste el combate!", 3)
                        # Restaurar HP después de victoria
                        for pokemon in self.partida_actual.equipo:
                            pokemon.hp_actual = pokemon.hp_max
                    elif resultado_combate == "derrota":
                        self.mostrar_mensaje_con_pausa("¡Perdiste el combate!", 3)
                        break
                    elif resultado_combate == "huida":
                        self.mostrar_mensaje_con_pausa("Regresas a la exploración...", 2)
            elif accion == 'm':
                self.menu_estados()
            elif accion == 'v':
                break
            elif accion == 'h':
                self.mostrar_historial()
            else:
                self.mostrar_mensaje_con_pausa("Comando no reconocido", 1)

    def mostrar_historial(self):
        self.limpiar_pantalla()
        print("=== HISTORIAL DE COMBATES ===")
        if self.partida_actual.historial_combates:
            for combate in self.partida_actual.historial_combates:
                print(f"- {combate}")
        else:
            print("Aún no hay combates en el historial")
        input("\nPresiona Enter para continuar...")

# ==============================
# EJECUCIÓN PRINCIPAL
# ==============================
if __name__ == "__main__":
    juego = JuegoPokemon()
    juego.menu_principal()