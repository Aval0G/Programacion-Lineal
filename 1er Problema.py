import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Coeficientes de la función objetivo (minimizar Z = 12A + 8B)
c = np.array([12, 8])  # Costos de los alimentos A y B

# Coeficientes de las restricciones (Ax <= b)
A = np.array([
    [-2, -3],  # Vitamina W
    [-4, -3],  # Vitamina X
    [-7, -6]   # Vitamina Y
])

b = np.array([-30, -50, -60])  # Límite derecho

# Llamar a la función linprog para resolver el problema
result = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

# Mostrar los resultados en la consola
if result.success:
    A_opt = result.x[0]
    B_opt = result.x[1]
    cost_opt = result.fun

    print("Solución óptima:")
    print(f"Cantidad de alimento A (A): {A_opt:.4f}")
    print(f"Cantidad de alimento B (B): {B_opt:.4f}")
    print(f"Costo mínimo total: {cost_opt:.2f} centavos")
else:
    print("No se pudo encontrar una solución óptima.")

# Crear un rango para las proporciones de A
A_vals = np.linspace(0, 20, 400)

# Calcular las restricciones
B_vals_w = (30 - 2 * A_vals) / 3  # Restricción Vitamina W
B_vals_x = (50 - 4 * A_vals) / 3  # Restricción Vitamina X
B_vals_y = (60 - 7 * A_vals) / 6  # Restricción Vitamina Y

# Graficar las restricciones
plt.figure(figsize=(10, 8))
plt.plot(A_vals, B_vals_w, label='2A + 3B ≤ 30 (Vitamina W)', color='blue')
plt.plot(A_vals, B_vals_x, label='4A + 3B ≤ 50 (Vitamina X)', color='green')
plt.plot(A_vals, B_vals_y, label='7A + 6B ≤ 60 (Vitamina Y)', color='red')

# Calcular la intersección de todas las restricciones
B_intersection = np.maximum(np.maximum(B_vals_w, B_vals_x), B_vals_y)

# Sombrear el área no factible (lo que está por fuera de la región factible)
plt.fill_between(A_vals, B_intersection, 20, color='gray', alpha=0.3, label='Área factible')

# Añadir líneas de la función objetivo para diferentes valores de Z (costos)
Z_vals = [120, 130, 133, 150, 180, 200]  # Valores del costo objetivo
for Z in Z_vals:
    B_Z = (Z - 12 * A_vals) / 8  # Despejar B de Z = 12A + 8B
    plt.plot(A_vals, B_Z, '--', label=f'Z = {Z}', alpha=0.7)

# Graficar la solución óptima
if result.success:
    plt.plot(A_opt, B_opt, 'ro', label='Solución óptima')
    plt.text(A_opt + 0.5, B_opt + 0.5, f'({A_opt:.2f}, {B_opt:.2f})', fontsize=12, color='red')

# Función para mostrar coordenadas al pasar el mouse
def on_hover(event):
    if event.inaxes == plt.gca():  # Si el mouse está dentro de los ejes
        x = event.xdata
        y = event.ydata
        plt.gca().set_title(f'A: {x:.2f}, B: {y:.2f}', fontsize=12)
        plt.draw()  # Redibujar la figura

# Conectar el evento de movimiento del mouse a la función on_hover
plt.gcf().canvas.mpl_connect('motion_notify_event', on_hover)

# Configuración del gráfico
plt.xlim(0, 20)  # Expandir los límites del gráfico
plt.ylim(0, 20)
plt.xlabel('Cantidad de Alimento A (onzas)')
plt.ylabel('Cantidad de Alimento B (onzas)')
plt.title('Problema de Dieta - Programación Lineal')
plt.axhline(0, color='black', linewidth=0.5, ls='--')
plt.axvline(0, color='black', linewidth=0.5, ls='--')
plt.grid()
plt.legend()
plt.show()
