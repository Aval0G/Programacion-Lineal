import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Coeficientes de la función objetivo (minimizar Z = 25X + 20Y)
c = np.array([25, 20])

# Coeficientes de las restricciones (Ax <= b)
A = np.array([
    [0.05, 0.07],  # Fosfatos
    [0.02, 0.01]   # Cloruro
])

b = np.array([0.06, 0.015])  # Límite derecho

# Restricción de igualdad (X + Y = 1)
A_eq = np.array([[1, 1]])
b_eq = np.array([1])

# Llamar a la función linprog para resolver el problema
result = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))

# Mostrar los resultados en la consola
if result.success:
    X_opt = result.x[0]
    Y_opt = result.x[1]
    cost_opt = result.fun

    print("Solución óptima:")
    print(f"Proporción de ingrediente 1 (X): {X_opt:.4f} onzas por onza de solución")
    print(f"Proporción de ingrediente 2 (Y): {Y_opt:.4f} onzas por onza de solución")
    print(f"Costo mínimo total: {cost_opt:.2f} centavos")
else:
    print("No se pudo encontrar una solución óptima.")

# Crear un rango para las proporciones de X
X_vals = np.linspace(0, 1, 100)

# Calcular las restricciones
Y_vals_fosfatos = (0.06 - 0.05 * X_vals) / 0.07  # Restricción de fosfatos
Y_vals_cloruro = (0.015 - 0.02 * X_vals) / 0.01   # Restricción de cloruro

# Graficar las restricciones
plt.figure(figsize=(10, 8))
plt.plot(X_vals, Y_vals_fosfatos, label='0.05X + 0.07Y ≤ 0.06 (Fosfatos)', color='blue')
plt.plot(X_vals, Y_vals_cloruro, label='0.02X + 0.01Y ≤ 0.015 (Cloruro)', color='green')

# Área de factibilidad
plt.fill_between(X_vals, 0, np.minimum(Y_vals_fosfatos, Y_vals_cloruro), 
                 where=(np.minimum(Y_vals_fosfatos, Y_vals_cloruro) >= 0), 
                 color='gray', alpha=0.5, label='Área factible')

# Añadir líneas de la función objetivo para diferentes valores de Z (costos)
Z_vals = [20, 22.5, 25, 27.5, 30]  # Valores del costo objetivo
for Z in Z_vals:
    Y_Z = (Z - 25 * X_vals) / 20  # Despejar Y de Z = 25X + 20Y
    plt.plot(X_vals, Y_Z, '--', label=f'Z = {Z}', alpha=0.7)

# Graficar la solución óptima
if result.success:
    plt.plot(X_opt, Y_opt, 'ro', label='Solución óptima')
    plt.text(X_opt + 0.01, Y_opt + 0.01, f'({X_opt:.4f}, {Y_opt:.4f})', fontsize=12, color='red')

# Función para mostrar coordenadas al pasar el mouse
def on_hover(event):
    if event.inaxes == plt.gca():  # Si el mouse está dentro de los ejes
        x = event.xdata
        y = event.ydata
        plt.gca().set_title(f'X: {x:.2f}, Y: {y:.2f}', fontsize=12)
        plt.draw()  # Redibujar la figura

# Conectar el evento de movimiento del mouse a la función on_hover
plt.gcf().canvas.mpl_connect('motion_notify_event', on_hover)

# Configuración del gráfico
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.xlabel('Proporción de Ingrediente 1 (X)')
plt.ylabel('Proporción de Ingrediente 2 (Y)')
plt.title('Problema de Mezcla - Programación Lineal')
plt.axhline(0, color='black', linewidth=0.5, ls='--')
plt.axvline(0, color='black', linewidth=0.5, ls='--')
plt.grid()
plt.legend()
plt.show()
