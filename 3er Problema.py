import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Coeficientes de la función objetivo (maximizar retorno => minimizar -Z = -10S - 8B)
c = np.array([-10, -8])  # Maximizar el retorno: Z = 10S + 8B

# Restricciones (A_ub * x <= b_ub)
A = np.array([
    [-1, -1],          # S + B <= 10,000 -> -S - B <= -10,000
    [3, -1],           # 3S - B <= 0 -> B >= 3S
    [-9, 1],           # -9S + B <= 0 -> B <= 9S
    [0, -1]            # B >= 4,000 -> -B <= -4,000
])

b = np.array([-10000, 0, 0, -4000])  # Límite derecho

# Restricción de igualdad (S + B = 10,000)
A_eq = np.array([[1, 1]])
b_eq = np.array([10000])

# Llamar a la función linprog para resolver el problema
result = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))

# Mostrar los resultados en la consola
if result.success:
    S_opt = result.x[0]
    B_opt = result.x[1]
    retorno_opt = -result.fun  # Cambiar de nuevo a positivo

    print("Solución óptima:")
    print(f"Inversión en acciones (S): ${S_opt:.2f}")
    print(f"Inversión en bonos (B): ${B_opt:.2f}")
    print(f"Retorno anual máximo: ${retorno_opt:.2f}")
else:
    print("No se pudo encontrar una solución óptima.")

# Crear un rango para las inversiones en acciones
S_vals = np.linspace(0, 4000, 100)

# Calcular las restricciones de inversión en bonos
B_budget = 10000 - S_vals  # Restricción de total S + B = 10,000
B_min_25 = 3 * S_vals  # B >= 3S (de S <= 0.25(S + B))
B_max_10 = 9 * S_vals  # B <= 9S (de S >= 0.1(S + B))
B_min_fixed = np.full_like(S_vals, 4000)  # Línea horizontal para B >= 4,000

# Limitar el área factible entre las intersecciones de las restricciones
plt.figure(figsize=(10, 8))
plt.plot(S_vals, B_budget, label='S + B = 10,000', color='blue')
plt.plot(S_vals, B_min_25, label='B ≥ 3S', color='orange')
plt.plot(S_vals, B_max_10, label='B ≤ 9S', color='green')
plt.plot(S_vals, B_min_fixed, label='B ≥ 4,000', color='red')

# Encontrar el área factible limitada por las restricciones
B_upper = np.minimum(B_budget, B_max_10)  # El valor máximo permitido entre el presupuesto y B <= 9S
B_lower = np.maximum(B_min_25, B_min_fixed)  # El valor mínimo permitido entre B >= 3S y B >= 4000

# Sombrear solo el área factible (triangular)
plt.fill_between(S_vals, B_lower, B_upper, where=(B_upper >= B_lower), color='gray', alpha=0.3, label='Área factible')

# Añadir líneas de la función objetivo para diferentes valores de Z
Z_vals = [60000, 70000, 80000, 85000, 90000]  # Valores del retorno objetivo
for Z in Z_vals:
    B_Z = (Z - 10 * S_vals) / 8  # Despejar B de Z = 10S + 8B
    plt.plot(S_vals, B_Z, '--', label=f'Z = {Z}', alpha=0.7)

# Graficar la solución óptima
if result.success:
    plt.plot(S_opt, B_opt, 'ro', label='Solución óptima')
    plt.text(S_opt + 50, B_opt + 50, f'({S_opt:.2f}, {B_opt:.2f})', fontsize=12, color='red')

# Función para mostrar coordenadas al pasar el mouse
def on_hover(event):
    if event.inaxes == plt.gca():  # Si el mouse está dentro de los ejes
        x = event.xdata
        y = event.ydata
        plt.gca().set_title(f'S: {x:.2f}, B: {y:.2f}', fontsize=12)
        plt.draw()  # Redibujar la figura

# Conectar el evento de movimiento del mouse a la función on_hover
plt.gcf().canvas.mpl_connect('motion_notify_event', on_hover)

# Configuración del gráfico
plt.xlim(0, 4000)
plt.ylim(0, 10000)
plt.xlabel('Inversión en Acciones (S)')
plt.ylabel('Inversión en Bonos (B)')
plt.title('Problema de Inversión - Programación Lineal')
plt.axhline(0, color='black', linewidth=0.5, ls='--')
plt.axvline(0, color='black', linewidth=0.5, ls='--')
plt.grid()
plt.legend()
plt.show()
