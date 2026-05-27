# Guion de exposición

## Diapositiva 1: Portada

1. **Título de la diapositiva:** Portada
2. **Texto breve en la diapositiva:** Tema, fuente, periodo y enfoque preventivo.
3. **Gráfica, tabla o captura:** Gráfica de accidentes por año como apoyo visual.
4. **Notas para exponer oralmente:** Presentar el proyecto y dejar claro que el objetivo no es solo describir, sino prevenir.
5. **Recomendación visual:** Título grande, fondo oscuro y tres indicadores clave.
**Conexión con la siguiente:** Para entender por qué importa, pasamos al problema de estudio.

## Diapositiva 2: Problema de estudio

1. **Título de la diapositiva:** Problema de estudio
2. **Texto breve en la diapositiva:** Los accidentes viales generan daños, lesiones y fallecimientos.
3. **Gráfica, tabla o captura:** Gráfica de evolución anual.
4. **Notas para exponer oralmente:** Explicar que el riesgo vial tiene patrones por lugar, tiempo y tipo de accidente.
5. **Recomendación visual:** Dos columnas: problema a la izquierda y gráfica a la derecha.
**Conexión con la siguiente:** A partir del problema, planteamos una pregunta y un objetivo.

## Diapositiva 3: Pregunta de investigación y objetivo

1. **Título de la diapositiva:** Pregunta de investigación y objetivo
2. **Texto breve en la diapositiva:** Pregunta guía y objetivo general del proyecto.
3. **Gráfica, tabla o captura:** Bloques de texto sin gráfica.
4. **Notas para exponer oralmente:** Mostrar que la investigación busca detectar patrones de riesgo en datos ATUS.
5. **Recomendación visual:** Dos bloques equilibrados: pregunta y objetivo.
**Conexión con la siguiente:** Después definimos la fuente de datos.

## Diapositiva 4: Fuente de datos ATUS / INEGI

1. **Título de la diapositiva:** Fuente de datos ATUS / INEGI
2. **Texto breve en la diapositiva:** Datos oficiales ATUS, Sonora, 2015-2024.
3. **Gráfica, tabla o captura:** Indicadores de periodo, fuente y registros.
4. **Notas para exponer oralmente:** Explicar que INEGI da una base confiable y comparable por año.
5. **Recomendación visual:** Tarjetas superiores y una gráfica compacta.
**Conexión con la siguiente:** Con la fuente clara, explicamos cómo se limpió la base.

## Diapositiva 5: Preparación y limpieza de datos

1. **Título de la diapositiva:** Preparación y limpieza de datos
2. **Texto breve en la diapositiva:** Unificación, filtro Sonora, eliminación de Certificado cero y variables nuevas.
3. **Gráfica, tabla o captura:** Tabla de pasos de limpieza.
4. **Notas para exponer oralmente:** Subrayar que limpiar datos evita conclusiones equivocadas.
5. **Recomendación visual:** Lista breve con tabla resumen.
**Conexión con la siguiente:** Luego se muestran las variables creadas.

## Diapositiva 6: Variables creadas: región, gravedad y víctimas

1. **Título de la diapositiva:** Variables creadas: región, gravedad y víctimas
2. **Texto breve en la diapositiva:** REGION, TOTAL_VICTIMAS, GRAVE_BIN, RANGO_HORA e indicadores de moto/bici.
3. **Gráfica, tabla o captura:** Tabla de variables y uso.
4. **Notas para exponer oralmente:** Explicar que estas variables traducen registros a riesgo vial.
5. **Recomendación visual:** Tabla dominante y notas preventivas al lado.
**Conexión con la siguiente:** Con variables listas, pasamos al análisis exploratorio.

## Diapositiva 7: Análisis exploratorio general

1. **Título de la diapositiva:** Análisis exploratorio general
2. **Texto breve en la diapositiva:** Crecimiento reciente y concentración territorial.
3. **Gráfica, tabla o captura:** Accidentes por año y por región.
4. **Notas para exponer oralmente:** Mencionar el pico de 2023 y la concentración en regiones urbanas.
5. **Recomendación visual:** Dos gráficas lado a lado con una frase final.
**Conexión con la siguiente:** Después hacemos zoom territorial.

## Diapositiva 8: Accidentes por región y municipio

1. **Título de la diapositiva:** Accidentes por región y municipio
2. **Texto breve en la diapositiva:** Hermosillo concentra volumen; Sierra destaca por gravedad.
3. **Gráfica, tabla o captura:** Gráfica regional y top de municipios.
4. **Notas para exponer oralmente:** Aclarar que volumen y gravedad son dimensiones diferentes.
5. **Recomendación visual:** Gráfica de región a la izquierda y municipios a la derecha.
**Conexión con la siguiente:** Luego vemos tipo de accidente y causa.

## Diapositiva 9: Accidentes por tipo y causa probable

1. **Título de la diapositiva:** Accidentes por tipo y causa probable
2. **Texto breve en la diapositiva:** Predomina colisión con vehículo automotor y causa Conductor.
3. **Gráfica, tabla o captura:** Barras de tipo y causa.
4. **Notas para exponer oralmente:** Conectar el hallazgo con velocidad, distancia, atención y señalamiento.
5. **Recomendación visual:** Gráfica amplia con tres bullets de lectura.
**Conexión con la siguiente:** Después analizamos cuándo ocurren los riesgos.

## Diapositiva 10: Análisis temporal

1. **Título de la diapositiva:** Análisis temporal
2. **Texto breve en la diapositiva:** Años, meses y horarios críticos; tarde del viernes como ventana relevante.
3. **Gráfica, tabla o captura:** Heatmap día-hora y barras mensuales.
4. **Notas para exponer oralmente:** Explicar que el tiempo ayuda a planear vigilancia y campañas específicas.
5. **Recomendación visual:** Heatmap y barras por mes con llamada inferior.
**Conexión con la siguiente:** Luego medimos asociación estadística.

## Diapositiva 11: Chi-cuadrada y Cramér's V

1. **Título de la diapositiva:** Chi-cuadrada y Cramér's V
2. **Texto breve en la diapositiva:** Medición de asociación entre variables y gravedad.
3. **Gráfica, tabla o captura:** Barras de Cramér's V y tabla de p-valores.
4. **Notas para exponer oralmente:** Aclarar que asociación no significa causalidad, pero sí orienta prioridades.
5. **Recomendación visual:** Gráfica principal y tabla breve.
**Conexión con la siguiente:** Después buscamos combinaciones frecuentes con Apriori.

## Diapositiva 12: Reglas de asociación con Apriori

1. **Título de la diapositiva:** Reglas de asociación con Apriori
2. **Texto breve en la diapositiva:** Combinaciones de condiciones que aparecen con accidentes graves.
3. **Gráfica, tabla o captura:** Tabla de reglas: soporte, confianza y lift.
4. **Notas para exponer oralmente:** Explicar que Apriori ayuda a convertir patrones en mensajes preventivos.
5. **Recomendación visual:** Tabla ancha con explicación debajo.
**Conexión con la siguiente:** Luego pasamos a modelos predictivos.

## Diapositiva 13: Modelos de clasificación

1. **Título de la diapositiva:** Modelos de clasificación
2. **Texto breve en la diapositiva:** Árbol, regresión logística y Random Forest para clasificar gravedad.
3. **Gráfica, tabla o captura:** Diagrama conceptual y tarjeta de Random Forest.
4. **Notas para exponer oralmente:** Explicar variable objetivo GRAVE_BIN y evitar fuga de información.
5. **Recomendación visual:** Lista técnica a la izquierda, idea clave a la derecha.
**Conexión con la siguiente:** Después comparamos el desempeño.

## Diapositiva 14: Comparación de modelos

1. **Título de la diapositiva:** Comparación de modelos
2. **Texto breve en la diapositiva:** Métricas: accuracy, precisión, recall, F1 y ROC-AUC.
3. **Gráfica, tabla o captura:** Gráfica de métricas y tabla comparativa.
4. **Notas para exponer oralmente:** Decir que en prevención importa detectar casos graves, no solo acertar en promedio.
5. **Recomendación visual:** Gráfica grande y tabla pequeña.
**Conexión con la siguiente:** Luego interpretamos el modelo fuerte.

## Diapositiva 15: Importancia de variables con Random Forest

1. **Título de la diapositiva:** Importancia de variables con Random Forest
2. **Texto breve en la diapositiva:** Variables que más aportan a distinguir gravedad.
3. **Gráfica, tabla o captura:** Gráfica de importancia de variables.
4. **Notas para exponer oralmente:** Explicar que la importancia ayuda a interpretar señales, no a probar causalidad.
5. **Recomendación visual:** Gráfica horizontal y bullets de cautela.
**Conexión con la siguiente:** Después agrupamos municipios.

## Diapositiva 16: Clustering jerárquico de municipios

1. **Título de la diapositiva:** Clustering jerárquico de municipios
2. **Texto breve en la diapositiva:** Municipios agrupados por comportamiento similar.
3. **Gráfica, tabla o captura:** Dendrograma de clustering.
4. **Notas para exponer oralmente:** Mostrar que permite comparar perfiles de riesgo y no solo municipios aislados.
5. **Recomendación visual:** Dendrograma amplio con explicación lateral.
**Conexión con la siguiente:** Luego traducimos resultados a prevención.

## Diapositiva 17: Interpretación preventiva

1. **Título de la diapositiva:** Interpretación preventiva
2. **Texto breve en la diapositiva:** Acciones sugeridas por región, horario y tipo de riesgo.
3. **Gráfica, tabla o captura:** Heatmap temporal como evidencia.
4. **Notas para exponer oralmente:** Enfatizar que los resultados deben convertirse en decisiones concretas.
5. **Recomendación visual:** Lista de acciones y gráfica de apoyo.
**Conexión con la siguiente:** Después cerramos conclusiones.

## Diapositiva 18: Conclusiones

1. **Título de la diapositiva:** Conclusiones
2. **Texto breve en la diapositiva:** De datos oficiales a evidencia accionable.
3. **Gráfica, tabla o captura:** Lista de conclusiones.
4. **Notas para exponer oralmente:** Resumir E2 y E3: preparación, EDA, modelos y enfoque preventivo.
5. **Recomendación visual:** Lista amplia y limpia.
**Conexión con la siguiente:** Luego proponemos trabajo futuro.

## Diapositiva 19: Recomendaciones

1. **Título de la diapositiva:** Recomendaciones
2. **Texto breve en la diapositiva:** Mejoras: georreferenciación, clima, tráfico, tableros y actualización anual.
3. **Gráfica, tabla o captura:** Bloque visual de siguiente paso.
4. **Notas para exponer oralmente:** Explicar que el proyecto puede crecer hacia decisiones operativas.
5. **Recomendación visual:** Bullets a la izquierda y frase fuerte a la derecha.
**Conexión con la siguiente:** Finalmente citamos fuentes.

## Diapositiva 20: Referencias

1. **Título de la diapositiva:** Referencias
2. **Texto breve en la diapositiva:** INEGI, E1, E2, E3 y bibliotecas usadas.
3. **Gráfica, tabla o captura:** Lista de referencias.
4. **Notas para exponer oralmente:** Cerrar mencionando que todo se basó en datos oficiales y notebooks reproducibles.
5. **Recomendación visual:** Lista limpia sin saturar.
**Conexión con la siguiente:** Cierre de la exposición.

