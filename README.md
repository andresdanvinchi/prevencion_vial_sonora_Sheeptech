# Prevencion vial en Sonora con ATUS

Proyecto de mineria de datos para analizar accidentes de transito en Sonora usando la base ATUS del INEGI. El objetivo es identificar patrones regionales, niveles de gravedad y posibles acciones de prevencion vial.

## Fuente de datos

Fuente principal:

- Instituto Nacional de Estadistica y Geografia. Accidentes de Transito Terrestre en Zonas Urbanas y Suburbanas (ATUS), 1997-2024.
- Sitio: https://www.inegi.org.mx/programas/accidentes/

En este repositorio se usan los CSV anuales de 2015 a 2024 y el catalogo municipal:

- `datos/originales/conjunto_de_datos/atus_anual_2015.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2016.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2017.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2018.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2019.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2020.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2021.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2022.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2023.csv`
- `datos/originales/conjunto_de_datos/atus_anual_2024.csv`
- `datos/originales/catalogos/tc_municipio.csv`

## Orden recomendado de ejecucion

1. `notebooks/atus_sonora_10_anios_prevencion.ipynb`
   - Carga datos 2015-2024.
   - Filtra Sonora.
   - Realiza limpieza, variables derivadas, EDA, reglas de asociacion, modelos y analisis temporal.

2. `E3_Modelos_Evaluacion/E3_Modelos_Evaluacion_ATUS_Sonora.ipynb`
   - Implementa y evalua los modelos del entregable E3.
   - Incluye Arbol de Decision base, Regresion Logistica, Random Forest ajustado, clustering jerarquico y reglas de asociacion.

3. `E2_Analisis_Exploratorio_Preprocesamiento/notebook_e2.md`
   - Documento de apoyo con el resumen del analisis exploratorio y preprocesamiento.

4. `E4_Informe_Final_Codigo_Completo/Informe_Final_Prevencion_Vial_Sonora.docx`
   - Informe final escrito del proyecto.

## Librerias necesarias

Los notebooks estan pensados para ejecutarse en Google Colab. Las librerias principales son:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn mlxtend statsmodels
```

En Colab normalmente ya vienen instaladas varias de estas librerias. Los notebooks incluyen celdas para instalar paquetes faltantes cuando sea necesario.

## Como ejecutar en Google Colab

1. Abrir Google Colab.
2. Subir o abrir el notebook desde GitHub.
3. Ejecutar las celdas en orden, de arriba hacia abajo.
4. Si el entorno tiene internet, los notebooks pueden leer los CSV desde GitHub.
5. Si el entorno no tiene internet, subir la carpeta del proyecto a Colab o montar Google Drive y usar `DATA_SOURCE = "local"`.

## Estructura del repositorio

```text
datos/
  originales/
    catalogos/
    conjunto_de_datos/
E1_Propuesta/
E2_Analisis_Exploratorio_Preprocesamiento/
E3_Modelos_Evaluacion/
E4_Informe_Final_Codigo_Completo/
notebooks/
README.md
```

## Variables principales creadas

- `REGION`: segmentacion regional de municipios de Sonora.
- `TOTAL_HERIDOS`: suma de personas heridas registradas.
- `TOTAL_MUERTOS`: suma de personas fallecidas registradas.
- `TOTAL_VICTIMAS`: suma de heridos y fallecidos.
- `GRAVE_BIN`: 1 si el accidente tuvo victimas, 0 si no tuvo victimas.
- `NIVEL_GRAVEDAD`: clasificacion descriptiva entre fatal, con heridos o solo danos.
- `INVOLUCRA_MOTO`: indica si participo motocicleta.
- `INVOLUCRA_BICI`: indica si participo bicicleta.
- `RANGO_HORA`: agrupa hora en madrugada, manana, tarde y noche.

## Reproducibilidad

Para reproducir el proyecto completo:

1. Confirmar que los archivos CSV esten en `datos/originales/conjunto_de_datos/`.
2. Confirmar que `tc_municipio.csv` este en `datos/originales/catalogos/`.
3. Ejecutar primero el notebook principal de `notebooks/`.
4. Ejecutar despues el notebook de E3.
5. Revisar los documentos de E2 y E4 para la interpretacion de resultados.

## Entregables

- E1: propuesta del proyecto.
- E2: analisis exploratorio y preprocesamiento.
- E3: implementacion y evaluacion de modelos.
- E4: informe final y codigo completo reproducible.
