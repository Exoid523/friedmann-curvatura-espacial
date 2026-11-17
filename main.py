
"""
Comparación de soluciones analíticas de Friedmann.

Modelos:
    k = +1: universo cerrado
    k =  0: universo plano
    k = -1: universo abierto
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from src.soluciones_analiticas import (
    solucion_plana,
    solucion_cerrada,
    solucion_abierta,
)


def main():
    # Tiempo adimensional para el universo plano
    tau = np.linspace(0, 2 * np.pi, 1500)
    x_plano = solucion_plana(tau)

    # Universo cerrado: expansión y recolapso
    eta_c = np.linspace(0, 2 * np.pi, 1500)
    tau_c, x_c = solucion_cerrada(eta_c)

    # Universo abierto: expansión indefinida
    eta_a = np.linspace(0, 3.1, 1500)
    tau_a, x_a = solucion_abierta(eta_a)

    # Gráfica comparativa
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(tau_c, x_c, label="Cerrado (k = +1)")
    ax.plot(tau, x_plano, label="Plano (k = 0)")
    ax.plot(tau_a, x_a, label="Abierto (k = -1)")

    ax.set(
        xlabel="Tiempo adimensional τ",
        ylabel="Factor de escala x",
        title="Soluciones analíticas de Friedmann",
        xlim=(0, 2 * np.pi),
    )

    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()

    # Guardar figuras para el informe y Beamer
    carpeta = Path("figuras")
    carpeta.mkdir(exist_ok=True)

    fig.savefig(carpeta / "friedmann_analiticas.png", dpi=300)
    fig.savefig(carpeta / "friedmann_analiticas.pdf")

    plt.close(fig)

    # Comparacion entre soluciones analiticas y numericas
    from src.soluciones_numericas import integrar_modelo

    x0 = 0.5
    modelos = [
        (1, "Cerrado"),
        (0, "Plano"),
        (-1, "Abierto"),
    ]

    fig_comp, axes = plt.subplots(
        1, 3, figsize=(14, 4.5)
    )
    tabla_errores = []

    print("\nCOMPARACION ANALITICA Y NUMERICA")

    for ax, (k, nombre) in zip(axes, modelos):

        solucion = integrar_modelo(
            k=k,
            x_inicial=x0,
            tau_final=6.5,
        )

        tiempo_numerico = solucion.t
        x_numerico = solucion.y[0]

        # Corregir el origen temporal de la solucion exacta
        if k == 0:
            tau0 = np.sqrt(2.0 * x0**3 / 9.0)
            x_analitico = solucion_plana(
                tiempo_numerico + tau0
            )

        elif k == 1:
            eta0 = np.arccos(1.0 - x0)
            tau0 = eta0 - np.sin(eta0)

            eta = np.linspace(eta0, 2*np.pi, 50000)
            tau_ref, x_ref = solucion_cerrada(eta)

            x_analitico = np.interp(
                tiempo_numerico + tau0,
                tau_ref,
                x_ref,
            )

        else:
            eta0 = np.arccosh(1.0 + x0)
            tau0 = np.sinh(eta0) - eta0

            eta = np.linspace(eta0, 4.0, 50000)
            tau_ref, x_ref = solucion_abierta(eta)

            x_analitico = np.interp(
                tiempo_numerico + tau0,
                tau_ref,
                x_ref,
            )

        # Calcular el error absoluto maximo
        error = np.max(
            np.abs(x_numerico - x_analitico)
        )

        print(f"{nombre} (k={k:+d})")
        print(f"  Error maximo: {error:.6e}")

        x_num, v_num = solucion.y

        residuo = np.max(
            np.abs(v_num**2 - 2.0 / x_num + k)
        )

        tabla_errores.append([k, error, residuo])
        # Representacion grafica
        ax.plot(
            tiempo_numerico,
            x_analitico,
            label="Analitica",
            linewidth=2,
        )

        ax.plot(
            tiempo_numerico[::12],
            x_numerico[::12],
            ".",
            label="Numerica",
            markersize=4,
        )

        ax.set_title(f"{nombre} (k={k:+d})")
        ax.set_xlabel("Tiempo desde x0 = 0.5")
        ax.set_ylabel("Factor de escala x")
        ax.grid(True, alpha=0.3)
        ax.legend()

    fig_comp.suptitle(
        "Friedmann: soluciones analiticas y numericas"
    )

    fig_comp.tight_layout()

    fig_comp.savefig(
        carpeta / "friedmann_comparacion.png",
        dpi=300,
    )

    fig_comp.savefig(
        carpeta / "friedmann_comparacion.pdf"
    )

    plt.close(fig_comp)

    # Exportar resultados numericos a CSV
    carpeta_resultados = Path("resultados")
    carpeta_resultados.mkdir(exist_ok=True)

    archivo_csv = carpeta_resultados / "errores_friedmann.csv"

    np.savetxt(
        archivo_csv,
        np.asarray(tabla_errores),
        delimiter=",",
        header="k,error_absoluto_maximo,residuo_friedmann_maximo",
        comments="",
        fmt=["%.0f", "%.12e", "%.12e"],
    )

    print(f"Tabla de errores guardada en: {archivo_csv}")
    print("Gráficas generadas correctamente.")


if __name__ == "__main__":
    main()
