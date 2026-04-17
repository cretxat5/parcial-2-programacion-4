#2. Sistema de atención de pacientes en una clínica
import json
import os


# -------------------------
# CLASE BASE
# -------------------------
class Paciente:
    def __init__(self, documento, nombre, edad, estado="Pendiente"):
        self._documento = documento.strip()
        self._nombre = nombre.strip()
        self._edad = int(edad)
        self._estado = estado

    @property
    def documento(self):
        return self._documento

    @property
    def nombre(self):
        return self._nombre

    @property
    def edad(self):
        return self._edad

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        self._estado = valor

    def to_dict(self):
        return {
            "tipo": "Paciente",
            "documento": self._documento,
            "nombre": self._nombre,
            "edad": self._edad,
            "estado": self._estado
        }

    def __str__(self):
        return f"[{self._documento}] {self._nombre} - {self._edad} años | {self._estado}"


# -------------------------
# SUBCLASES
# -------------------------
class PacienteGeneral(Paciente):
    def __init__(self, documento, nombre, edad, eps, estado="Pendiente"):
        super().__init__(documento, nombre, edad, estado)
        self._eps = eps.strip()

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "PacienteGeneral"
        d["eps"] = self._eps
        return d

    def __str__(self):
        return f"[General] {super().__str__()} | EPS: {self._eps}"


class PacientePrioritario(Paciente):
    def __init__(self, documento, nombre, edad, condicion, estado="Pendiente"):
        super().__init__(documento, nombre, edad, estado)
        self._condicion = condicion.strip()

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "PacientePrioritario"
        d["condicion"] = self._condicion
        return d

    def __str__(self):
        return f"[Prioritario] {super().__str__()} | Condición: {self._condicion}"


class PacienteUrgencias(Paciente):
    def __init__(self, documento, nombre, edad, gravedad, estado="Pendiente"):
        super().__init__(documento, nombre, edad, estado)
        self._gravedad = int(gravedad)

    @property
    def gravedad(self):
        return self._gravedad

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "PacienteUrgencias"
        d["gravedad"] = self._gravedad
        return d

    def __str__(self):
        return f"[Urgencias] {super().__str__()} | Gravedad: {self._gravedad}/5"


# -------------------------
# GESTOR
# -------------------------
class GestorPacientes:
    def __init__(self, archivo="pacientes.json"):
        self.archivo = archivo
        self.pacientes = {}
        self.cargar()

    # -------------------------
    def cargar(self):
        if not os.path.exists(self.archivo):
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except:
            print(" Error al leer archivo JSON.")
            self.pacientes = {}
            return

        for d in datos:
            tipo = d.get("tipo")

            try:
                if tipo == "PacienteGeneral":
                    p = PacienteGeneral(
                        d["documento"], d["nombre"], d["edad"],
                        d["eps"], d["estado"]
                    )

                elif tipo == "PacientePrioritario":
                    p = PacientePrioritario(
                        d["documento"], d["nombre"], d["edad"],
                        d["condicion"], d["estado"]
                    )

                elif tipo == "PacienteUrgencias":
                    p = PacienteUrgencias(
                        d["documento"], d["nombre"], d["edad"],
                        d["gravedad"], d["estado"]
                    )

                else:
                    p = Paciente(
                        d["documento"], d["nombre"], d["edad"],
                        d["estado"]
                    )

                self.pacientes[p.documento] = p

            except:
                continue

    # -------------------------
    def guardar(self):
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(
                    [p.to_dict() for p in self.pacientes.values()],
                    f,
                    indent=4,
                    ensure_ascii=False
                )
        except:
            print(" Error al guardar archivo.")

    # -------------------------
    def registrar(self, tipo, doc, nombre, edad, **kwargs):

        doc = doc.strip()
        nombre = nombre.strip()

        if not doc:
            print(" Documento vacío.")
            return

        if doc in self.pacientes:
            print(" Documento repetido.")
            return

        if not nombre:
            print(" Nombre inválido.")
            return

        try:
            edad = int(edad)
            if edad <= 0 or edad > 120:
                print(" Edad inválida.")
                return
        except:
            print(" Edad inválida.")
            return

        if tipo == "1":
            eps = kwargs.get("eps", "").strip()

            if not eps:
                print(" EPS inválida.")
                return

            self.pacientes[doc] = PacienteGeneral(doc, nombre, edad, eps)

        elif tipo == "2":
            condicion = kwargs.get("condicion", "").strip()

            if not condicion:
                print(" Condición inválida.")
                return

            self.pacientes[doc] = PacientePrioritario(
                doc, nombre, edad, condicion
            )

        elif tipo == "3":
            try:
                gravedad = int(kwargs.get("gravedad"))

                if gravedad < 1 or gravedad > 5:
                    print(" Gravedad debe estar entre 1 y 5.")
                    return

            except:
                print(" Gravedad inválida.")
                return

            self.pacientes[doc] = PacienteUrgencias(
                doc, nombre, edad, gravedad
            )

        else:
            print("Tipo inválido.")
            return

        self.guardar()
        print("✅ Paciente registrado correctamente.")

    # -------------------------
    def mostrar_todos(self):
        if not self.pacientes:
            print("📭 No hay pacientes registrados.")
            return

        print("\n📋 LISTA DE PACIENTES")
        for p in self.pacientes.values():
            print(p)

    # -------------------------
    def buscar(self, doc):
        doc = doc.strip()

        if doc in self.pacientes:
            print(self.pacientes[doc])
        else:
            print(" Paciente no encontrado.")

    # -------------------------
    def atender_siguiente(self):

        pendientes = [
            p for p in self.pacientes.values()
            if p.estado == "Pendiente"
        ]

        if not pendientes:
            print("📭 No hay pacientes pendientes.")
            return

        urgencias = [
            p for p in pendientes
            if isinstance(p, PacienteUrgencias)
        ]

        if urgencias:
            urgencias.sort(
                key=lambda x: x.gravedad,
                reverse=True
            )
            siguiente = urgencias[0]

        else:
            prioritarios = [
                p for p in pendientes
                if isinstance(p, PacientePrioritario)
            ]

            if prioritarios:
                siguiente = prioritarios[0]

            else:
                generales = [
                    p for p in pendientes
                    if isinstance(p, PacienteGeneral)
                ]

                siguiente = generales[0]

        siguiente.estado = "Atendido"
        self.guardar()

        print("\n✅ PACIENTE ATENDIDO:")
        print(siguiente)


# -------------------------
# MENÚ
# -------------------------
def menu():

    gestor = GestorPacientes()

    while True:

        print("\n===== SISTEMA CLÍNICA =====")
        print("1. Registrar paciente")
        print("2. Mostrar pacientes")
        print("3. Buscar paciente")
        print("4. Atender siguiente")
        print("5. Salir")

        op = input("Opción: ").strip()

        # -------------------------
        if op == "1":

            tipo = input(
                "Tipo (1 General / 2 Prioritario / 3 Urgencias): "
            ).strip()

            if tipo not in ("1", "2", "3"):
                print(" Tipo inválido.")
                continue

            doc = input("Documento: ").strip()

            if not doc:
                print(" Documento vacío.")
                continue

            if doc in gestor.pacientes:
                print("❌ Ese documento ya está registrado.")
                continue
            nombre = input("Nombre: ").strip().title()
            edad = input("Edad: ")

            kwargs = {}

            if tipo == "1":
                kwargs["eps"] = input("EPS: ")

            elif tipo == "2":
                kwargs["condicion"] = input(
                    "Condición especial: "
                )

            elif tipo == "3":
                kwargs["gravedad"] = input(
                    "Nivel gravedad (1 a 5): "
                )

            gestor.registrar(
                tipo, doc, nombre, edad, **kwargs
            )

        # -------------------------
        elif op == "2":
            gestor.mostrar_todos()

        # -------------------------
        elif op == "3":
            doc = input("Documento a buscar: ")
            gestor.buscar(doc)

        # -------------------------
        elif op == "4":
            gestor.atender_siguiente()

        # -------------------------
        elif op == "5":
            print(" Saliendo del sistema.")
            break

        # -------------------------
        else:
            print(" Opción inválida.")


# -------------------------
if __name__ == "__main__":
    menu()