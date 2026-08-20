# 🚀 Predicción del Aterrizaje de la Primera Etapa del Falcon 9

Proyecto de Ciencia de Datos orientado al análisis y predicción de los aterrizajes de la primera etapa del cohete Falcon 9 de SpaceX utilizando técnicas de análisis estadístico, visualización de datos y Machine Learning.

## Objetivos

- Analizar los factores que influyen en el éxito de los aterrizajes.
- Explorar datos históricos de lanzamientos Falcon 9.
- Identificar patrones mediante SQL y visualizaciones.
- Construir modelos predictivos capaces de anticipar el resultado de una recuperación.

## Tecnologías

- Python
- Pandas y NumPy
- Matplotlib y Seaborn
- SQLite
- Folium
- Plotly Dash
- Scikit-Learn
- Quarto

## Metodología

1. **Data Collection**: obtención de datos desde la API de SpaceX y Wikipedia.
2. **Data Wrangling**: limpieza, transformación y preparación de datos.
3. **EDA**: análisis exploratorio mediante gráficos y estadísticas.
4. **SQL Analysis**: consultas analíticas sobre una base de datos SQLite.
5. **Geospatial Analysis**: análisis geográfico de las bases de lanzamiento con Folium.
6. **Dashboard**: desarrollo de una aplicación interactiva con Plotly Dash.
7. **Machine Learning**: entrenamiento y evaluación de modelos de clasificación.

## Modelos Evaluados

- Logistic Regression
- Support Vector Machine (SVM)
- Decision Tree
- K-Nearest Neighbors (KNN)

## Resultados Principales

- La experiencia acumulada de SpaceX es uno de los factores más relevantes.
- La masa de la carga útil influye en la probabilidad de recuperación.
- El tipo de órbita afecta la complejidad del aterrizaje.
- KSC LC-39A presenta los mejores resultados operativos.
- Los modelos lograron una precisión aproximada del **83.3%**.

## Estructura del Proyecto

```text
data/
notebooks/
dashboard/
reports/
images/
README.md
```

## Ejecución

```bash
pip install -r requirements.txt
jupyter notebook
```

Para ejecutar el dashboard:

```bash
python spacex_dashboard.py
```

## Autor

**José M. Martínez Ruiz**

Proyecto desarrollado como parte del programa **IBM Data Science Professional Certificate**.