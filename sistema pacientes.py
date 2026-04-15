import json
import os

class Paciente:
    def __init__(self, documento, nombre, edad, estado="Pendiente"):
        self._documento = documento
        self._nombre = nombre
        self._edad = edad
        self._estado = estado

    @property
    def documento(self): return self._documento
    @property
    def nombre(self): return self._nombre
    @property
    def edad(self): return self._edad
    @property
    def estado(self): return self._estado
    @estado.setter
    def estado(self, v): self._estado = v

    def to_dict(self):
        return {"tipo": "Paciente", "documento": self._documento, "nombre": self._nombre,
                "edad": self._edad, "estado": self._estado}
    def __str__(self):
        return f"[{self._documento}] {self._nombre} ({self._edad}a) | Estado: {self._estado}"

class PacienteGeneral(Paciente):
    def __init__(self, documento, nombre, edad, eps, estado="Pendiente"):
        super().__init__(documento, nombre, edad, estado); self._eps = eps
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "PacienteGeneral"; d["eps"] = self._eps; return d
    def __str__(self): return f"{super().__str__()} | EPS: {self._eps}"

class PacientePrioritario(Paciente):
    def __init__(self, documento, nombre, edad, condicion, estado="Pendiente"):
        super().__init__(documento, nombre, edad, estado); self._condicion = condicion
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "PacientePrioritario"; d["condicion"] = self._condicion; return d
    def __str__(self): return f"{super().__str__()} | Condición: {self._condicion}"

class PacienteUrgencias(Paciente):
    def __init__(self, documento, nombre, edad, gravedad, estado="Pendiente"):
        super().__init__(documento, nombre, edad, estado); self._gravedad = gravedad
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "PacienteUrgencias"; d["gravedad"] = self._gravedad; return d
    def __str__(self): return f"{super().__str__()} | Gravedad: {self._gravedad}/5"

class GestorPacientes:
    def __init__(self, archivo="pacientes.json"):
        self.archivo = archivo; self.pacientes = {}; self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f: datos = json.load(f)
            for d in datos:
                t = d.pop("tipo")
                cls = {"PacienteGeneral": PacienteGeneral, "PacientePrioritario": PacientePrioritario,
                       "PacienteUrgencias": PacienteUrgencias, "Paciente": Paciente}.get(t, Paciente)
                p = cls(**d)
                self.pacientes[p.documento] = p

    def guardar(self):
        with open(self.archivo, "w") as f: json.dump([p.to_dict() for p in self.pacientes.values()], f, indent=4)

    def registrar(self, tipo, doc, nombre, edad, **kwargs):
        if not (0 < edad < 120): print("❌ Edad inválida."); return
        if doc in self.pacientes: print("❌ Documento ya registrado."); return
        if tipo == "1": self.pacientes[doc] = PacienteGeneral(doc, nombre, edad, kwargs["eps"])
        elif tipo == "2": self.pacientes[doc] = PacientePrioritario(doc, nombre, edad, kwargs["cond"])
        elif tipo == "3": self.pacientes[doc] = PacienteUrgencias(doc, nombre, edad, int(kwargs["grav"]))
        self.guardar(); print("✅ Paciente registrado.")

    def buscar(self, doc):
        p = self.pacientes.get(doc)
        print(p if p else "❌ No encontrado.")

    def atender_siguiente(self):
        pendientes = [p for p in self.pacientes.values() if p.estado == "Pendiente"]
        if not pendientes: print("📭 No hay pacientes pendientes."); return
        # Prioridad: Urgencias > Prioritarios > Generales
        prioridad = {"PacienteUrgencias": 1, "PacientePrioritario": 2, "PacienteGeneral": 3}
        pendientes.sort(key=lambda x: prioridad.get(type(x).__name__, 4))
        siguiente = pendientes[0]
        siguiente.estado = "Atendido"
        self.guardar()
        print(f"✅ Atendido: {siguiente}")

def menu_pacientes():
    gestor = GestorPacientes()
    while True:
        print("\n=== SISTEMA CLÍNICA DE PACIENTES ===")
        print("1. Registrar\n2. Mostrar todos\n3. Buscar por documento\n4. Atender siguiente\n5. Salir")
        op = input("Opción: ")
        if op == "1":
            tipo = input("Tipo (1:General 2:Prioritario 3:Urgencias): ")
            doc = input("Documento: "); nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            if tipo == "1": kwargs = {"eps": input("EPS: ")}
            elif tipo == "2": kwargs = {"cond": input("Condición: ")}
            elif tipo == "3": kwargs = {"grav": input("Gravedad (1-5): ")}
            else: continue
            gestor.registrar(tipo, doc, nombre, edad, **kwargs)
        elif op == "2":
            for p in gestor.pacientes.values(): print(p)
        elif op == "3": gestor.buscar(input("Documento: "))
        elif op == "4": gestor.atender_siguiente()
        elif op == "5": break
        else: print("⚠️ Opción inválida.")

if __name__ == "__main__":
    menu_pacientes()