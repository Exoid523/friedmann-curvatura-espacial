# Informe de Friedmann — fuente LaTeX

Documento adaptado de la plantilla académica USAC/ECFM facilitada para el curso de Relatividad General.

## Compilación con Overleaf

Subir `main.tex`, `referencias.bib`, `logo_usac.png`, `logo_ecfm.png` y la carpeta `figuras/` con sus cuatro archivos al proyecto de Overleaf. Seleccionar pdfLaTeX y Biber para la bibliografía.

## Compilación local

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## Datos y figuras

Las tablas del informe muestran los resultados de las ejecuciones del proyecto descritas durante el trabajo con VS Code. El script `reproducir_resultados.py` reproduce las dos figuras a partir de las ecuaciones, parámetros y método numérico declarados y verifica nuevamente los órdenes de magnitud del error y del residuo. La ligera variación en las últimas cifras depende de la versión de SciPy y de la evaluación interpolada.

La reproducción no constituye un análisis de convergencia.
