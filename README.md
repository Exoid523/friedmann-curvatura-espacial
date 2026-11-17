
# Soluciones analíticas y numéricas de las ecuaciones de Friedmann

**Curso:** Relatividad General  
**Institución:** Escuela de Ciencias Físicas y Matemáticas, USAC  
**Docente:** Dr. Juan Ponciano  
**Semestre:** Segundo semestre de 2026

## 1. Descripción del proyecto

Este proyecto estudia las soluciones de las ecuaciones de Friedmann para tres modelos cosmológicos de Friedmann-Lemaître-Robertson-Walker (FLRW):

- Universo cerrado: k = +1.
- Universo plano: k = 0.
- Universo abierto: k = -1.

El trabajo combina soluciones analíticas, integración numérica de ecuaciones diferenciales ordinarias y comparación cuantitativa de resultados.

El propósito es analizar cómo influye la curvatura espacial en la evolución del factor de escala y comprobar la consistencia de las soluciones numéricas mediante expresiones exactas.

## 2. Modelo físico

Se considera un universo homogéneo e isótropo con las siguientes condiciones:

- Materia sin presión: p = 0.
- Constante cosmológica nula: Lambda = 0.
- Densidad de materia positiva.
- Curvatura espacial normalizada: k = -1, 0, +1.

La primera ecuación de Friedmann es

    H² = (8πG/3)ρ - kc²/a²

y la conservación de la materia implica

    ρa³ = constante.

Definiendo

    C = (8πG/3)ρ₀a₀³,

se obtiene

    (da/dt)² = C/a - kc².

Se introducen las escalas características

    a* = C/(2c²)
    t* = C/(2c³)

y las variables adimensionales

    x = a/a*
    τ = t/t*.

La ecuación fundamental se transforma en

    (dx/dτ)² = 2/x - k.

## 3. Soluciones analíticas

### Universo plano (k = 0)

    x(τ) = [(9/2)τ²]^(1/3)

El factor de escala aumenta indefinidamente y su evolución corresponde a una ley de potencia.

### Universo cerrado (k = +1)

    x(η) = 1 - cos(η)
    τ(η) = η - sin(η)

La expansión máxima ocurre en

    η = π
    x_max = 2
    τ_max = π.

Posteriormente, el modelo presenta una fase de contracción.

### Universo abierto (k = -1)

    x(η) = cosh(η) - 1
    τ(η) = sinh(η) - η

El factor de escala aumenta indefinidamente y se aproxima a un crecimiento lineal para tiempos grandes.

## 4. Método computacional

Se resolvió numéricamente el sistema de primer orden

    dx/dτ = v
    dv/dτ = -1/x².

Las condiciones iniciales utilizadas fueron

    x₀ = 0.5
    v₀ = sqrt(2/x₀ - k).

La integración se realizó utilizando la función `solve_ivp` de SciPy, con el método explícito DOP853.

Parámetros de integración:

- Método: DOP853.
- Tolerancia relativa: 1e-10.
- Tolerancia absoluta: 1e-12.
- Paso máximo: 0.02.
- Intervalo previsto: desde τ = 0 hasta τ = 6.5, medido a partir de la condición inicial.

Para evitar la singularidad en x = 0, se incorporó un evento de terminación durante la contracción, cuando x desciende hasta 0.05.

El tiempo de la integración numérica se mide desde x₀ = 0.5. Para comparar con las soluciones analíticas se corrige el desplazamiento correspondiente del origen temporal.

## 5. Verificación numérica

Se utilizaron dos procedimientos de comprobación.

### Comparación con las soluciones analíticas

Se calculó el error absoluto máximo:

    E_max = max |x_num(τᵢ) - x_anal(τᵢ)|.

Resultados obtenidos:

| Modelo | Error absoluto máximo |
|---|---:|
| Cerrado (k = +1) | 1.370463e-09 |
| Plano (k = 0) | 4.093614e-12 |
| Abierto (k = -1) | 4.610599e-10 |

Para los modelos cerrado y abierto, la comparación incluye una interpolación lineal de las soluciones paramétricas.

### Restricción de Friedmann

Se evaluó el residuo

    ε(τ) = v² - 2/x + k.

Los máximos valores absolutos obtenidos fueron:

| Modelo | Residuo máximo |
|---|---:|
| Cerrado (k = +1) | 2.106e-09 |
| Plano (k = 0) | 1.198e-12 |
| Abierto (k = -1) | 2.211e-12 |

Los residuos pequeños y la concordancia con las soluciones exactas respaldan la consistencia de los resultados numéricos para los parámetros utilizados.

Estos resultados no sustituyen un estudio de convergencia ni representan una estimación aislada del error del integrador.

## 6. Estructura del proyecto

    Proyecto_Friedmann/
    |
    |-- src/
    |   |-- __init__.py
    |   |-- soluciones_analiticas.py
    |   |-- soluciones_numericas.py
    |
    |-- figuras/
    |   |-- friedmann_analiticas.png
    |   |-- friedmann_analiticas.pdf
    |   |-- friedmann_comparacion.png
    |   |-- friedmann_comparacion.pdf
    |
    |-- resultados/
    |   |-- errores_friedmann.csv
    |
    |-- main.py
    |-- requirements.txt
    |-- README.md

## 7. Bibliotecas utilizadas

- Python 3.
- NumPy: evaluación de funciones y arreglos numéricos.
- SciPy: integración numérica mediante solve_ivp.
- Matplotlib: visualización de resultados.

La implementación se desarrolló y ejecutó utilizando Visual Studio Code y Ubuntu mediante WSL.

## 8. Ejecución

Desde la carpeta principal del proyecto, con un entorno virtual de Linux activado que contenga las dependencias, ejecutar:

    python main.py

El programa genera las gráficas comparativas y exporta los errores al archivo:

    resultados/errores_friedmann.csv

Las figuras se almacenan en el directorio `figuras/`.

## 9. Interpretación y limitaciones

Los tres modelos presentan una evolución inicial semejante. Sus diferencias aumentan conforme la curvatura espacial adquiere mayor importancia relativa.

En el modelo cerrado se observa expansión seguida de recolapso; los modelos plano y abierto continúan expandiéndose.

Estas conclusiones corresponden específicamente a universos dominados por materia sin presión y con constante cosmológica nula. No describen necesariamente el destino de modelos cosmológicos con radiación o energía oscura.

El modelo constituye un estudio idealizado de soluciones exactas de Friedmann y no realiza ajustes a observaciones cosmológicas.

## 10. Referencias de estudio

- Bert Janssen. Teoría de la Relatividad General (2013).
- Sean Carroll. Spacetime and Geometry (2004).
- Steven Weinberg. Gravitation and Cosmology (1972).

Las referencias se utilizan como marco teórico para la formulación cosmológica. Las derivaciones, implementaciones y comprobaciones realizadas en este proyecto se documentarán en el informe académico.
