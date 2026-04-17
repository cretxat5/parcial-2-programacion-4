#1. Sistema de gestión de vehículos para una empresa de alquiler
import json
import os
from typing import Dict

# -------------------------
# utils.py (normalización)
# -------------------------
def normalize_placa(placa: str):
    if placa is None:
        return ""
    return placa.strip().replace(" ", "").lower()

# -------------------------
# models.py
# -------------------------
class Vehiculo:
    def __init__(self, placa, marca, modelo, precio_dia, disponible=True):
        self._placa = normalize_placa(placa)
        self._marca = marca
        self._modelo = modelo
        self._precio_dia = float(precio_dia)
        self._disponible = bool(disponible)

    # Propiedades (encapsulamiento)
    @property
    def placa(self):
        return self._placa

    @property
    def marca(self):
        return self._marca

    @property
    def modelo(self):
        return self._modelo

    @property
    def precio_dia(self):
        return self._precio_dia

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    def to_dict(self) -> dict:
        return {
            "tipo": "Vehiculo",
            "placa": self._placa,
            "marca": self._marca,
            "modelo": self._modelo,
            "precio_dia": self._precio_dia,
            "disponible": self._disponible
        }

    def descripcion(self):
        # Método polimórfico base
        return f"[{self._placa}] {self._marca} {self._modelo} - ${self._precio_dia:.2f}/día | {'Disponible' if self._disponible else 'Alquilado'}"

    def __str__(self):
        return self.descripcion()


class Automovil(Vehiculo):
    def __init__(self, placa, marca, modelo, precio_dia, num_puertas, disponible=True):
        super().__init__(placa, marca, modelo, precio_dia, disponible)
        self._num_puertas = int(num_puertas)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["tipo"] = "Automovil"
        d["num_puertas"] = self._num_puertas
        return d

    def descripcion(self):
        return f"{super().descripcion()} (Automóvil | Puertas: {self._num_puertas})"


class Motocicleta(Vehiculo):
    def __init__(self, placa, marca, modelo, precio_dia, cilindraje, disponible=True):
        super().__init__(placa, marca, modelo, precio_dia, disponible)
        self._cilindraje = int(cilindraje)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["tipo"] = "Motocicleta"
        d["cilindraje"] = self._cilindraje
        return d

    def descripcion(self):
        return f"{super().descripcion()} (Moto | Cilindraje: {self._cilindraje}cc)"


class Camion(Vehiculo):
    def __init__(self, placa, marca, modelo, precio_dia, capacidad_carga, disponible=True):
        super().__init__(placa, marca, modelo, precio_dia, disponible)
        self._capacidad_carga = float(capacidad_carga)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["tipo"] = "Camion"
        d["capacidad_carga"] = self._capacidad_carga
        return d

    def descripcion(self):
        return f"{super().descripcion()} (Camión | Carga: {self._capacidad_carga}t)"

# -------------------------
# (GestorVehiculos)
# -------------------------
class GestorVehiculos:
    def __init__(self, archivo="vehiculos.json"):
        self.archivo = archivo
        self.vehiculos: Dict[str, Vehiculo] = {}
        self.cargar()

    def cargar(self):
        """Carga vehículos desde JSON. Maneja archivo inexistente o corrupto."""
        if not os.path.exists(self.archivo):
            # archivo no existe: inicia vacío
            self.vehiculos = {}
            return
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except (json.JSONDecodeError, IOError):
            print(" Error leyendo archivo JSON. Se iniciará con inventario vacío.")
            self.vehiculos = {}
            return

        self.vehiculos = {}
        for d in datos:
            tipo = d.get("tipo", "Vehiculo")
            # Aseguramos que los parámetros coincidan con los constructores
            try:
                if tipo == "Automovil":
                    v = Automovil(d.get("placa"), d.get("marca"), d.get("modelo"), d.get("precio_dia"), d.get("num_puertas"), d.get("disponible", True))
                elif tipo == "Motocicleta":
                    v = Motocicleta(d.get("placa"), d.get("marca"), d.get("modelo"), d.get("precio_dia"), d.get("cilindraje"), d.get("disponible", True))
                elif tipo == "Camion":
                    v = Camion(d.get("placa"), d.get("marca"), d.get("modelo"), d.get("precio_dia"), d.get("capacidad_carga"), d.get("disponible", True))
                else:
                    v = Vehiculo(d.get("placa"), d.get("marca"), d.get("modelo"), d.get("precio_dia"), d.get("disponible", True))
            except Exception:
                # Si hay un error creando la instancia se salta
                continue
            self.vehiculos[v.placa] = v

    def guardar(self):
        """Guarda el inventario actual en JSON."""
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([v.to_dict() for v in self.vehiculos.values()], f, indent=4, ensure_ascii=False)
        except IOError:
            print(" Error al guardar el archivo JSON.")

    def registrar(self, tipo, placa, marca, modelo, precio, disp=True, **kwargs):
        placa_norm = normalize_placa(placa)
        if not placa_norm:
            print(" Error: Placa inválida.")
            return
        if placa_norm in self.vehiculos:
            print(" Error: Placa ya registrada.")
            return
        try:
            precio = float(precio)
            if precio <= 0:
                print(" Error: Precio inválido.")
                return
        except (ValueError, TypeError):
            print(" Error: Precio inválido.")
            return

        # Crear según tipo
        if tipo == "1":
            try:
                puertas = int(kwargs.get("puertas"))
            except (TypeError, ValueError):
                print(" Error: Número de puertas inválido.")
                return
            v = Automovil(placa, marca, modelo, precio, puertas, disp)
        elif tipo == "2":
            try:
                cilindraje = int(kwargs.get("cilindraje"))
            except (TypeError, ValueError):
                print(" Error: Cilindraje inválido.")
                return
            v = Motocicleta(placa, marca, modelo, precio, cilindraje, disp)
        elif tipo == "3":
            try:
                carga = float(kwargs.get("carga"))
            except (TypeError, ValueError):
                print(" Error: Capacidad de carga inválida.")
                return
            v = Camion(placa, marca, modelo, precio, carga, disp)
        else:
            print(" Error: Tipo de vehículo inválido.")
            return

        self.vehiculos[v.placa] = v
        self.guardar()
        print(" Vehículo registrado correctamente.")

    def mostrar_disponibles(self):
        if not self.vehiculos:
            print(" No hay vehículos registrados.")
            return
        disponibles = [v for v in self.vehiculos.values() if v.disponible]
        if not disponibles:
            print(" No hay vehículos disponibles.")
            return
        print("\n VEHÍCULOS DISPONIBLES:")
        for v in disponibles:
            print(v)

    def listar_todos(self):
        if not self.vehiculos:
            print(" No hay vehículos registrados.")
            return
        print("\n📋 TODOS LOS VEHÍCULOS:")
        for v in self.vehiculos.values():
            print(v)

    def alquilar(self, placa, dias):
        if not self.vehiculos:
            print(" No hay vehículos registrados.")
            return
        try:
            dias = int(dias)
            if dias <= 0:
                print(" Error: La cantidad de días debe ser mayor que 0.")
                return
        except (ValueError, TypeError):
            print(" Error: Días inválidos.")
            return

        # Si no hay disponibles, evitamos búsqueda por placa
        if not any(v.disponible for v in self.vehiculos.values()):
            print(" No hay vehículos disponibles.")
            return

        placa_norm = normalize_placa(placa)
        v = self.vehiculos.get(placa_norm)
        if not v:
            print("Vehículo no encontrado.")
            return
        if not v.disponible:
            print(" Vehículo ya está alquilado.")
            return

        v.disponible = False
        costo = v.precio_dia * dias
        self.guardar()
        print(f" Vehículo {placa_norm} alquilado por {dias} días. Costo total: ${costo:.2f}")

    def devolver(self, placa):
        if not self.vehiculos:
            print("📭 No hay vehículos registrados.")
            return
        placa_norm = normalize_placa(placa)
        v = self.vehiculos.get(placa_norm)
        if not v:
            print(" Vehículo no encontrado.")
            return
        if v.disponible:
            print(" Este vehículo ya está disponible.")
            return
        v.disponible = True
        self.guardar()
        print(f" Vehículo {placa_norm} devuelto correctamente.")


def menu_vehiculos():
    gestor = GestorVehiculos()
    while True:
        print("\n=== SISTEMA DE ALQUILER DE VEHÍCULOS ===")
        print("1. Registrar vehículo")
        print("2. Mostrar disponibles")
        print("3. Listar todos")
        print("4. Alquilar")
        print("5. Devolver")
        print("6. Salir")
        op = input("Opción: ").strip()

        if op == "1":
            tipo = input("Tipo (1:Auto 2:Moto 3:Camión): ").strip()
            # Validación inmediata del tipo
            if tipo not in ("1", "2", "3"):
                print(" Tipo inválido. Debes ingresar 1, 2 o 3.")
                continue

            placa = input("Placa: ").strip()
            marca = input("Marca: ").strip()
            modelo = input("Modelo: ").strip()

            # Validar precio antes de seguir
            try:
                precio = float(input("Precio/día: ").strip())
                if precio <= 0:
                    print(" Precio inválido. Debe ser mayor que 0.")
                    continue
            except ValueError:
                print(" Precio inválido.")
                continue

            disp = input("¿Disponible? (s/n): ").strip().lower() == "s"

            # Pedir y validar solo el dato específico del tipo
            kwargs = {}
            if tipo == "1":
                try:
                    puertas = int(input("Puertas: ").strip())
                    if puertas <= 0:
                        print(" Número de puertas inválido.")
                        continue
                    kwargs["puertas"] = puertas
                except ValueError:
                    print(" Número de puertas inválido.")
                    continue

            elif tipo == "2":
                try:
                    cilindraje = int(input("Cilindraje: ").strip())
                    if cilindraje <= 0:
                        print(" Cilindraje inválido.")
                        continue
                    kwargs["cilindraje"] = cilindraje
                except ValueError:
                    print(" Cilindraje inválido.")
                    continue

            elif tipo == "3":
                try:
                    carga = float(input("Cap. Carga (t): ").strip())
                    if carga <= 0:
                        print(" Capacidad de carga inválida.")
                        continue
                    kwargs["carga"] = carga
                except ValueError:
                    print(" Capacidad de carga inválida.")
                    continue

            gestor.registrar(tipo, placa, marca, modelo, precio, disp, **kwargs)

        elif op == "2":
            gestor.mostrar_disponibles()

        elif op == "3":
            gestor.listar_todos()

        elif op == "4":
            # Verificamos inventario antes de pedir datos al usuario
            if not gestor.vehiculos:
                print("📭 No hay vehículos registrados. Primero registra vehículos.")
                continue

            if not any(v.disponible for v in gestor.vehiculos.values()):
                print("📭 No hay vehículos disponibles para alquilar en este momento.")
                continue

            # Si llegamos aquí, sí hay al menos un vehículo disponible: pedimos placa y días
            placa = input("Placa a alquilar: ").strip()
            try:
                dias = int(input("Días: ").strip())
            except ValueError:
                print(" Días inválidos.")
                continue

            gestor.alquilar(placa, dias)

        elif op == "5":
            # Verificamos inventario antes de pedir placa para devolución
            if not gestor.vehiculos:
                print("📭 No hay vehículos registrados.")
                continue

            if not any(not v.disponible for v in gestor.vehiculos.values()):
                print("📭 No hay vehículos alquilados para devolver.")
                continue

            placa = input("Placa a devolver: ").strip()
            gestor.devolver(placa)

        elif op == "6":
            print("Saliendo...")
            break
        else:
            print(" Opción inválida.")

# -------------------------
# Ejecutable
# -------------------------
if __name__ == "__main__":
    menu_vehiculos()