import json
import os

def cargar_json(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r") as f: return json.load(f)
    return []

def reporte_vehiculo_costoso():
    vehiculos = cargar_json("vehiculos.json")
    if not vehiculos: print("📭 No hay vehículos registrados."); return
    mas_costoso = max(vehiculos, key=lambda v: v["precio_dia"])
    print(f"\n🚗 VEHÍCULO MÁS COSTOSO:")
    print(f"Placa: {mas_costoso['placa']} | Modelo: {mas_costoso['modelo']} | Precio/día: ${mas_costoso['precio_dia']:.2f}")

def reporte_paciente_critico():
    pacientes = cargar_json("pacientes.json")
    urgencias = [p for p in pacientes if p["tipo"] == "PacienteUrgencias" and p["estado"] == "Pendiente"]
    if not urgencias: print("📭 No hay pacientes de urgencias pendientes."); return
    mas_critico = max(urgencias, key=lambda p: p.get("gravedad", 0))
    print(f"\n🏥 PACIENTE MÁS CRÍTICO:")
    print(f"Nombre: {mas_critico['nombre']} | Gravedad: {mas_critico.get('gravedad', 'N/A')}/5 | Estado: {mas_critico['estado']}")

def reporte_producto_vendido():
    productos = cargar_json("productos.json")
    if not productos: print("📭 No hay productos registrados."); return
    mas_vendido = max(productos, key=lambda p: p.get("vendidas", 0))
    print(f"\n💻 PRODUCTO MÁS VENDIDO:")
    print(f"Código: {mas_vendido['codigo']} | Nombre: {mas_vendido['nombre']} | Unidades vendidas: {mas_vendido.get('vendidas', 0)}")

def menu_reportes():
    while True:
        print("\n=== MÓDULO DE REPORTES ===")
        print("1. Vehículo más costoso\n2. Paciente más crítico\n3. Producto más vendido\n4. Salir")
        op = input("Opción: ")
        if op == "1": reporte_vehiculo_costoso()
        elif op == "2": reporte_paciente_critico()
        elif op == "3": reporte_producto_vendido()
        elif op == "4": break
        else: print("⚠️ Opción inválida.")

if __name__ == "__main__":
    menu_reportes()