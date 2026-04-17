import json
import os


# =====================================
# CLASE BASE
# =====================================
class Producto:
    def __init__(self, codigo, nombre, precio, cantidad, vendidas=0):
        self._codigo = codigo.strip().upper()
        self._nombre = nombre.strip().title()
        self._precio = float(precio)
        self._cantidad = int(cantidad)
        self._vendidas = int(vendidas)

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        self._cantidad = valor

    @property
    def vendidas(self):
        return self._vendidas

    @vendidas.setter
    def vendidas(self, valor):
        self._vendidas = valor

    def to_dict(self):
        return {
            "tipo": "Producto",
            "codigo": self._codigo,
            "nombre": self._nombre,
            "precio": self._precio,
            "cantidad": self._cantidad,
            "vendidas": self._vendidas
        }

    def __str__(self):
        return f"[{self._codigo}] {self._nombre} | ${self._precio:.2f} | Stock: {self._cantidad} | Vendidos: {self._vendidas}"


# =====================================
# SUBCLASES
# =====================================
class Computador(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, ram, procesador, vendidas=0):
        super().__init__(codigo, nombre, precio, cantidad, vendidas)
        self._ram = int(ram)
        self._procesador = procesador.strip().title()

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "Computador"
        d["ram"] = self._ram
        d["procesador"] = self._procesador
        return d

    def __str__(self):
        return f"[COMPUTADOR] {super().__str__()} | RAM: {self._ram}GB | CPU: {self._procesador}"


class Celular(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, almacenamiento, camaras, vendidas=0):
        super().__init__(codigo, nombre, precio, cantidad, vendidas)
        self._almacenamiento = int(almacenamiento)
        self._camaras = int(camaras)

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "Celular"
        d["almacenamiento"] = self._almacenamiento
        d["camaras"] = self._camaras
        return d

    def __str__(self):
        return f"[CELULAR] {super().__str__()} | Almacenamiento: {self._almacenamiento}GB | Cámaras: {self._camaras}"


class Accesorio(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, categoria, vendidas=0):
        super().__init__(codigo, nombre, precio, cantidad, vendidas)
        self._categoria = categoria.strip().title()

    def to_dict(self):
        d = super().to_dict()
        d["tipo"] = "Accesorio"
        d["categoria"] = self._categoria
        return d

    def __str__(self):
        return f"[ACCESORIO] {super().__str__()} | Categoría: {self._categoria}"


# =====================================
# GESTOR
# =====================================
class GestorTienda:
    def __init__(self, archivo="productos.json"):
        self.archivo = archivo
        self.productos = {}
        self.cargar()

    # -------------------------------
    def cargar(self):
        if not os.path.exists(self.archivo):
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except:
            print(" Error leyendo archivo.")
            return

        for d in datos:
            tipo = d.get("tipo")

            try:
                if tipo == "Computador":
                    p = Computador(
                        d["codigo"], d["nombre"], d["precio"],
                        d["cantidad"], d["ram"],
                        d["procesador"], d["vendidas"]
                    )

                elif tipo == "Celular":
                    p = Celular(
                        d["codigo"], d["nombre"], d["precio"],
                        d["cantidad"], d["almacenamiento"],
                        d["camaras"], d["vendidas"]
                    )

                elif tipo == "Accesorio":
                    p = Accesorio(
                        d["codigo"], d["nombre"], d["precio"],
                        d["cantidad"], d["categoria"],
                        d["vendidas"]
                    )

                else:
                    p = Producto(
                        d["codigo"], d["nombre"], d["precio"],
                        d["cantidad"], d["vendidas"]
                    )

                self.productos[p.codigo] = p

            except:
                continue

    # -------------------------------
    def guardar(self):
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(
                    [p.to_dict() for p in self.productos.values()],
                    f,
                    indent=4,
                    ensure_ascii=False
                )
        except:
            print(" Error al guardar.")

    # -------------------------------
    def registrar(self, tipo, codigo, nombre, precio, cantidad, **kwargs):

        codigo = codigo.strip().upper()
        nombre = nombre.strip().title()

        if not codigo:
            print(" Código vacío.")
            return

        if codigo in self.productos:
            print(" Código repetido.")
            return

        if not nombre:
            print(" Nombre inválido.")
            return

        try:
            precio = float(precio)
            if precio <= 0:
                print(" Precio inválido.")
                return
        except:
            print(" Precio inválido.")
            return

        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                print(" Cantidad inválida.")
                return
        except:
            print(" Cantidad inválida.")
            return

        if tipo == "1":
            try:
                ram = int(kwargs["ram"])
                if ram <= 0:
                    print(" RAM inválida.")
                    return
            except:
                print(" RAM inválida.")
                return

            procesador = kwargs["procesador"].strip()

            if not procesador:
                print(" Procesador inválido.")
                return

            self.productos[codigo] = Computador(
                codigo, nombre, precio, cantidad,
                ram, procesador
            )

        elif tipo == "2":
            try:
                alm = int(kwargs["almacenamiento"])
                cam = int(kwargs["camaras"])

                if alm <= 0 or cam <= 0:
                    print(" Datos inválidos.")
                    return
            except:
                print(" Datos inválidos.")
                return

            self.productos[codigo] = Celular(
                codigo, nombre, precio,
                cantidad, alm, cam
            )

        elif tipo == "3":
            categoria = kwargs["categoria"].strip()

            if not categoria:
                print(" Categoría inválida.")
                return

            self.productos[codigo] = Accesorio(
                codigo, nombre, precio,
                cantidad, categoria
            )

        else:
            print(" Tipo inválido.")
            return

        self.guardar()
        print("✅ Producto registrado correctamente.")

    # -------------------------------
    def mostrar_inventario(self):

        if not self.productos:
            print("📭 No hay productos registrados.")
            return

        print("\n📦 INVENTARIO")
        for p in self.productos.values():
            print(p)

    # -------------------------------
    def buscar(self, codigo):

        codigo = codigo.strip().upper()

        p = self.productos.get(codigo)

        if p:
            print(p)
        else:
            print(" Producto no encontrado.")

    # -------------------------------
    def vender(self, codigo, cantidad):

        codigo = codigo.strip().upper()

        if codigo not in self.productos:
            print(" Producto no encontrado.")
            return

        try:
            cantidad = int(cantidad)

            if cantidad <= 0:
                print(" Cantidad inválida.")
                return

        except:
            print(" Cantidad inválida.")
            return

        p = self.productos[codigo]

        if cantidad > p.cantidad:
            print(" Stock insuficiente.")
            return

        subtotal = p.precio * cantidad

        descuento = 0

        # descuento por cantidad
        if cantidad >= 3:
            descuento += subtotal * 0.08

        # descuento adicional
        if subtotal > 3000000:
            descuento += subtotal * 0.05

        total = subtotal - descuento

        p.cantidad -= cantidad
        p.vendidas += cantidad

        self.guardar()

        print("\n✅ Venta realizada")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Descuento: ${descuento:.2f}")
        print(f"Total: ${total:.2f}")

    # -------------------------------
    def reabastecer(self, codigo, cantidad):

        codigo = codigo.strip().upper()

        if codigo not in self.productos:
            print(" Producto no encontrado.")
            return

        try:
            cantidad = int(cantidad)

            if cantidad <= 0:
                print(" Cantidad inválida.")
                return

        except:
            print(" Cantidad inválida.")
            return

        self.productos[codigo].cantidad += cantidad

        self.guardar()

        print("✅ Stock actualizado.")

    # -------------------------------


# =====================================
# MENÚ
# =====================================
def menu():

    gestor = GestorTienda()

    while True:

        print("\n====== TIENDA TECNOLÓGICA ======")
        print("1. Registrar producto")
        print("2. Mostrar inventario")
        print("3. Buscar producto")
        print("4. Vender producto")
        print("5. Reabastecer")
        print("6. Salir")

        op = input("Opción: ").strip()

        # ---------------------------
        if op == "1":

            tipo = input(
                "Tipo (1 Computador / 2 Celular / 3 Accesorio): "
            ).strip()

            if tipo not in ("1", "2", "3"):
                print(" Tipo inválido.")
                continue

            codigo = input("Código: ").strip().upper()

            if not codigo:
                print(" Código vacío.")
                continue

            if codigo in gestor.productos:
                print(" Código repetido.")
                continue

            nombre = input("Nombre: ").strip().title()

            if not nombre:
                print(" Nombre inválido.")
                continue

            precio = input("Precio: ")
            cantidad = input("Cantidad: ")

            kwargs = {}

            if tipo == "1":
                kwargs["ram"] = input("RAM GB: ")
                kwargs["procesador"] = input("Procesador: ")

            elif tipo == "2":
                kwargs["almacenamiento"] = input("Almacenamiento GB: ")
                kwargs["camaras"] = input("Número cámaras: ")

            elif tipo == "3":
                kwargs["categoria"] = input("Categoría: ")

            gestor.registrar(
                tipo, codigo, nombre,
                precio, cantidad, **kwargs
            )

        # ---------------------------
        elif op == "2":
            gestor.mostrar_inventario()

        # ---------------------------
        elif op == "3":
            codigo = input("Código a buscar: ")
            gestor.buscar(codigo)

        # ---------------------------
        elif op == "4":

            codigo = input("Código: ").strip().upper()

            if codigo not in gestor.productos:
              print(" Producto no registrado.")
              continue

            cantidad = input("Cantidad: ")
            gestor.vender(codigo, cantidad)

        # ---------------------------
        elif op == "5":

          codigo = input("Código: ").strip().upper()

          if codigo not in gestor.productos:
           print(" Producto no registrado.")
           continue

          cantidad = input("Cantidad a añadir: ")
          gestor.reabastecer(codigo, cantidad)
        # ---------------------------


        elif op == "6":
            print(" Saliendo del sistema.")
            break

        else:
            print(" Opción inválida.")


# =====================================
if __name__ == "__main__":
    menu()