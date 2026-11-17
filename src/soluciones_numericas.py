
"""
Integración numérica de las ecuaciones de Friedmann.

Modelo cosmológico:
    Materia sin presión: p = 0
    Constante cosmológica: Lambda = 0

Sistema adimensional:
    dx/dtau = v
    dv/dtau = -1/x**2

Restricción de Friedmann:
    v**2 = 2/x - k
"""

import numpy as np
from scipy.integrate import solve_ivp


def ecuaciones_friedmann(tau, estado):
    """Sistema de ecuaciones diferenciales de Friedmann."""
    x, v = estado

    return [v, -1.0 / x**2]


def integrar_modelo(k, x_inicial=0.5, tau_final=6.5):
    """
    Integra numéricamente un modelo cosmológico.

    Parámetros
    ----------
    k : int
        Curvatura espacial: -1, 0 o +1.
    x_inicial : float
        Factor de escala inicial, estrictamente positivo.
    tau_final : float
        Tiempo adimensional final.

    Retorna
    -------
    solucion : OdeResult
        Resultado de scipy.integrate.solve_ivp.
    """

    if k not in (-1, 0, 1):
        raise ValueError("La curvatura k debe ser -1, 0 o +1.")

    if not np.isfinite(x_inicial) or x_inicial <= 0.05:
        raise ValueError("x_inicial debe ser mayor que 0.05.")

    if not np.isfinite(tau_final) or tau_final <= 0:
        raise ValueError("tau_final debe ser positivo.")

    argumento = 2.0 / x_inicial - k

    if argumento < 0:
        raise ValueError("Condición inicial incompatible con Friedmann.")

    # Condición inicial de expansión
    v_inicial = np.sqrt(argumento)

    # Detener la integración antes de llegar a x = 0
    def evento_colapso(tau, estado):
        return estado[0] - 0.05

    evento_colapso.terminal = True
    evento_colapso.direction = -1

    solucion = solve_ivp(
        fun=ecuaciones_friedmann,
        t_span=(0.0, tau_final),
        y0=[x_inicial, v_inicial],
        method="DOP853",
        rtol=1e-10,
        atol=1e-12,
        max_step=0.02,
        events=evento_colapso,
    )

    if not solucion.success:
        raise RuntimeError(solucion.message)

    return solucion


def error_restriccion(solucion, k):
    """
    Evalúa el residuo de la restricción de Friedmann.

    Debe permanecer aproximadamente igual a cero.
    """
    x, v = solucion.y

    residuo = v**2 - 2.0 / x + k

    return np.max(np.abs(residuo))


if __name__ == "__main__":

    for k in (1, 0, -1):

        solucion = integrar_modelo(k)

        error = error_restriccion(solucion, k)

        print(f"\nModelo con k = {k:+d}")
        print(f"Tiempo final: {solucion.t[-1]:.6f}")
        print(f"Factor de escala final: {solucion.y[0, -1]:.6f}")
        print(f"Error máximo de la restricción: {error:.3e}")
