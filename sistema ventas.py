import json
import os

class Producto:
    def __init__(self, codigo, nombre, precio, cantidad, vendidas=0):
        self._codigo = codigo.upper()
        self._nombre = nombre
        self._precio = precio
        self._cantidad = cantidad
        self._vendidas = vendidas

    @property
    def codigo(self): return self._codigo
    @property
    def nombre(self): return self._nombre
    @property
    def precio(self): return self._precio
    @property
    def cantidad(self): return self._cantidad
    @cantidad.setter
    def cantidad(self, v): self._cantidad = v
    @property
    def vendidas(self): return self._vendidas
    @vendidas.setter
    def vendidas(self, v): self._vendidas = v

    def to_dict(self):
        return {"tipo": "Producto", "codigo": self._codigo, "nombre": self._nombre,
                "precio": self._precio, "cantidad": self._cantidad, "vendidas": self._vendidas}
    def __str__(self):
        return f"[{self._codigo}] {self._nombre} | ${self._precio} | Stock: {self._cantidad} | Vendidos: {self._vendidas}"

class Computador(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, ram, proc, vendidas=0):
        super().__init__(codigo, nombre, precio, cantidad, vendidas); self._ram = ram; self._proc = proc
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "Computador"; d["ram"] = self._ram; d["proc"] = self._proc; return d
    def __str__(self): return f"{super().__str__()} (RAM: {self._ram}GB | Proc: {self._proc})"

class Celular(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, almacenamiento, camaras, vendidas=0):
        super().__init__(codigo, nombre, precio, cantidad, vendidas); self._alm = almacenamiento; self._cam = camaras
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "Celular"; d["almacenamiento"] = self._alm; d["camaras"] = self._cam; return d
    def __str__(self): return f"{super().__str__()} (Alm: {self._alm}GB | Cámaras: {self._cam})"

class Accesorio(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, categoria, vendidas=0):
        super().__init__(codigo, nombre, precio, cantidad, vendidas); self._categoria = categoria
    def to_dict(self):
        d = super().to_dict(); d["tipo"] = "Accesorio"; d["categoria"] = self._categoria; return d
    def __str__(self): return f"{super().__str__()} (Categoría: {self._categoria})"

class GestorTienda:
    def __init__(self, archivo="productos.json"):
        self.archivo = archivo; self.productos = {}; self.cargar()

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f: datos = json.load(f)
            for d in datos:
                t = d.pop("tipo")
                cls = {"Computador": Computador, "Celular": Celular, "Accesorio": Accesorio, "Producto": Producto}.get(t, Producto)
                p = cls(**d)
                self.productos[p.codigo] = p

    def guardar(self):
        with open(self.archivo, "w") as f: json.dump([p.to_dict() for p in self.productos.values()], f, indent=4)

    def registrar(self, tipo, cod, nom, precio, cant, **kwargs):
        if precio <= 0: print("❌ Precio inválido."); return
        if cant < 0: print("❌ Cantidad inválida."); return
        if cod.upper() in self.productos: print("❌ Código repetido."); return
        if tipo == "1": self.productos[cod.upper()] = Computador(cod, nom, precio, cant, kwargs["ram"], kwargs["proc"])
        elif tipo == "2": self.productos[cod.upper()] = Celular(cod, nom, precio, cant, kwargs["alm"], kwargs["cam"])
        elif tipo == "3": self.productos[cod.upper()] = Accesorio(cod, nom, precio, cant, kwargs["cat"])
        self.guardar(); print("✅ Producto registrado.")

    def vender(self, cod, cant):
        if cant <= 0: print("❌ Cantidad inválida."); return
        p = self.productos.get(cod.upper())
        if not p: print("❌ Producto no encontrado."); return
        if cant > p.cantidad: print("❌ Stock insuficiente."); return
        subtotal = p.precio * cant
        descuento = 0.08 if cant >= 3 else 0.0
        total_con_desc = subtotal * (1 - descuento)
        p.cantidad -= cant; p.vendidas += cant
        self.guardar()
        print(f"✅ Venta exitosa.\nSubtotal: ${subtotal:.2f} | Descuento: {descuento*100}% | Total: ${total_con_desc:.2f}")

    def reabastecer(self, cod, cant):
        if cant <= 0: print("❌ Cantidad inválida."); return
        p = self.productos.get(cod.upper())
        if not p: print("❌ Producto no encontrado."); return
        p.cantidad += cant; self.guardar()
        print(f"✅ Stock actualizado. Nuevo stock: {p.cantidad}")

def menu_tienda():
    gestor = GestorTienda()
    while True:
        print("\n=== TIENDA TECNOLÓGICA ===")
        print("1. Registrar\n2. Inventario\n3. Vender\n4. Reabastecer\n5. Buscar\n6. Salir")
        op = input("Opción: ")
        if op == "1":
            tipo = input("Tipo (1:PC 2:Cel 3:Acc): ")
            cod = input("Código: "); nom = input("Nombre: ")
            precio = float(input("Precio: ")); cant = int(input("Cantidad: "))
            if tipo == "1": kwargs = {"ram": int(input("RAM: ")), "proc": input("Proc: ")}
            elif tipo == "2": kwargs = {"alm": int(input("Alm(GB): ")), "cam": int(input("Cámaras: "))}
            elif tipo == "3": kwargs = {"cat": input("Categoría: ")}
            else: continue
            gestor.registrar(tipo, cod, nom, precio, cant, **kwargs)
        elif op == "2":
            for p in gestor.productos.values(): print(p)
        elif op == "3": gestor.vender(input("Código: "), int(input("Cantidad: ")))
        elif op == "4": gestor.reabastecer(input("Código: "), int(input("Cantidad a añadir: ")))
        elif op == "5":
            p = gestor.productos.get(input("Código: ").upper())
            print(p if p else "❌ No encontrado.")
        elif op == "6": break
        else: print("⚠️ Opción inválida.")

if __name__ == "__main__":
    menu_tienda()
    