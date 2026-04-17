import json
import os


# =====================================
# FUNCIÓN GENERAL
# =====================================
def cargar_json(archivo):

    if not os.path.exists(archivo):
        return []

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        print(f" Error leyendo {archivo}")
        return []


# =====================================
# REPORTE VEHÍCULOS
# =====================================
def reporte_vehiculo_costoso():

    vehiculos = cargar_json("vehiculos.json")

    if not vehiculos:
        print("📭 No hay vehículos registrados.")
        return

    mas_costoso = max(
        vehiculos,
        key=lambda v: v.get("precio_dia", 0)
    )

    print("\n🚗 VEHÍCULO MÁS COSTOSO")
    print(f"Tipo: {mas_costoso.get('tipo', 'N/A')}")
    print(f"Placa: {mas_costoso.get('placa', 'N/A').upper()}")
    print(f"Marca: {mas_costoso.get('marca', 'N/A')}")
    print(f"Modelo: {mas_costoso.get('modelo', 'N/A')}")
    print(
        f"Precio por día: "
        f"${mas_costoso.get('precio_dia', 0):.2f}"
    )


# =====================================
# REPORTE PACIENTES
# =====================================
def reporte_paciente_critico():

    pacientes = cargar_json("pacientes.json")

    pendientes = [
        p for p in pacientes
        if p.get("estado") == "Pendiente"
    ]

    if not pendientes:
        print("📭 No hay pacientes pendientes.")
        return

    urgencias = [
        p for p in pendientes
        if p.get("tipo") == "PacienteUrgencias"
    ]

    if urgencias:
        mas_critico = max(
            urgencias,
            key=lambda p: p.get("gravedad", 0)
        )

    else:
        prioritarios = [
            p for p in pendientes
            if p.get("tipo") == "PacientePrioritario"
        ]

        if prioritarios:
            mas_critico = prioritarios[0]

        else:
            generales = [
                p for p in pendientes
                if p.get("tipo") == "PacienteGeneral"
            ]

            mas_critico = generales[0]

    print("\n🏥 PACIENTE MÁS CRÍTICO")
    print(f"Tipo: {mas_critico.get('tipo')}")
    print(f"Nombre: {mas_critico.get('nombre')}")
    print(f"Estado: {mas_critico.get('estado')}")
# =====================================
# REPORTE PRODUCTOS
# =====================================
def reporte_producto_vendido():

    productos = cargar_json("productos.json")

    if not productos:
        print("📭 No hay productos registrados.")
        return

    vendidos = [
        p for p in productos
        if p.get("vendidas", 0) > 0
    ]

    if not vendidos:
        print("📭 Aún no se han realizado ventas.")
        return

    mas_vendido = max(
        vendidos,
        key=lambda p: p.get("vendidas", 0)
    )

    print("\n💻 PRODUCTO MÁS VENDIDO")
    print(f"Código: {mas_vendido['codigo']}")
    print(f"Nombre: {mas_vendido['nombre']}")
    print(f"Unidades vendidas: {mas_vendido['vendidas']}")


# =====================================
# MENÚ REPORTES
# =====================================
def menu_reportes():

    while True:

        print("\n====== MÓDULO DE REPORTES ======")
        print("1. Vehículo más costoso")
        print("2. Paciente más crítico")
        print("3. Producto más vendido")
        print("4. Salir")

        op = input("Opción: ").strip()

        # -------------------------
        if op == "1":
            reporte_vehiculo_costoso()

        elif op == "2":
            reporte_paciente_critico()

        elif op == "3":
            reporte_producto_vendido()

        elif op == "4":
            print(" Saliendo de reportes.")
            break

        else:
            print(" Opción inválida.")


# =====================================
if __name__ == "__main__":
    menu_reportes()