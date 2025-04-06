from scipy.optimize import minimize
import numpy as np
'''Método de localización'''
def fcn_localizacion(a, b, w):
    # Función a minimizar
    def weighted_distance(params):
        x, y = params
        return np.sum(w * np.sqrt((x - a)**2 + (y - b)**2))

    # Punto inicial para la optimización
    x_grav = sum(w*a) / sum(w)
    y_grav = sum(w*b) / sum(w)
    initial_guess = [x_grav, y_grav]

    # Optimización
    result = minimize(weighted_distance, initial_guess)

    # Solución óptima
    optimal_x, optimal_y = result.x
    print(f"Coordenadas óptimas: x = {optimal_x}, y = {optimal_y}")
    return optimal_x, optimal_y