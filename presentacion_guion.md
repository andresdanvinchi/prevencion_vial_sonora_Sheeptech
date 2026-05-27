# Presentación: Análisis de accidentes de tránsito en Sonora para identificar patrones de riesgo vial

## Diapositiva 1: Portada
1. **Título:** Análisis de accidentes de tránsito en Sonora para identificar patrones de riesgo vial
2. **Texto breve:** Minería de Datos | ATUS INEGI 2015-2024 | Enfoque preventivo
3. **Visual:** Imagen sobria relacionada con prevención vial o una franja con íconos de carretera, peatón y vehículo. No requiere gráfica.
4. **Notas:** Presentar el proyecto como un análisis basado en datos reales para entender dónde, cuándo y cómo ocurren accidentes con mayor riesgo en Sonora. Frase: "El objetivo no es solo describir accidentes, sino convertir los datos en información útil para prevenirlos."
5. **Recomendación visual:** Fondo claro, título grande al centro, subtítulo debajo y datos del equipo/institución en la parte inferior. Usar acento azul oscuro o verde vial.

## Diapositiva 2: Problema de estudio
1. **Título:** Los accidentes viales tienen patrones que pueden analizarse
2. **Texto breve:** Los accidentes generan daños materiales, lesiones y muertes. En Sonora, el riesgo no se distribuye igual entre regiones, municipios, tipos de accidente y horarios.
3. **Visual:** Usar una lámina conceptual o captura del informe/propuesta donde se explique el contexto del problema. Alternativa: tabla simple con impactos: lesiones, fallecimientos, costos y movilidad.
4. **Notas:** Explicar que analizar solo el total estatal oculta diferencias importantes. Frase: "No todos los municipios tienen el mismo volumen ni la misma gravedad."
5. **Recomendación visual:** Dos columnas: izquierda con el problema en 3 bullets; derecha con una imagen o esquema de impacto vial. Transición: "A partir de este problema planteamos una pregunta y un objetivo."

## Diapositiva 3: Pregunta de investigación y objetivo
1. **Título:** ¿Qué patrones explican el riesgo vial en Sonora?
2. **Texto breve:** Pregunta: ¿Qué patrones presentan los accidentes de tránsito en las regiones de Sonora y cómo pueden apoyar estrategias de prevención? Objetivo: identificar patrones de frecuencia, gravedad, causa, horario y municipio usando minería de datos.
3. **Visual:** Diagrama pequeño: Datos ATUS -> análisis -> modelos -> prevención.
4. **Notas:** Aclarar que el proyecto combina análisis exploratorio y modelos para generar interpretación preventiva. Frase: "Buscamos pasar de registros históricos a decisiones preventivas."
5. **Recomendación visual:** Colocar pregunta en una banda superior y objetivo en una caja limpia debajo. Evitar mucho texto. Transición: "Para responder esto usamos una fuente oficial."

## Diapositiva 4: Fuente de datos ATUS / INEGI
1. **Título:** Se utilizaron datos ATUS de INEGI 2015-2024
2. **Texto breve:** Fuente: Accidentes de Tránsito Terrestre en Zonas Urbanas y Suburbanas. Se filtró Sonora, clave de entidad 26, y se trabajaron 183,911 accidentes reales.
3. **Visual:** `presentacion_assets/generated/dataset_resumen.png`. Revisar notebook principal, celda 11, e informe final sección "Descripción del dataset".
4. **Notas:** Mencionar que ATUS es una fuente pública y reproducible. Frase: "El análisis se basa en datos oficiales, no en percepciones."
5. **Recomendación visual:** Tabla de resumen a la derecha y a la izquierda un bloque corto con fuente, periodo y cobertura. Transición: "Después de obtener los datos, el siguiente paso fue prepararlos."

## Diapositiva 5: Preparación y limpieza de datos
1. **Título:** Antes de analizar, los datos se limpiaron y prepararon
2. **Texto breve:** Se unieron archivos anuales, se filtró Sonora, se eliminaron registros "Certificado cero", se normalizaron claves municipales y se convirtieron variables numéricas.
3. **Visual:** `presentacion_assets/generated/limpieza_flujo.png`. Revisar E2, secciones 4 y 5; notebook principal, celda 13-14.
4. **Notas:** Explicar que la limpieza evita analizar registros que no representan accidentes reales. Frase: "La calidad de datos define qué tan confiables serán las conclusiones."
5. **Recomendación visual:** Flujo horizontal de 5 a 6 pasos. Mantener texto breve. Transición: "Con los datos listos, creamos variables para interpretar mejor el riesgo."

## Diapositiva 6: Variables creadas: región, gravedad y víctimas
1. **Título:** Se crearon variables para medir riesgo y gravedad
2. **Texto breve:** Variables clave: REGION, TOTAL_HERIDOS, TOTAL_MUERTOS, TOTAL_VICTIMAS, GRAVE_BIN, NIVEL_GRAVEDAD, RANGO_HORA, INVOLUCRA_MOTO e INVOLUCRA_BICI.
3. **Visual:** `presentacion_assets/generated/variables_creadas.png`. Revisar notebook principal, celda 13-14, y README "Variables principales creadas".
4. **Notas:** Explicar que la gravedad se definió con base en heridos o fallecidos. Frase: "Un accidente grave es aquel que tuvo impacto humano, no solo daño material."
5. **Recomendación visual:** Tabla de variables con una columna de uso. Resaltar `GRAVE_BIN` con color. Transición: "Estas variables permitieron empezar con el análisis exploratorio."

## Diapositiva 7: Análisis exploratorio general
1. **Título:** El análisis exploratorio mostró volumen, gravedad y causas dominantes
2. **Texto breve:** El dataset final tiene 183,911 accidentes. La mayoría son de solo daños, pero 16.99% presentan heridos o fallecidos.
3. **Visual:** `presentacion_assets/generated/eda_general_con_gravedad.png`. Se generó a partir del notebook principal, celdas 17 y 20, para mostrar en una sola evidencia año, gravedad, región y tipo de accidente.
4. **Notas:** Comentar que esta gráfica resume accidentes por año, región, tipo y causa. Frase: "Primero observamos el panorama general antes de modelar."
5. **Recomendación visual:** Usar la gráfica completa ocupando 70% de la diapositiva y una nota lateral con 2 hallazgos. Transición: "Después bajamos el análisis al nivel regional y municipal."

## Diapositiva 8: Accidentes por región y municipio
1. **Título:** Hermosillo concentra más accidentes, pero la gravedad cambia por región
2. **Texto breve:** Hermosillo registra 65,252 accidentes. Sur y Valle y Frontera también concentran muchos casos. Sierra presenta el mayor porcentaje de accidentes graves: 24.25%.
3. **Visual:** `presentacion_assets/generated/region_municipio_riesgo.png`. Se generó con la tabla `region_summary` y el top de municipios del notebook principal, celda 20.
4. **Notas:** Diferenciar volumen y severidad. Frase: "Una región puede tener pocos accidentes, pero una proporción alta de casos graves."
5. **Recomendación visual:** Gráfica de barras por región a la izquierda y tabla pequeña de porcentaje de gravedad a la derecha. Transición: "Luego revisamos qué tipos y causas aparecen con más frecuencia."

## Diapositiva 9: Accidentes por tipo y causa probable
1. **Título:** La colisión con vehículo automotor domina el registro
2. **Texto breve:** El tipo más común es la colisión con vehículo automotor. La causa probable más frecuente es Conductor, lo que orienta la prevención hacia conducta vial y control operativo.
3. **Visual:** `presentacion_assets/generated/tipo_causa_ranking.png`. Se generó desde el ranking de `TIPACCID` y `CAUSAACCI` del notebook principal, celda 17.
4. **Notas:** Evitar interpretar "Conductor" como culpa individual; es una categoría amplia. Frase: "El dato apunta a reforzar educación, señalamiento, velocidad y atención al volante."
5. **Recomendación visual:** Dos barras horizontales: tipo de accidente y causa probable. Añadir un callout: "Conductor = categoría amplia". Transición: "Además del lugar y tipo, también importa cuándo ocurren los accidentes."

## Diapositiva 10: Análisis temporal: años, meses y horarios críticos
1. **Título:** La tarde concentra el riesgo, con viernes como franja crítica
2. **Texto breve:** Los accidentes aumentan después de 2020. En el cruce día-hora, la tarde concentra los valores más altos y el viernes por la tarde aparece como franja crítica con 10,802 accidentes.
3. **Visual:** `presentacion_assets/notebook_outputs/main_cell_51_img_1.png` para serie mensual y `presentacion_assets/notebook_outputs/main_cell_23_img_2.png` para día y rango de hora. Revisar notebook principal, celdas 23 y 51.
4. **Notas:** Relacionar viernes tarde con salida laboral, movilidad comercial y traslados de fin de semana. Aclarar que el sábado por la tarde también es alto, por lo que la lectura preventiva es reforzar tardes cercanas al fin de semana. Frase: "El horario crítico permite pensar en prevención focalizada, no solo general."
5. **Recomendación visual:** Colocar arriba la serie mensual y abajo el heatmap. Resaltar viernes-tarde con un callout, sin decir que sea el único máximo absoluto. Transición: "Para comprobar asociaciones entre variables usamos pruebas estadísticas."

## Diapositiva 11: Prueba Chi-cuadrada y Cramér’s V
1. **Título:** Las variables categóricas sí muestran asociación estadística
2. **Texto breve:** Se aplicó Chi-cuadrada para detectar dependencia y Cramér’s V para medir fuerza de asociación. La relación más fuerte fue REGION vs TIPACCID.
3. **Visual:** `presentacion_assets/generated/chi_cramers_table.png`. Revisar notebook principal, celda 27.
4. **Notas:** Explicar que p-value significativo no siempre implica relación fuerte; por eso se usa Cramér’s V. Frase: "La estadística confirma que los patrones no son completamente aleatorios."
5. **Recomendación visual:** Tabla con la relación más fuerte resaltada. Agregar mini nota: "p-value: significancia; V: fuerza". Transición: "Después buscamos combinaciones frecuentes con reglas de asociación."

## Diapositiva 12: Reglas de asociación con Apriori
1. **Título:** Los atropellamientos se asocian fuertemente con gravedad alta
2. **Texto breve:** Las reglas muestran que los accidentes tipo atropellamiento tienen alta relación con accidentes graves. Esto tiene utilidad directa para proteger peatones.
3. **Visual:** `presentacion_assets/generated/apriori_reglas.png`. Revisar notebook principal, celda 31, o E3 celda 24.
4. **Notas:** Definir rápido soporte, confianza y lift. Frase: "Apriori ayuda a encontrar combinaciones que conviene vigilar de forma preventiva."
5. **Recomendación visual:** Tabla de 3 reglas principales y un callout: "Atropellamiento -> gravedad alta". Transición: "Con estas variables también entrenamos modelos de clasificación."

## Diapositiva 13: Modelos de clasificación de gravedad
1. **Título:** Se entrenaron modelos para clasificar accidentes graves
2. **Texto breve:** Variable objetivo: GRAVE_BIN. Modelos: Árbol de Decisión, Regresión Logística y Random Forest ajustado. Se evitó fuga de información excluyendo heridos, muertos, víctimas y CLASACC como predictores.
3. **Visual:** `presentacion_assets/generated/modelos_pipeline_gravedad.png`. Para evidencia de evaluación específica se pueden revisar `presentacion_assets/notebook_outputs/e3_cell_14_img_1.png`, `e3_cell_16_img_1.png` y `e3_cell_18_img_1.png` en E3 celdas 14, 16 y 18.
4. **Notas:** Explicar por qué no se usaron variables que ya contienen la respuesta. Frase: "El modelo debía aprender patrones previos, no recibir la gravedad ya calculada."
5. **Recomendación visual:** Tres mini paneles por modelo o un diagrama de pipeline: preprocesamiento -> entrenamiento -> evaluación. Transición: "La comparación se hizo con métricas enfocadas en la clase grave."

## Diapositiva 14: Comparación de modelos
1. **Título:** Random Forest logró el mejor equilibrio para gravedad
2. **Texto breve:** Random Forest ajustado obtuvo F1 grave de 0.6298 y ROC-AUC de 0.8911. Regresión Logística tuvo mayor recall grave: 0.7387.
3. **Visual:** `presentacion_assets/generated/modelos_comparacion.png`. Revisar E3 celda 26.
4. **Notas:** Explicar que accuracy no basta porque los accidentes graves son minoría. Frase: "En prevención vial importa detectar los casos graves, no solo acertar en la mayoría."
5. **Recomendación visual:** Tabla comparativa con Random Forest resaltado y una nota para Regresión Logística como opción sensible al recall. Transición: "Para entender el modelo fuerte revisamos sus variables más importantes."

## Diapositiva 15: Importancia de variables con Random Forest
1. **Título:** El tipo de accidente fue una señal clave para el modelo
2. **Texto breve:** Las variables más importantes incluyeron tipo de accidente, atropellamiento, participación de motocicleta, total de vehículos, edad del conductor y algunos municipios/regiones.
3. **Visual:** `presentacion_assets/notebook_outputs/e3_cell_20_img_1.png` o `main_cell_43_img_1.png`. Revisar E3 celda 20 o notebook principal celda 43.
4. **Notas:** Conectar importancia de variables con prevención: no solo predice, también orienta acciones. Frase: "El modelo confirma que el tipo de accidente y la exposición de usuarios vulnerables importan."
5. **Recomendación visual:** Gráfica de importancia ocupando casi toda la diapositiva, con 2 callouts: "Atropellamiento" y "Motocicleta". Transición: "Además de clasificar accidentes, agrupamos municipios similares."

## Diapositiva 16: Clustering jerárquico de municipios
1. **Título:** El clustering agrupó municipios con comportamientos similares
2. **Texto breve:** El clustering jerárquico permitió identificar perfiles municipales según volumen, porcentaje de gravedad, heridos, fallecidos, motocicletas y vehículos involucrados.
3. **Visual:** `presentacion_assets/notebook_outputs/e3_cell_22_img_1.png` o `main_cell_47_img_1.png`. Revisar E3 celda 22.
4. **Notas:** Aclarar que clustering no predice gravedad individual; agrupa municipios para diseñar estrategias. Frase: "No todos los municipios necesitan la misma intervención preventiva."
5. **Recomendación visual:** Dendrograma grande y tabla pequeña con número de clusters seleccionado: 6. Transición: "Con los resultados estadísticos y de modelos, pasamos a la interpretación preventiva."

## Diapositiva 17: Interpretación preventiva de resultados
1. **Título:** Los hallazgos se traducen en acciones preventivas
2. **Texto breve:** Alto volumen: Hermosillo, Sur y Valle, Frontera. Alta gravedad proporcional: Sierra, Centro, Sur y Valle. Riesgos clave: atropellamientos, motocicletas y viernes por la tarde.
3. **Visual:** `presentacion_assets/generated/matriz_preventiva.png`.
4. **Notas:** Enfatizar que el proyecto no termina en gráficas; busca orientar prevención. Frase: "La minería de datos tiene valor cuando ayuda a decidir dónde actuar primero."
5. **Recomendación visual:** Matriz de hallazgo, lugar y acción. Usar colores discretos: azul para evidencia, verde para acción. Transición: "De esta interpretación salen las conclusiones principales."

## Diapositiva 18: Conclusiones
1. **Título:** El riesgo vial en Sonora combina volumen y gravedad
2. **Texto breve:** Hermosillo concentra más accidentes, pero Sierra y Centro presentan mayor proporción de gravedad. Los modelos y reglas confirman que tipo de accidente, horario y región aportan señales preventivas.
3. **Visual:** Tres conclusiones numeradas o mini resumen con iconos: región, gravedad, modelo.
4. **Notas:** Cerrar la parte analítica con una idea clara: volumen y gravedad deben analizarse juntos. Frase: "La prevención debe priorizar tanto dónde ocurren más accidentes como dónde son más graves."
5. **Recomendación visual:** Slide limpia con 3 bloques horizontales. No usar tablas grandes. Transición: "A partir de eso proponemos recomendaciones concretas."

## Diapositiva 19: Recomendaciones
1. **Título:** Recomendaciones para prevención vial basada en datos
2. **Texto breve:** Priorizar regiones de alto volumen, atender zonas con alta gravedad, reforzar educación vial, proteger peatones y motociclistas, y focalizar acciones en viernes por la tarde.
3. **Visual:** Lista visual de 5 recomendaciones con íconos sencillos. Puede reutilizarse `presentacion_assets/generated/matriz_preventiva.png` si se prefiere evidencia.
4. **Notas:** Explicar que las recomendaciones son de orientación, no políticas definitivas. Frase: "Los datos ayudan a enfocar recursos donde pueden tener mayor impacto."
5. **Recomendación visual:** Cinco tarjetas pequeñas o lista con íconos; evitar párrafos. Transición: "Finalmente, cerramos con las fuentes utilizadas."

## Diapositiva 20: Referencias
1. **Título:** Referencias
2. **Texto breve:** INEGI ATUS 1997-2024; scikit-learn; pandas; matplotlib; seaborn; notebooks E2 y E3 del proyecto.
3. **Visual:** Lista bibliográfica breve con logos institucionales solo si son oficiales/verificados. Si no, usar texto.
4. **Notas:** Mencionar que los notebooks permiten reproducir el análisis. Frase: "Todas las gráficas y modelos provienen de los notebooks del proyecto y de datos públicos de INEGI."
5. **Recomendación visual:** Fondo claro, referencias en letra pequeña pero legible. Incluir ruta de notebooks: `E2_Analisis_Exploratorio_Preprocesamiento.ipynb`, `E3_Modelos_Evaluacion_ATUS_Sonora.ipynb`, `notebooks/atus_sonora_10_anios_prevencion.ipynb`.
