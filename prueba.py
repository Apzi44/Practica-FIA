from collections import deque

productos = {
    "Bola": 30,
    "Paleta": 10,
    "Promo1": 50,
    "Promo2": 70
}

estado_inicial = (150, [])
cola = deque([estado_inicial])
combinaciones = []

while cola:
    dinero, compras = cola.popleft()
    
    # Si ya cumple la condición, la guardamos
    if "Promo2" in compras:
        combinaciones.append((dinero, compras))
    
    # Generar nuevos estados
    for producto, costo in productos.items():
        nuevo_dinero = dinero - costo
        if nuevo_dinero >= 0:
            nuevo_estado = (nuevo_dinero, compras + [producto])
            cola.append(nuevo_estado)

# Eliminar duplicados
combinaciones_unicas = set(tuple(sorted(c)) for _, c in combinaciones)
for combinacion in combinaciones_unicas:
    print(f", Compras: {combinacion[1:]}, Dinero restante: {150 - sum(productos[p] for p in combinacion[1:])}")
