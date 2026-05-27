# Informe final - Prevención vial en Sonora con ATUS

## Portada e identificación del equipo

Proyecto: Prevención vial en Sonora mediante análisis de accidentes de transito.

Materia: Minería de Datos.

Institución: TecNM / Instituto Tecnologico de Hermosillo.

Equipo:

- Felix Gautrin Diane.
- Landavazo Vasquez Andres Leonardo.
- Fuentes Babuca Felipe de Jesus.

Fuente principal de datos: Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas (ATUS), INEGI.

Periodo analizado: 2015-2024.

## Resumen ejecutivo

Este proyecto estudia los accidentes de tránsito registrados en Sonora durante los últimos diez años disponibles en la base ATUS. El propósito principal fue identificar patrones regionales de frecuencia, gravedad y causas probables para proponer acciones preventivas más enfocadas. El enfoque no fue buscar culpables individuales, sino entender el comportamiento general de los datos y traducirlo en información util para la seguridad vial.

El análisis partio de registros anuales de accidentes en zonas urbanas y suburbanas. Despues de filtrar Sonora y eliminar registros marcados como `Certificado cero`, se trabajo con 183,911 accidentes reales. Se construyeron variables derivadas como región, total de heridos, total de fallecidos, total de víctimas, participacion de motocicleta o bicicleta, rango de hora y una variable binaria de gravedad.

La exploracion mostro que Hermosillo concentra el mayor número de accidentes, seguido por Sur y Valle y Frontera. Sin embargo, las regiones con mayor porcentaje de accidentes graves fueron Sierra, Centro y Sur y Valle. Esta diferencia fue una de las partes más importantes del proyecto, porque demuestra que el volumen de accidentes y la gravedad no siempre apuntan a los mismos lugares.

En modelado se implementaron varios enfoques. Primero, un árbol de Decision como linea base. Despues, una Regresion Logística como modelo interpretable y un Random Forest ajustado como modelo más elaborado. También se uso clustering jerárquico para agrupar municipios con comportamientos parecidos y reglas de asociación para encontrar combinaciones frecuentes relacionadas con accidentes graves.

La recomendación principal fue usar el Random Forest ajustado como modelo de clasificación cuando se busca el mejor equilibrio entre precision y recall para accidentes graves. Este informe queda alineado con el cuaderno principal `notebooks/atus_sonora_10_anios_prevencion.ipynb` y con el entregable E3 actualizado. La Regresion Logística se conserva como alternativa cuando se necesita una explicacion más sencilla. El clustering y las reglas de asociación complementan el análisis porque ayudan a traducir los resultados en acciones preventivas por región o tipo de municipio.

## 1. Introduccion y contexto del problema

Los accidentes de tránsito son una problematica social porque afectan directamente la seguridad de conductores, pasajeros, peatones, ciclistas, motociclistas y familias. Ademas de los daños materiales, los accidentes pueden provocar lesiones, muertes, costos economicos, interrupciones en la movilidad y presion sobre servicios de emergencia.

En Sonora, el comportamiento de los accidentes no es igual en todos los municipios. La capital, las ciudades fronterizas, las zonas costeras, los municipios del sur y las localidades serranas tienen condiciones de movilidad diferentes. Por eso, analizar solamente el total estatal puede ocultar patrones importantes.

El proyecto se planteo desde un enfoque preventivo e interpretativo. La pregunta principal fue: que patrones presentan los accidentes de tránsito en las diferentes regiones de Sonora y cuales son las causas más frecuentes que pueden ayudar a proponer estrategias de prevención vial.

Para responder esta pregunta, se trabajo con datos reales y públicos del INEGI. El uso de una fuente oficial permite que el análisis sea reproducible y que las conclusiones se basen en evidencia. La idea fue avanzar desde la comprension del problema hasta el modelado, sin perder de vista que el resultado final debe servir para interpretar y prevenir.

## 2. Descripción del dataset

La base utilizada fue Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas (ATUS), publicada por el Instituto Nacional de Estadistica y Geografia. Se trabajaron los archivos anuales de 2015 a 2024, lo que permite observar una década completa de comportamiento.

Los datos originales incluyen accidentes de todo Mexico. Para este proyecto se filtro solamente el estado de Sonora, identificado con la clave de entidad 26. También se uso el catalogo municipal para agregar el nombre del municipio a partir de la clave de entidad y municipio.

| Elemento | Resultado |
|---|---:|
| Periodo cubierto | 2015-2024 |
| Registros de Sonora antes de depurar | 187,104 |
| Registros `Certificado cero` eliminados | 3,193 |
| Accidentes reales analizados | 183,911 |
| Municipios presentes | 70 |
| Porcentaje de accidentes graves | 16.99% |

Las variables disponibles incluyen información geografica, temporal, categorica y numerica. Entre las variables más importantes estan municipio, año, mes, dia de semana, hora, tipo de accidente, causa probable, tipo de vehículos involucrados, personas heridas y personas fallecidas.

Para facilitar el análisis se crearon variables derivadas. La variable `REGION` permite comparar zonas de Sonora. `TOTAL_HERIDOS`, `TOTAL_MUERTOS` y `TOTAL_VICTIMAS` resumen el impacto humano del accidente. `GRAVE_BIN` clasifica si el accidente tuvo victimas. `RANGO_HORA` agrupa la hora del accidente en madrugada, manana, tarde y noche. `INVOLUCRA_MOTO` e `INVOLUCRA_BICI` indican si participaron motocicletas o bicicletas.

## 3. Preparación y calidad de datos

La preparación inicio con la lectura de los CSV anuales. Para que el proyecto fuera reproducible, los notebooks se configuraron para cargar los archivos desde GitHub o desde una copia local. Despues se filtro Sonora y se eliminaron registros de `Certificado cero`, porque esos registros indican ausencia de accidente y no representan eventos viales ocurridos.

También se convirtieron variables numericas que venian como texto. Esto fue necesario para sumar heridos, fallecidos y vehículos involucrados. Las claves de entidad y municipio se normalizaron con ceros a la izquierda para unir correctamente con el catalogo municipal.

En calidad de datos se detectaron valores faltantes principalmente en la edad del conductor. Esta variable se conservo, pero en los modelos se trato con imputacion de mediana. En variables categoricas se uso imputacion por moda. Está decision permite no perder registros y mantiene el dataset completo para el modelado.

Se identificaron 274 duplicados exactos. Debido al tamaño del dataset, su presencia no cambia de forma importante el análisis exploratorio, pero se documentaron como parte de la calidad de datos. Para modelado final, se recomienda eliminarlos si el objetivo es entrenar modelos de produccion.

Los outliers se conservaron. En este problema, los valores extremos no son ruido automaticamente: un accidente con muchos heridos, fallecidos o vehículos involucrados puede ser justamente el caso que más interesa prevenir. Eliminar esos registros hubiera reducido la capacidad del análisis para estudiar la gravedad.

## 4. Análisis exploratorio

El análisis exploratorio permitio conocer el comportamiento general antes de aplicar modelos. El primer hallazgo fue temporal: los accidentes aumentaron de manera gradual hasta 2019, bajaron en 2020 y subieron con fuerza despues de ese año. El valor más alto se observo en 2023, con 26,557 accidentes.

Por región, Hermosillo concentro 65,252 accidentes, seguido por Sur y Valle con 54,154 y Frontera con 44,264. Este resultado era esperado porque son zonas con mayor movilidad urbana, actividad económica o flujo vehicular. Sin embargo, la gravedad conto una historia diferente.

Cuando se reviso el porcentaje de accidentes graves, la Sierra tuvo 24.25%, Centro 22.38% y Sur y Valle 21.12%. Hermosillo, aunque tiene el mayor volumen de accidentes, tuvo 13.39% de accidentes graves. Esto muestra que la prevención debe mirar tanto cantidad como severidad.

El tipo de accidente más frecuente fue la colision con vehículo automotor, con 125,202 casos. En segundo lugar aparecio la colision con motocicleta, con 18,531 casos, y despues la colision con objeto fijo, con 17,205 casos. Estos resultados sugieren que una parte importante de la prevención debe enfocarse en interacciones entre vehículos, control de velocidad, distancia segura y puntos de conflicto urbano.

La causa probable más registrada fue `Conductor`, con 178,145 accidentes. Aunque está categoria es amplia, indica que las estrategias preventivas deben considerar conducta vial, atencion al volante, respeto a señalamientos, velocidad y educacion vial.

El análisis por hora y dia mostro una concentracion relevante los viernes por la tarde, con 10,802 accidentes. Este patron puede relacionarse con salida laboral, movilidad comercial y traslados de fin de semana. A nivel preventivo, este resultado sugiere reforzar vigilancia, campanas y control operativo en horarios especificos.

## 5. Metodología de modelado

La etapa de modelado se diseno para cubrir tres necesidades: tener una linea base simple, construir un modelo más fuerte de clasificación y agregar un metodo diferente para entender la estructura del dataset.

La variable objetivo fue `GRAVE_BIN`. Esta variable vale 1 si el accidente tuvo personas heridas o fallecidas, y 0 si no tuvo victimas. Se eligio esta definición porque el enfoque del proyecto es preventivo: interesa distinguir los accidentes que generan mayor impacto humano.

Para evitar fuga de información, no se usaron como predictores las columnas `TOTAL_HERIDOS`, `TOTAL_MUERTOS`, `TOTAL_VICTIMAS` ni `CLASACC`, porque estan directamente relacionadas con la definicion de gravedad. Si se usaran, el modelo recibiria parte de la respuesta de forma indirecta.

Las variables predictoras incluyeron región, municipio, mes, dia de semana, rango de hora, tipo de accidente, causa probable, tipo de camino o superficie, sexo, aliento, cinturon, edad del conductor, total de vehículos, participacion de motocicleta y participacion de bicicleta.

Para el preprocesamiento se uso imputacion de faltantes, codificacion One-Hot para variables categoricas y normalizacion para variables numericas. Despues se dividieron los datos en entrenamiento y prueba con estratificacion, para mantener una proporcion parecida de accidentes graves y no graves.

## 6. Modelos implementados

| Modelo | Tipo | Funcion dentro del proyecto |
|---|---|---|
| KNN linea base | Clasificación supervisada basada en vecinos | Cumple el metodo de K-Nearest Neighbors del curso y sirve como referencia simple |
| árbol de Decision interpretable | Clasificación supervisada | Sirve para extraer una regla IF-THEN y explicar una decision del modelo |
| Regresion Logística | Clasificación supervisada interpretable | Permite comparar con un modelo claro y facil de explicar |
| Random Forest ajustado | Clasificación supervisada elaborada | Busca mejor rendimiento con ajuste de hiperparametros |
| Clustering jerárquico | Aprendizaje no supervisado | Agrupa municipios con patrones parecidos |
| Reglas de asociación | Metodo descriptivo | Encuentra combinaciones frecuentes relacionadas con gravedad |

KNN se agrego como linea base del curso. Este metodo clasifica un accidente segun los casos mas cercanos despues del preprocesamiento. Debido al tamaño del dataset y a la cantidad de variables categoricas codificadas, se uso como referencia tecnica y no como candidato principal de recomendacion.

El árbol de Decision se uso como modelo interpretable. A diferencia del Random Forest, permite leer rutas de decision concretas. Por eso se extrajo una regla IF-THEN para explicar de forma sencilla que combinaciones de condiciones llevan al modelo hacia una clasificacion de gravedad.

La Regresion Logística se incluyo porque es interpretable. Aunque no siempre logra el mejor rendimiento, permite entender de forma más clara como cambian las probabilidades segun las variables. También se uso con pesos balanceados para dar mayor atencion a la clase grave.

El Random Forest ajustado fue el modelo más elaborado. Combina muchos arboles y reduce la dependencia de una sola estructura. Se ajustaron hiperparametros como número de arboles, profundidad, minimo de muestras por hoja, seleccion de variables y pesos de clase.

El clustering jerárquico se aplico a nivel municipal. En lugar de clasificar accidentes individuales, agrupa municipios segun indicadores como total de accidentes, porcentaje de gravedad, promedio de heridos, promedio de fallecidos, presencia de motocicletas, bicicletas y tipos de accidente.

Las reglas de asociación se usaron como complemento interpretativo. Este metodo ayuda a encontrar combinaciones frecuentes de condiciones que terminan en gravedad alta, por ejemplo cierto tipo de accidente o combinaciones de región, causa y horario.

## 7. Evaluación de modelos

La evaluación de clasificación no se baso solamente en accuracy. En este problema, un modelo podría tener buen accuracy si clasifica bien los accidentes no graves, porque son la mayoria. Sin embargo, para seguridad vial importa especialmente la clase grave.

Por eso se revisaron precision, recall, F1-score, matriz de confusion, curva ROC y ROC-AUC. La precision indica que tan confiables son las predicciones positivas de gravedad. El recall indica cuantos accidentes graves reales logra detectar el modelo. El F1-score resume el equilibrio entre precision y recall.

En la ejecucion documentada, el Random Forest ajustado obtuvo el mejor equilibrio para la clase grave. La Regresion Logística tuvo alto recall, por lo que puede ser util si la prioridad principal es detectar la mayor cantidad posible de accidentes graves, aunque produzca más falsos positivos. KNN y el árbol interpretable se conservaron como referencias del curso y como apoyo explicativo.

| Modelo | Accuracy | Precision grave | Recall grave | F1 grave | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| KNN linea base | Ver notebook | Ver notebook | Ver notebook | Ver notebook | Ver notebook |
| árbol IF-THEN | Ver notebook | Ver notebook | Ver notebook | Ver notebook | Ver notebook |
| Regresion Logística | 0.8229 | 0.4861 | 0.7387 | 0.5863 | 0.8806 |
| Random Forest ajustado | 0.8600 | 0.5719 | 0.7007 | 0.6298 | 0.8911 |

Los valores exactos de KNN y del árbol IF-THEN quedan en el notebook principal ATUS porque se calculan al ejecutar las celdas con las muestras estratificadas definidas para mantener el proceso reproducible. La interpretación se mantiene: no basta con ver accuracy, porque la clase grave es menos frecuente y es la más importante para prevencion.

Como parte del requisito de árboles de Decision, el notebook extrae una regla IF-THEN mediante `export_text`. La lectura esperada de esa salida es:

```text
IF se cumplen las condiciones de la ruta del arbol
THEN el accidente se clasifica hacia No grave o Grave segun la hoja final.
```

Esta regla ayuda a comunicar el razonamiento de un modelo simple, aunque el modelo recomendado para desempeño general siga siendo Random Forest.

## 8. Comparativa y recomendación

Con base en las metricas, el modelo recomendado para el proyecto es el Random Forest ajustado. La razon principal es que ofrece el mejor equilibrio general para la clase grave, especialmente en F1-score. Esto significa que logra una relacion más balanceada entre detectar accidentes graves y no marcar demasiados accidentes como graves cuando no lo son.

La Regresion Logística no se descarta. Su recall fue alto, lo que significa que detecta una mayor proporcion de accidentes graves. En un contexto preventivo donde se prefiere activar alertas aunque existan falsos positivos, podría ser una opcion util. Ademas, es más facil de explicar que Random Forest.

KNN y el árbol IF-THEN cumplen funciones de referencia. KNN permite cubrir un metodo basado en cercania entre observaciones, mientras que el árbol permite explicar decisiones con reglas. Ninguno de los dos desplaza la recomendacion principal porque el objetivo final requiere balance entre deteccion de gravedad y estabilidad del modelo.

El clustering jerárquico no compite directamente con los clasificadores porque responde otra pregunta. Mientras los clasificadores predicen gravedad a nivel de accidente, el clustering agrupa municipios. Esto permite pensar en estrategias diferenciadas: municipios con alto volumen, municipios con alta gravedad proporcional y municipios con participacion relevante de motocicletas o tipos especificos de accidente.

## 9. Resultados preventivos principales

El primer resultado preventivo es que Hermosillo, Sur y Valle y Frontera concentran el mayor volumen de accidentes. Estas regiones requieren acciones de escala amplia: educacion vial, control de velocidad, vigilancia en cruces y seguimiento de zonas con alta movilidad.

El segundo resultado es que la Sierra, Centro y Sur y Valle tienen porcentajes de gravedad más altos. Estas zonas requieren atencion aunque no siempre aparezcan como las de mayor cantidad de accidentes. En ellas puede ser más importante revisar tiempos de respuesta, condiciones viales, traslados entre localidades y riesgos asociados a la geografia.

El tercer resultado es que la colision con vehículo automotor domina el total de accidentes. Esto sugiere estrategias enfocadas en interacciones vehiculares: distancia segura, respeto a semaforos, señalamientos, control de velocidad y vigilancia en intersecciones.

El cuarto resultado es la relevancia de motocicletas. La colision con motocicleta aparece entre los tipos más frecuentes y la variable de motocicleta tiene peso en el modelado. Por eso, las recomendaciones deben incluir uso de casco, visibilidad, respeto de carriles y campanas dirigidas a motociclistas.

El quinto resultado es temporal: las tardes cercanas al fin de semana concentran muchos accidentes, y viernes por la tarde registra 10,802 casos. Esta información permite proponer acciones por horario, como operativos preventivos, mensajes en redes o refuerzo de vigilancia en horas de salida laboral.

## 10. Discusion crítica y limitaciones

La primera limitación es que ATUS cubre accidentes en zonas urbanas y suburbanas. Por lo tanto, no necesariamente representa todos los accidentes carreteros del estado. Esto importa en Sonora porque hay municipios con grandes distancias y movilidad interurbana.

La segunda limitación es que algunas variables son amplias. Por ejemplo, `Conductor` aparece como causa probable en la gran mayoria de registros, pero no distingue si el problema fue velocidad, distraccion, alcohol, falta de respeto a señales u otro comportamiento especifico.

La tercera limitación es la calidad de algunas variables. La edad del conductor tiene valores faltantes o no especificados. También hay variables como aliento o cinturon con categorias no especificadas. Esto reduce la precision interpretativa de ciertos hallazgos.

La cuarta limitación es que los modelos no deben interpretarse como predictores exactos del futuro. Los accidentes son eventos complejos que dependen de condiciones de movilidad, clima, infraestructura, conducta, vigilancia y otros factores que no siempre estan en la base.

La quinta limitación es que el análisis regional se definio de forma operativa para comparar municipios. Aunque la segmentacion ayuda a interpretar, podría ajustarse con criterios oficiales de planeacion, movilidad o seguridad pública si se cuenta con ellos.

## 11. Conclusiones

El proyecto permitio conocer mejor los accidentes de tránsito en Sonora durante el periodo 2015-2024. La base final tuvo 183,911 accidentes reales y mostro diferencias importantes entre regiones, municipios, tipos de accidente y niveles de gravedad.

Una conclusión central es que el volumen de accidentes y la gravedad no siempre coinciden. Hermosillo concentra la mayor cantidad de accidentes, pero regiones como Sierra, Centro y Sur y Valle presentan mayores porcentajes de accidentes graves. Esto confirma que una estrategia preventiva debe combinar cantidad y severidad.

Otra conclusión es que la causa probable `Conductor` domina los registros. Esto no significa culpar a personas individuales, sino reconocer que la conducta vial debe ser un eje fuerte de prevencion. La educacion vial, el control de velocidad, la atencion a motociclistas y la vigilancia en horarios criticos pueden tener impacto.

En modelado, el Random Forest ajustado fue la recomendación principal por su equilibrio entre precision y recall para accidentes graves. La Regresion Logística queda como alternativa interpretable, especialmente si se busca explicar de manera sencilla los resultados o priorizar recall. KNN y el árbol IF-THEN se incorporaron como referencias del curso y para fortalecer la explicabilidad.

El clustering jerárquico agrego valor al mostrar que los municipios pueden agruparse por perfiles de riesgo. Esto abre la puerta a estrategias diferenciadas por tipo de municipio, en lugar de aplicar una sola recomendación general para todo el estado.

En general, el proyecto demuestra que la minería de datos puede apoyar la prevención vial cuando se combina análisis exploratorio, calidad de datos, modelos evaluados correctamente e interpretación humana de los resultados.

## 12. Recomendaciones

1. Priorizar acciones de alto volumen en Hermosillo, Sur y Valle y Frontera.
2. Atender la gravedad proporcional en Sierra, Centro y Sur y Valle.
3. Reforzar campanas sobre velocidad, distancia segura y respeto a senalamientos.
4. Desarrollar campanas especificas para motociclistas.
5. Revisar horarios criticos, especialmente tardes cercanas al fin de semana y viernes por la tarde.
6. Complementar ATUS con datos de infraestructura, clima, alcoholimetria y carreteras si se desea un análisis más completo.
7. Mantener el repositorio organizado para que los notebooks puedan ejecutarse de nuevo con datos actualizados.

## 13. Referencias bibliográficas

Instituto Nacional de Estadistica y Geografia. (2025). Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas (ATUS), 1997-2024. INEGI. https://www.inegi.org.mx/programas/accidentes/

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.

McKinney, W. (2010). Data structures for statistical computing in Python. Proceedings of the 9th Python in Science Conference, 56-61.

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95.

Waskom, M. L. (2021). seaborn: Statistical data visualization. Journal of Open Source Software, 6(60), 3021.

## 14. Anexos: código relevante

### Anexo A. Carga de datos

```python
YEARS = list(range(2015, 2025))
SONORA_ID = "26"

frames = []
for year in YEARS:
    tmp = read_atus_year(year)
    tmp = tmp[tmp["ID_ENTIDAD"].astype(str).str.zfill(2) == SONORA_ID].copy()
    frames.append(tmp)

atus = pd.concat(frames, ignore_index=True)
atus = atus[atus["TIPACCID"].ne("Certificado cero")].copy()
```

### Anexo B. Construccion de gravedad

```python
atus["TOTAL_MUERTOS"] = atus[dead_cols].fillna(0).sum(axis=1)
atus["TOTAL_HERIDOS"] = atus[injury_cols].fillna(0).sum(axis=1)
atus["TOTAL_VICTIMAS"] = atus["TOTAL_MUERTOS"] + atus["TOTAL_HERIDOS"]

atus["GRAVE_BIN"] = (
    (atus["TOTAL_VICTIMAS"] > 0) |
    (atus["CLASACC"].isin(["Fatal", "No fatal"]))
).astype(int)
```

### Anexo C. Preprocesamiento para modelos

```python
preprocess = ColumnTransformer(
    transformers=[
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=20)),
        ]), categorical_features),
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), numeric_features),
    ]
)
```

### Anexo D. Random Forest ajustado

### Anexo D1. KNN linea base

```python
knn_model = Pipeline([
    ("preprocess", preprocess),
    ("model", KNeighborsClassifier(n_neighbors=5, weights="distance")),
])

knn_model.fit(X_knn_train, y_knn_train)
knn_pred = knn_model.predict(X_knn_test)
```

### Anexo D2. Regla IF-THEN del árbol de Decision

```python
tree_rule_model = Pipeline([
    ("preprocess", preprocess),
    ("model", DecisionTreeClassifier(max_depth=3, min_samples_leaf=100, random_state=42)),
])

tree_rule_model.fit(X_train, y_train)
tree_rules = export_text(
    tree_rule_model.named_steps["model"],
    feature_names=list(tree_rule_model.named_steps["preprocess"].get_feature_names_out()),
    max_depth=3,
)

print("Regla IF-THEN extraida del arbol:")
print(tree_rules)
```

```python
rf_pipeline = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(random_state=42, n_jobs=-1)),
])

param_distributions = {
    "model__n_estimators": [120, 200],
    "model__max_depth": [None, 12, 20],
    "model__min_samples_leaf": [1, 3, 5],
    "model__max_features": ["sqrt", "log2"],
    "model__class_weight": ["balanced", "balanced_subsample"],
}
```

### Anexo E. Clustering jerárquico

```python
municipal = (
    atus.groupby(["ID_MUNICIPIO", "NOM_MUNICIPIO", "REGION"])
    .agg(
        accidentes=("GRAVE_BIN", "size"),
        pct_graves=("GRAVE_BIN", "mean"),
        heridos_prom=("TOTAL_HERIDOS", "mean"),
        muertos_prom=("TOTAL_MUERTOS", "mean"),
        pct_moto=("INVOLUCRA_MOTO", "mean"),
    )
    .reset_index()
)

X_cluster = StandardScaler().fit_transform(municipal[cluster_features])
Z = linkage(X_cluster, method="ward")
```
