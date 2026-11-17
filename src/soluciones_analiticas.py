
"""
Soluciones analíticas de las ecuaciones de Friedmann.

Modelo:
    Universo homogéneo e isótropo (FLRW)
    Materia sin presión: p = 0
    Constante cosmológica: Lambda = 0

Variables adimensionales:
    x = a/a_*
    tau = t/t_*

Ecuación de Friedmann:
    (dx/dtau)^2 = 2/x - k
"""

import numpy as np


def validar_parametro(valor, nombre):
    """Comprueba que el parámetro sea finito y no negativo."""
    arreglo = np.asarray(valor, dtype=float)

    if not np.all(np.isfinite(arreglo)):
        raise ValueError(f"{nombre} debe contener valores finitos.")

    if np.any(arreglo < 0):
        raise ValueError(f"{nombre} no puede ser negativo.")

    return arreglo


def solucion_plana(tau):
    """
    Solución exacta para curvatura nula: k = 0.

    x(tau) = [(9/2) tau^2]^(1/3)
    """
    tau = validar_parametro(tau, "tau")

    return np.cbrt(4.5 * tau**2)


def solucion_cerrada(eta):
    """
    Solución paramétrica para curvatura positiva: k = +1.

    0 <= eta <= 2*pi.

    Retorna:
        tau: tiempo cosmológico adimensional
        x: factor de escala adimensional
    """
    eta = validar_parametro(eta, "eta")

    if np.any(eta > 2 * np.pi):
        raise ValueError("Para el modelo cerrado, eta <= 2*pi.")

    tau = eta - np.sin(eta)
    x = 1.0 - np.cos(eta)

    return tau, x


def solucion_abierta(eta):
    """
    Solución paramétrica para curvatura negativa: k = -1.

    Retorna:
        tau: tiempo cosmológico adimensional
        x: factor de escala adimensional
    """
    eta = validar_parametro(eta, "eta")

    tau = np.sinh(eta) - eta
    x = np.cosh(eta) - 1.0

    return tau, x


if __name__ == "__main__":
    print("Comprobación de soluciones analíticas")

    print("Modelo plano:")
    print("x(1) =", solucion_plana(1.0))

    print("\nModelo cerrado (eta = pi):")
    tau, x = solucion_cerrada(np.pi)
    print("tau =", tau, "x =", x)

    print("\nModelo abierto (eta = 1):")
    tau, x = solucion_abierta(1.0)
    print("tau =", tau, "x =", x)
