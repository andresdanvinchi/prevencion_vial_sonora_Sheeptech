# E3 - Implementacion y evaluacion de modelos

## Entregable principal

El notebook principal de este entregable es:

`E3_Modelos_Evaluacion/E3_Modelos_Evaluacion_ATUS_Sonora.ipynb`

El notebook trabaja con datos de ATUS para Sonora durante 10 anos, de 2015 a 2024. El objetivo es implementar, evaluar y comparar modelos que ayuden a analizar la gravedad de accidentes de transito y a identificar patrones utiles para prevencion vial.

## a) Implementacion

Se implementaron los siguientes metodos:

| Metodo | Tipo | Proposito |
|---|---|---|
| Arbol de Decision base | Clasificacion supervisada | Linea base simple con parametros por defecto |
| Regresion Logistica | Clasificacion supervisada interpretable | Comparar con un modelo sencillo y explicable |
| Random Forest ajustado | Clasificacion supervisada elaborada | Clasificar gravedad con ajuste de hiperparametros |
| Clustering jerarquico | Aprendizaje no supervisado | Agrupar municipios con comportamiento parecido |
| Reglas de asociacion | Metodo descriptivo | Encontrar combinaciones frecuentes relacionadas con gravedad |

La variable objetivo de clasificacion es `GRAVE_BIN`, donde `1` representa accidentes con personas heridas o fallecidas, y `0` representa accidentes sin victimas.

Para evitar fuga de informacion no se usan como predictores `TOTAL_HERIDOS`, `TOTAL_MUERTOS`, `TOTAL_VICTIMAS` ni `CLASACC`, porque esas variables se relacionan directamente con la construccion de la gravedad.

## b) Evaluacion

Los modelos de clasificacion se evaluan con:

- Matriz de confusion.
- Accuracy.
- Precision de la clase grave.
- Recall de la clase grave.
- F1-score de la clase grave.
- Curva ROC.
- ROC-AUC.

El clustering jerarquico se evalua con:

- Silhouette score.
- Davies-Bouldin.
- Cohesion interna.
- Perfil de clusters por municipio.

Las reglas de asociacion se interpretan con:

- Soporte.
- Confianza.
- Lift.

## c) Comparativa

El notebook genera una tabla comparativa con los modelos de clasificacion lado a lado. La recomendacion se basa principalmente en el F1-score de la clase grave y el ROC-AUC, porque el objetivo preventivo no es solo acertar en general, sino detectar mejor los accidentes con victimas.

En terminos del problema, el modelo recomendado debe ser el que tenga mejor equilibrio entre precision y recall para la clase grave. Si el objetivo institucional fuera detectar la mayor cantidad posible de accidentes graves, tambien debe revisarse el modelo con mayor recall.

## Interpretacion general

El Random Forest ajustado se considera el candidato mas fuerte cuando obtiene el mejor equilibrio de metricas, porque aprovecha muchas variables y permite revisar importancia de caracteristicas. La regresion logistica se conserva como alternativa cuando se busca mayor facilidad de explicacion. El arbol de decision base funciona como comparacion inicial.

El clustering jerarquico complementa el analisis porque no clasifica accidentes individuales, sino que agrupa municipios con patrones similares. Esto ayuda a proponer estrategias por tipo de municipio o region. Las reglas de asociacion agregan patrones faciles de comunicar para acciones preventivas.
