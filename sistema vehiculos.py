import json
import os

class Vehiculo:
    def __init__(self, placa, marca, modelo, precio_dia, disponible=True):
        self._placa = placa.upper()
        self._marca = marca
        self._modelo = modelo
        self._precio_dia = precio_dia
        self._disponible = disponible

    @property
    def placa(self): return self._placa
    @property
    def marca(self): return self._marca
    @property
    def modelo(self): return self._modelo
    @property
    def precio_dia(self): return self._precio_dia
    @property
    def disponible(self): return self._disponible

    @disponible.setter
    def disponible(self, valor): self._disponible = valor

    def to_dict(self):
        return {
            "tipo": "Vehiculo", "placa": self._placa, "marca": self._marca,
            "modelo": self._modelo, "precio_dia": self._precio_dia, "disponible": self._disponible
        }

    def __str__(self):
        return f"[{self._placa}] {self._marca} {self._modelo} - ${self._precio_dia}/día | {'✅ Disponible' if self._disponible else '❌ Alquilado'}"


class Automovil(Vehiculo):
    def __init__(self, placa, marca, modelo, precio_dia, num_puertas, disponible=True):
        super().__init__(placa, marca, modelo, precio_dia, disponible)
        self._num_puertas = num_puertas
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "Automovil"; d["num_puertas"] = self._num_puertas; return d
    def __str__(self): return f"{super().__str__()} (Automóvil | Puertas: {self._num_puertas})"

class Motocicleta(Vehiculo):
    def __init__(self, placa, marca, modelo, precio_dia, cilindraje, disponible=True):
        super().__init__(placa, marca, modelo, precio_dia, disponible)
        self._cilindraje = cilindraje
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "Motocicleta"; d["cilindraje"] = self._cilindraje; return d
    def __str__(self): return f"{super().__str__()} (Moto | Cilindraje: {self._cilindraje}cc)"

class Camion(Vehiculo):
    def __init__(self, placa, marca, modelo, precio_dia, capacidad_carga, disponible=True):
        super().__init__(placa, marca, modelo, precio_dia, disponible)
        self._capacidad_carga = capacidad_carga
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "Camion"; d["capacidad_carga"] = self._capacidad_carga; return d
    def __str__(self): return f"{super().__str__()} (Camión | Carga: {self._capacidad_carga}t)"

class GestorVehiculos:
    def __init__(self, archivo="vehiculos.json"):
        self.archivo = archivo
        self.vehiculos = {}
        self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                datos = json.load(f)
            for d in datos:
                t = d.pop("tipo")
                cls = {"Automovil": Automovil, "Motocicleta": Motocicleta, "Camion": Camion, "Vehiculo": Vehiculo}.get(t, Vehiculo)
                v = cls(**d)
                self.vehiculos[v.placa] = v

    def guardar(self):
        with open(self.archivo, "w") as f:
            json.dump([v.to_dict() for v in self.vehiculos.values()], f, indent=4)

    def registrar(self, tipo, placa, marca, modelo, precio, disp, **kwargs):
        if placa.upper() in self.vehiculos:
            print("❌ Error: Placa ya registrada.")
            return
        if tipo == "1": self.vehiculos[placa.upper()] = Automovil(placa, marca, modelo, precio, kwargs["puertas"], disp)
        elif tipo == "2": self.vehiculos[placa.upper()] = Motocicleta(placa, marca, modelo, precio, kwargs["cilindraje"], disp)
        elif tipo == "3": self.vehiculos[placa.upper()] = Camion(placa, marca, modelo, precio, kwargs["carga"], disp)
        self.guardar()
        print("✅ Vehículo registrado correctamente.")

    def mostrar_disponibles(self):
        disponibles = [v for v in self.vehiculos.values() if v.disponible]
        if not disponibles: print("📭 No hay vehículos disponibles.")
        else:
            print("\n🚗 VEHÍCULOS DISPONIBLES:")
            for v in disponibles: print(v)

    def alquilar(self, placa, dias):
        v = self.vehiculos.get(placa.upper())
        if not v: print("❌ Vehículo no encontrado.")
        elif not v.disponible: print("❌ Vehículo ya está alquilado.")
        else:
            v.disponible = False
            costo = v.precio_dia * dias
            self.guardar()
            print(f"✅ Vehículo {placa.upper()} alquilado por {dias} días. Costo total: ${costo:.2f}")

    def devolver(self, placa):
        v = self.vehiculos.get(placa.upper())
        if not v: print("❌ Vehículo no encontrado.")
        elif v.disponible: print("⚠️ Este vehículo ya está disponible.")
        else:
            v.disponible = True
            self.guardar()
            print(f"✅ Vehículo {placa.upper()} devuelto correctamente.")

def menu_vehiculos():
    gestor = GestorVehiculos()
    while True:
        print("\n=== SISTEMA DE ALQUILER DE VEHÍCULOS ===")
        print("1. Registrar vehículo\n2. Mostrar disponibles\n3. Alquilar\n4. Devolver\n5. Salir")
        op = input("Opción: ")
        if op == "1":
            tipo = input("Tipo (1:Auto 2:Moto 3:Camión): ")
            placa = input("Placa: ").upper()
            marca = input("Marca: "); modelo = input("Modelo: ")
            precio = float(input("Precio/día: "))
            disp = input("¿Disponible? (s/n): ").lower() == "s"
            if tipo == "1": kwargs = {"puertas": int(input("Puertas: "))}
            elif tipo == "2": kwargs = {"cilindraje": int(input("Cilindraje: "))}
            elif tipo == "3": kwargs = {"carga": float(input("Cap. Carga (t): "))}
            else: continue
            gestor.registrar(tipo, placa, marca, modelo, precio, disp, **kwargs)
        elif op == "2": gestor.mostrar_disponibles()
        elif op == "3":
            placa = input("Placa a alquilar: "); dias = int(input("Días: "))
            gestor.alquilar(placa, dias)
        elif op == "4": gestor.devolver(input("Placa a devolver: "))
        elif op == "5": break
        else: print("⚠️ Opción inválida.")

if __name__ == "__main__":
    menu_vehiculos()