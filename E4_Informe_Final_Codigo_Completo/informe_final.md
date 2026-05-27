# Informe final - Prevencion vial en Sonora con ATUS

## Portada e identificacion del equipo

Proyecto: Prevencion vial en Sonora mediante analisis de accidentes de transito.

Materia: Mineria de Datos.

Institucion: TecNM / Instituto Tecnologico de Hermosillo.

Equipo:

- Felix Gautrin Diane.
- Landavazo Vasquez Andres Leonardo.
- Fuentes Babuca Felipe de Jesus.

Fuente principal de datos: Accidentes de Transito Terrestre en Zonas Urbanas y Suburbanas (ATUS), INEGI.

Periodo analizado: 2015-2024.

## Resumen ejecutivo

Este proyecto estudia los accidentes de transito registrados en Sonora durante los ultimos diez años disponibles en la base ATUS. El proposito principal fue identificar patrones regionales de frecuencia, gravedad y causas probables para proponer acciones preventivas mas enfocadas. El enfoque no fue buscar culpables individuales, sino entender el comportamiento general de los datos y traducirlo en informacion util para la seguridad vial.

El analisis partio de registros anuales de accidentes en zonas urbanas y suburbanas. Despues de filtrar Sonora y eliminar registros marcados como `Certificado cero`, se trabajo con 183,911 accidentes reales. Se construyeron variables derivadas como region, total de heridos, total de fallecidos, total de victimas, participacion de motocicleta o bicicleta, rango de hora y una variable binaria de gravedad.

La exploracion mostro que Hermosillo concentra el mayor numero de accidentes, seguido por Sur y Valle y Frontera. Sin embargo, las regiones con mayor porcentaje de accidentes graves fueron Sierra, Centro y Sur y Valle. Esta diferencia fue una de las partes mas importantes del proyecto, porque demuestra que el volumen de accidentes y la gravedad no siempre apuntan a los mismos lugares.

En modelado se implementaron varios enfoques. Primero, un Arbol de Decision como linea base. Despues, una Regresion Logistica como modelo interpretable y un Random Forest ajustado como modelo mas elaborado. Tambien se uso clustering jerarquico para agrupar municipios con comportamientos parecidos y reglas de asociacion para encontrar combinaciones frecuentes relacionadas con accidentes graves.

La recomendacion principal fue usar el Random Forest ajustado como modelo de clasificacion cuando se busca el mejor equilibrio entre precision y recall para accidentes graves. Este informe queda alineado con el cuaderno principal `notebooks/atus_sonora_10_anios_prevencion.ipynb` y con el entregable E3 actualizado. La Regresion Logistica se conserva como alternativa cuando se necesita una explicacion mas sencilla. El clustering y las reglas de asociacion complementan el analisis porque ayudan a traducir los resultados en acciones preventivas por region o tipo de municipio.

## 1. Introduccion y contexto del problema

Los accidentes de transito son una problematica social porque afectan directamente la seguridad de conductores, pasajeros, peatones, ciclistas, motociclistas y familias. Ademas de los danos materiales, los accidentes pueden provocar lesiones, muertes, costos economicos, interrupciones en la movilidad y presion sobre servicios de emergencia.

En Sonora, el comportamiento de los accidentes no es igual en todos los municipios. La capital, las ciudades fronterizas, las zonas costeras, los municipios del sur y las localidades serranas tienen condiciones de movilidad diferentes. Por eso, analizar solamente el total estatal puede ocultar patrones importantes.

El proyecto se planteo desde un enfoque preventivo e interpretativo. La pregunta principal fue: que patrones presentan los accidentes de transito en las diferentes regiones de Sonora y cuales son las causas mas frecuentes que pueden ayudar a proponer estrategias de prevencion vial.

Para responder esta pregunta, se trabajo con datos reales y publicos del INEGI. El uso de una fuente oficial permite que el analisis sea reproducible y que las conclusiones se basen en evidencia. La idea fue avanzar desde la comprension del problema hasta el modelado, sin perder de vista que el resultado final debe servir para interpretar y prevenir.

## 2. Descripcion del dataset

La base utilizada fue Accidentes de Transito Terrestre en Zonas Urbanas y Suburbanas (ATUS), publicada por el Instituto Nacional de Estadistica y Geografia. Se trabajaron los archivos anuales de 2015 a 2024, lo que permite observar una decada completa de comportamiento.

Los datos originales incluyen accidentes de todo Mexico. Para este proyecto se filtro solamente el estado de Sonora, identificado con la clave de entidad 26. Tambien se uso el catalogo municipal para agregar el nombre del municipio a partir de la clave de entidad y municipio.

| Elemento | Resultado |
|---|---:|
| Periodo cubierto | 2015-2024 |
| Registros de Sonora antes de depurar | 187,104 |
| Registros `Certificado cero` eliminados | 3,193 |
| Accidentes reales analizados | 183,911 |
| Municipios presentes | 70 |
| Porcentaje de accidentes graves | 16.99% |

Las variables disponibles incluyen informacion geografica, temporal, categorica y numerica. Entre las variables mas importantes estan municipio, año, mes, dia de semana, hora, tipo de accidente, causa probable, tipo de vehiculos involucrados, personas heridas y personas fallecidas.

Para facilitar el analisis se crearon variables derivadas. La variable `REGION` permite comparar zonas de Sonora. `TOTAL_HERIDOS`, `TOTAL_MUERTOS` y `TOTAL_VICTIMAS` resumen el impacto humano del accidente. `GRAVE_BIN` clasifica si el accidente tuvo victimas. `RANGO_HORA` agrupa la hora del accidente en madrugada, manana, tarde y noche. `INVOLUCRA_MOTO` e `INVOLUCRA_BICI` indican si participaron motocicletas o bicicletas.

## 3. Preparacion y calidad de datos

La preparacion inicio con la lectura de los CSV anuales. Para que el proyecto fuera reproducible, los notebooks se configuraron para cargar los archivos desde GitHub o desde una copia local. Despues se filtro Sonora y se eliminaron registros de `Certificado cero`, porque esos registros indican ausencia de accidente y no representan eventos viales ocurridos.

Tambien se convirtieron variables numericas que venian como texto. Esto fue necesario para sumar heridos, fallecidos y vehiculos involucrados. Las claves de entidad y municipio se normalizaron con ceros a la izquierda para unir correctamente con el catalogo municipal.

En calidad de datos se detectaron valores faltantes principalmente en la edad del conductor. Esta variable se conservo, pero en los modelos se trato con imputacion de mediana. En variables categoricas se uso imputacion por moda. Esta decision permite no perder registros y mantiene el dataset completo para el modelado.

Se identificaron 274 duplicados exactos. Debido al tamano del dataset, su presencia no cambia de forma importante el analisis exploratorio, pero se documentaron como parte de la calidad de datos. Para modelado final, se recomienda eliminarlos si el objetivo es entrenar modelos de produccion.

Los outliers se conservaron. En este problema, los valores extremos no son ruido automaticamente: un accidente con muchos heridos, fallecidos o vehiculos involucrados puede ser justamente el caso que mas interesa prevenir. Eliminar esos registros hubiera reducido la capacidad del analisis para estudiar la gravedad.

## 4. Analisis exploratorio

El analisis exploratorio permitio conocer el comportamiento general antes de aplicar modelos. El primer hallazgo fue temporal: los accidentes aumentaron de manera gradual hasta 2019, bajaron en 2020 y subieron con fuerza despues de ese año. El valor mas alto se observo en 2023, con 26,557 accidentes.

Por region, Hermosillo concentro 65,252 accidentes, seguido por Sur y Valle con 54,154 y Frontera con 44,264. Este resultado era esperado porque son zonas con mayor movilidad urbana, actividad economica o flujo vehicular. Sin embargo, la gravedad conto una historia diferente.

Cuando se reviso el porcentaje de accidentes graves, la Sierra tuvo 24.25%, Centro 22.38% y Sur y Valle 21.12%. Hermosillo, aunque tiene el mayor volumen de accidentes, tuvo 13.39% de accidentes graves. Esto muestra que la prevencion debe mirar tanto cantidad como severidad.

El tipo de accidente mas frecuente fue la colision con vehiculo automotor, con 125,202 casos. En segundo lugar aparecio la colision con motocicleta, con 18,531 casos, y despues la colision con objeto fijo, con 17,205 casos. Estos resultados sugieren que una parte importante de la prevencion debe enfocarse en interacciones entre vehiculos, control de velocidad, distancia segura y puntos de conflicto urbano.

La causa probable mas registrada fue `Conductor`, con 178,145 accidentes. Aunque esta categoria es amplia, indica que las estrategias preventivas deben considerar conducta vial, atencion al volante, respeto a senalamientos, velocidad y educacion vial.

El analisis por hora y dia mostro una concentracion relevante los viernes por la tarde, con 10,802 accidentes. Este patron puede relacionarse con salida laboral, movilidad comercial y traslados de fin de semana. A nivel preventivo, este resultado sugiere reforzar vigilancia, campanas y control operativo en horarios especificos.

## 5. Metodologia de modelado

La etapa de modelado se diseno para cubrir tres necesidades: tener una linea base simple, construir un modelo mas fuerte de clasificacion y agregar un metodo diferente para entender la estructura del dataset.

La variable objetivo fue `GRAVE_BIN`. Esta variable vale 1 si el accidente tuvo personas heridas o fallecidas, y 0 si no tuvo victimas. Se eligio esta definicion porque el enfoque del proyecto es preventivo: interesa distinguir los accidentes que generan mayor impacto humano.

Para evitar fuga de informacion, no se usaron como predictores las columnas `TOTAL_HERIDOS`, `TOTAL_MUERTOS`, `TOTAL_VICTIMAS` ni `CLASACC`, porque estan directamente relacionadas con la definicion de gravedad. Si se usaran, el modelo recibiria parte de la respuesta de forma indirecta.

Las variables predictoras incluyeron region, municipio, mes, dia de semana, rango de hora, tipo de accidente, causa probable, tipo de camino o superficie, sexo, aliento, cinturon, edad del conductor, total de vehiculos, participacion de motocicleta y participacion de bicicleta.

Para el preprocesamiento se uso imputacion de faltantes, codificacion One-Hot para variables categoricas y normalizacion para variables numericas. Despues se dividieron los datos en entrenamiento y prueba con estratificacion, para mantener una proporcion parecida de accidentes graves y no graves.

## 6. Modelos implementados

| Modelo | Tipo | Funcion dentro del proyecto |
|---|---|---|
| Arbol de Decision base | Clasificacion supervisada | Sirve como linea base simple con parametros por defecto |
| Regresion Logistica | Clasificacion supervisada interpretable | Permite comparar con un modelo claro y facil de explicar |
| Random Forest ajustado | Clasificacion supervisada elaborada | Busca mejor rendimiento con ajuste de hiperparametros |
| Clustering jerarquico | Aprendizaje no supervisado | Agrupa municipios con patrones parecidos |
| Reglas de asociacion | Metodo descriptivo | Encuentra combinaciones frecuentes relacionadas con gravedad |

El Arbol de Decision se uso como punto de partida. Es facil de entender, pero puede ser inestable y ajustarse demasiado a los datos si no se controla su profundidad. Aun asi, cumple bien la funcion de linea base.

La Regresion Logistica se incluyo porque es interpretable. Aunque no siempre logra el mejor rendimiento, permite entender de forma mas clara como cambian las probabilidades segun las variables. Tambien se uso con pesos balanceados para dar mayor atencion a la clase grave.

El Random Forest ajustado fue el modelo mas elaborado. Combina muchos arboles y reduce la dependencia de una sola estructura. Se ajustaron hiperparametros como numero de arboles, profundidad, minimo de muestras por hoja, seleccion de variables y pesos de clase.

El clustering jerarquico se aplico a nivel municipal. En lugar de clasificar accidentes individuales, agrupa municipios segun indicadores como total de accidentes, porcentaje de gravedad, promedio de heridos, promedio de fallecidos, presencia de motocicletas, bicicletas y tipos de accidente.

Las reglas de asociacion se usaron como complemento interpretativo. Este metodo ayuda a encontrar combinaciones frecuentes de condiciones que terminan en gravedad alta, por ejemplo cierto tipo de accidente o combinaciones de region, causa y horario.

## 7. Evaluacion de modelos

La evaluacion de clasificacion no se baso solamente en accuracy. En este problema, un modelo podria tener buen accuracy si clasifica bien los accidentes no graves, porque son la mayoria. Sin embargo, para seguridad vial importa especialmente la clase grave.

Por eso se revisaron precision, recall, F1-score, matriz de confusion, curva ROC y ROC-AUC. La precision indica que tan confiables son las predicciones positivas de gravedad. El recall indica cuantos accidentes graves reales logra detectar el modelo. El F1-score resume el equilibrio entre precision y recall.

En la ejecucion documentada en E3, el Random Forest ajustado obtuvo el mejor F1 para la clase grave. La Regresion Logistica tuvo el mayor recall, por lo que puede ser util si la prioridad principal es detectar la mayor cantidad posible de accidentes graves, aunque produzca mas falsos positivos.

| Modelo | Accuracy | Precision grave | Recall grave | F1 grave | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Arbol de Decision base | 0.8466 | 0.5491 | 0.5437 | 0.5464 | 0.7260 |
| Regresion Logistica | 0.8229 | 0.4861 | 0.7387 | 0.5863 | 0.8806 |
| Random Forest ajustado | 0.8600 | 0.5719 | 0.7007 | 0.6298 | 0.8911 |

Estos resultados corresponden al notebook E3 alineado con el cuaderno principal ATUS. La interpretacion se mantiene: no basta con ver accuracy, porque la clase grave es menos frecuente y es la mas importante para prevencion.

## 8. Comparativa y recomendacion

Con base en las metricas, el modelo recomendado para el proyecto es el Random Forest ajustado. La razon principal es que ofrece el mejor equilibrio general para la clase grave, especialmente en F1-score. Esto significa que logra una relacion mas balanceada entre detectar accidentes graves y no marcar demasiados accidentes como graves cuando no lo son.

La Regresion Logistica no se descarta. Su recall fue alto, lo que significa que detecta una mayor proporcion de accidentes graves. En un contexto preventivo donde se prefiere activar alertas aunque existan falsos positivos, podria ser una opcion util. Ademas, es mas facil de explicar que Random Forest.

El Arbol de Decision base cumple como referencia inicial, pero no seria la primera recomendacion final. Su desempeno fue menor y puede depender mucho de pequenas variaciones en los datos.

El clustering jerarquico no compite directamente con los clasificadores porque responde otra pregunta. Mientras los clasificadores predicen gravedad a nivel de accidente, el clustering agrupa municipios. Esto permite pensar en estrategias diferenciadas: municipios con alto volumen, municipios con alta gravedad proporcional y municipios con participacion relevante de motocicletas o tipos especificos de accidente.

## 9. Resultados preventivos principales

El primer resultado preventivo es que Hermosillo, Sur y Valle y Frontera concentran el mayor volumen de accidentes. Estas regiones requieren acciones de escala amplia: educacion vial, control de velocidad, vigilancia en cruces y seguimiento de zonas con alta movilidad.

El segundo resultado es que la Sierra, Centro y Sur y Valle tienen porcentajes de gravedad mas altos. Estas zonas requieren atencion aunque no siempre aparezcan como las de mayor cantidad de accidentes. En ellas puede ser mas importante revisar tiempos de respuesta, condiciones viales, traslados entre localidades y riesgos asociados a la geografia.

El tercer resultado es que la colision con vehiculo automotor domina el total de accidentes. Esto sugiere estrategias enfocadas en interacciones vehiculares: distancia segura, respeto a semaforos, senalamientos, control de velocidad y vigilancia en intersecciones.

El cuarto resultado es la relevancia de motocicletas. La colision con motocicleta aparece entre los tipos mas frecuentes y la variable de motocicleta tiene peso en el modelado. Por eso, las recomendaciones deben incluir uso de casco, visibilidad, respeto de carriles y campanas dirigidas a motociclistas.

El quinto resultado es temporal: las tardes cercanas al fin de semana concentran muchos accidentes, y viernes por la tarde registra 10,802 casos. Esta informacion permite proponer acciones por horario, como operativos preventivos, mensajes en redes o refuerzo de vigilancia en horas de salida laboral.

## 10. Discusion critica y limitaciones

La primera limitacion es que ATUS cubre accidentes en zonas urbanas y suburbanas. Por lo tanto, no necesariamente representa todos los accidentes carreteros del estado. Esto importa en Sonora porque hay municipios con grandes distancias y movilidad interurbana.

La segunda limitacion es que algunas variables son amplias. Por ejemplo, `Conductor` aparece como causa probable en la gran mayoria de registros, pero no distingue si el problema fue velocidad, distraccion, alcohol, falta de respeto a senales u otro comportamiento especifico.

La tercera limitacion es la calidad de algunas variables. La edad del conductor tiene valores faltantes o no especificados. Tambien hay variables como aliento o cinturon con categorias no especificadas. Esto reduce la precision interpretativa de ciertos hallazgos.

La cuarta limitacion es que los modelos no deben interpretarse como predictores exactos del futuro. Los accidentes son eventos complejos que dependen de condiciones de movilidad, clima, infraestructura, conducta, vigilancia y otros factores que no siempre estan en la base.

La quinta limitacion es que el analisis regional se definio de forma operativa para comparar municipios. Aunque la segmentacion ayuda a interpretar, podria ajustarse con criterios oficiales de planeacion, movilidad o seguridad publica si se cuenta con ellos.

## 11. Conclusiones

El proyecto permitio conocer mejor los accidentes de transito en Sonora durante el periodo 2015-2024. La base final tuvo 183,911 accidentes reales y mostro diferencias importantes entre regiones, municipios, tipos de accidente y niveles de gravedad.

Una conclusion central es que el volumen de accidentes y la gravedad no siempre coinciden. Hermosillo concentra la mayor cantidad de accidentes, pero regiones como Sierra, Centro y Sur y Valle presentan mayores porcentajes de accidentes graves. Esto confirma que una estrategia preventiva debe combinar cantidad y severidad.

Otra conclusion es que la causa probable `Conductor` domina los registros. Esto no significa culpar a personas individuales, sino reconocer que la conducta vial debe ser un eje fuerte de prevencion. La educacion vial, el control de velocidad, la atencion a motociclistas y la vigilancia en horarios criticos pueden tener impacto.

En modelado, el Random Forest ajustado fue la recomendacion principal por su equilibrio entre precision y recall para accidentes graves. La Regresion Logistica queda como alternativa interpretable, especialmente si se busca explicar de manera sencilla los resultados o priorizar recall.

El clustering jerarquico agrego valor al mostrar que los municipios pueden agruparse por perfiles de riesgo. Esto abre la puerta a estrategias diferenciadas por tipo de municipio, en lugar de aplicar una sola recomendacion general para todo el estado.

En general, el proyecto demuestra que la mineria de datos puede apoyar la prevencion vial cuando se combina analisis exploratorio, calidad de datos, modelos evaluados correctamente e interpretacion humana de los resultados.

## 12. Recomendaciones

1. Priorizar acciones de alto volumen en Hermosillo, Sur y Valle y Frontera.
2. Atender la gravedad proporcional en Sierra, Centro y Sur y Valle.
3. Reforzar campanas sobre velocidad, distancia segura y respeto a senalamientos.
4. Desarrollar campanas especificas para motociclistas.
5. Revisar horarios criticos, especialmente tardes cercanas al fin de semana y viernes por la tarde.
6. Complementar ATUS con datos de infraestructura, clima, alcoholimetria y carreteras si se desea un analisis mas completo.
7. Mantener el repositorio organizado para que los notebooks puedan ejecutarse de nuevo con datos actualizados.

## 13. Referencias bibliograficas

Instituto Nacional de Estadistica y Geografia. (2025). Accidentes de Transito Terrestre en Zonas Urbanas y Suburbanas (ATUS), 1997-2024. INEGI. https://www.inegi.org.mx/programas/accidentes/

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.

McKinney, W. (2010). Data structures for statistical computing in Python. Proceedings of the 9th Python in Science Conference, 56-61.

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95.

Waskom, M. L. (2021). seaborn: Statistical data visualization. Journal of Open Source Software, 6(60), 3021.

## 14. Anexos: codigo relevante

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

### Anexo E. Clustering jerarquico

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
