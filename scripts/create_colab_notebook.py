import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "atus_sonora_10_anios_prevencion.ipynb"


def md(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip().splitlines(True),
    }


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.strip().splitlines(True),
    }


cells = [
    md(
        r"""
# Prevencion vial en Sonora con ATUS, ultimos 10 anos disponibles

Este notebook esta preparado para Google Colab y analiza accidentes de transito de Sonora usando la base ATUS de INEGI.

Periodo usado: **2015 a 2024**, que corresponde a los ultimos 10 anos disponibles en los archivos locales del proyecto.

Tecnicas aplicadas:

- Analisis exploratorio de datos (EDA)
- Analisis regional y temporal
- Chi-cuadrada y Cramer's V
- Reglas de asociacion con Apriori
- Regresion logistica
- Random Forest
- Clustering jerarquico
- Series de tiempo exploratorias con ARIMA y Prophet si esta disponible

Nota metodologica: la gravedad se construye con heridos/fallecidos o la clasificacion del accidente. Por eso, esas variables no se usan como predictoras en los modelos de clasificacion para evitar fuga de informacion.
"""
    ),
    md(
        r"""
## 1. Instalacion de librerias

En Colab, esta celda instala dependencias que no siempre vienen incluidas. Si estas ejecutando localmente y ya las tienes instaladas, puedes omitirla.
"""
    ),
    code(
        r"""
import sys
import subprocess
import importlib.util

def ensure_package(import_name, pip_name=None):
    if importlib.util.find_spec(import_name) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pip_name or import_name])

ensure_package("mlxtend")
ensure_package("statsmodels")

# Prophet puede tardar en instalarse. Se intenta usar solo si ya esta disponible.
"""
    ),
    md("## 2. Carga de librerias y configuracion"),
    code(
        r"""
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import chi2_contingency
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from mlxtend.frequent_patterns import apriori, association_rules

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 100)
sns.set_theme(style="whitegrid", palette="Set2")
"""
    ),
    md(
        r"""
## 3. Ubicar datos del proyecto

Para usarlo en Colab, sube la carpeta del proyecto completa o monta Google Drive. El notebook buscara automaticamente `datos/originales/conjunto_de_datos`.
"""
    ),
    code(
        r"""
# Si usas Google Drive, descomenta estas lineas:
# from google.colab import drive
# drive.mount("/content/drive")

candidate_base_dirs = [
    Path.cwd(),
    Path.cwd().parent,
    Path("/content/prevencion_vial_sonora_Sheeptech"),
    Path("/content/drive/MyDrive/prevencion_vial_sonora_Sheeptech"),
]

PROJECT_DIR = None
for base in candidate_base_dirs:
    if (base / "datos" / "originales" / "conjunto_de_datos").exists():
        PROJECT_DIR = base
        break

if PROJECT_DIR is None:
    raise FileNotFoundError(
        "No se encontro la carpeta datos/originales/conjunto_de_datos. "
        "Sube el proyecto completo a Colab o ajusta PROJECT_DIR manualmente."
    )

DATA_DIR = PROJECT_DIR / "datos" / "originales" / "conjunto_de_datos"
CAT_DIR = PROJECT_DIR / "datos" / "originales" / "catalogos"

print("Proyecto:", PROJECT_DIR)
print("Datos:", DATA_DIR)
"""
    ),
    md("## 4. Cargar ATUS 2015-2024 y filtrar Sonora"),
    code(
        r"""
YEARS = list(range(2015, 2025))
SONORA_ID = "26"

def read_atus_year(year):
    path = DATA_DIR / f"atus_anual_{year}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No existe {path}")
    df = pd.read_csv(
        path,
        dtype=str,
        skipinitialspace=True,
        encoding="utf-8",
        low_memory=False,
        index_col=False,
    )
    df.columns = df.columns.str.strip()
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": np.nan, "None": np.nan})
    return df

frames = []
for year in YEARS:
    tmp = read_atus_year(year)
    tmp = tmp[tmp["ID_ENTIDAD"].astype(str).str.strip().str.zfill(2) == SONORA_ID].copy()
    frames.append(tmp)

atus = pd.concat(frames, ignore_index=True)

mun = pd.read_csv(CAT_DIR / "tc_municipio.csv", dtype=str, encoding="utf-8", skipinitialspace=True)
mun.columns = mun.columns.str.strip()
for col in mun.columns:
    mun[col] = mun[col].astype(str).str.strip()
mun["ID_ENTIDAD"] = mun["ID_ENTIDAD"].str.zfill(2)
mun["ID_MUNICIPIO"] = mun["ID_MUNICIPIO"].str.zfill(3)

atus["ID_ENTIDAD"] = atus["ID_ENTIDAD"].astype(str).str.strip().str.zfill(2)
atus["ID_MUNICIPIO"] = atus["ID_MUNICIPIO"].astype(str).str.strip().str.zfill(3)

# ATUS incluye registros "Certificado cero" para indicar ausencia de accidente.
# Se excluyen porque el proyecto analiza accidentes ocurridos.
atus = atus[atus["TIPACCID"].ne("Certificado cero")].copy()

atus = atus.merge(
    mun[["ID_ENTIDAD", "ID_MUNICIPIO", "NOM_MUNICIPIO"]],
    on=["ID_ENTIDAD", "ID_MUNICIPIO"],
    how="left",
)

print("Registros Sonora 2015-2024:", len(atus))
display(atus.head())
"""
    ),
    md("## 5. Limpieza, variables derivadas y regiones"),
    code(
        r"""
dead_cols = ["CONDMUERTO", "PASAMUERTO", "PEATMUERTO", "CICLMUERTO", "OTROMUERTO", "NEMUERTO"]
injury_cols = ["CONDHERIDO", "PASAHERIDO", "PEATHERIDO", "CICLHERIDO", "OTROHERIDO", "NEHERIDO"]
vehicle_cols = [
    "AUTOMOVIL", "CAMPASAJ", "MICROBUS", "PASCAMION", "OMNIBUS", "TRANVIA",
    "CAMIONETA", "CAMION", "TRACTOR", "FERROCARRI", "MOTOCICLET", "BICICLETA", "OTROVEHIC"
]
numeric_cols = dead_cols + injury_cols + vehicle_cols

for col in numeric_cols + ["ANIO", "ID_HORA", "ID_MINUTO", "ID_DIA", "ID_EDAD"]:
    if col in atus.columns:
        atus[col] = pd.to_numeric(atus[col], errors="coerce")

atus["TOTAL_MUERTOS"] = atus[dead_cols].fillna(0).sum(axis=1)
atus["TOTAL_HERIDOS"] = atus[injury_cols].fillna(0).sum(axis=1)
atus["TOTAL_VICTIMAS"] = atus["TOTAL_MUERTOS"] + atus["TOTAL_HERIDOS"]
atus["TOTAL_VEHICULOS"] = atus[vehicle_cols].fillna(0).sum(axis=1)
atus["INVOLUCRA_MOTO"] = (atus["MOTOCICLET"].fillna(0) > 0).astype(int)
atus["INVOLUCRA_BICI"] = (atus["BICICLETA"].fillna(0) > 0).astype(int)

atus["GRAVE_BIN"] = (
    (atus["TOTAL_VICTIMAS"] > 0) |
    (atus["CLASACC"].isin(["Fatal", "No fatal"]))
).astype(int)
atus["NIVEL_GRAVEDAD"] = np.select(
    [atus["TOTAL_MUERTOS"] > 0, atus["TOTAL_HERIDOS"] > 0],
    ["Fatal", "Con heridos"],
    default="Solo danos",
)

region_map = {
    "030": "Hermosillo",
    "002": "Frontera", "019": "Frontera", "027": "Frontera", "035": "Frontera",
    "039": "Frontera", "041": "Frontera", "043": "Frontera", "055": "Frontera",
    "058": "Frontera", "059": "Frontera", "060": "Frontera", "067": "Frontera",
    "004": "Costa y desierto", "007": "Costa y desierto", "017": "Costa y desierto",
    "046": "Costa y desierto", "047": "Costa y desierto", "048": "Costa y desierto",
    "064": "Costa y desierto", "065": "Costa y desierto", "070": "Costa y desierto",
    "001": "Centro", "006": "Centro", "013": "Centro", "014": "Centro", "016": "Centro",
    "020": "Centro", "021": "Centro", "022": "Centro", "023": "Centro", "024": "Centro",
    "028": "Centro", "034": "Centro", "037": "Centro", "038": "Centro", "045": "Centro",
    "050": "Centro", "053": "Centro", "054": "Centro", "056": "Centro", "057": "Centro",
    "063": "Centro", "066": "Centro", "068": "Centro",
    "003": "Sur y Valle", "012": "Sur y Valle", "018": "Sur y Valle", "025": "Sur y Valle",
    "026": "Sur y Valle", "029": "Sur y Valle", "033": "Sur y Valle", "042": "Sur y Valle",
    "049": "Sur y Valle", "051": "Sur y Valle", "071": "Sur y Valle", "072": "Sur y Valle",
    "005": "Sierra", "008": "Sierra", "009": "Sierra", "010": "Sierra", "011": "Sierra",
    "015": "Sierra", "031": "Sierra", "032": "Sierra", "040": "Sierra", "044": "Sierra",
    "052": "Sierra", "061": "Sierra", "062": "Sierra", "069": "Sierra",
}
atus["REGION"] = atus["ID_MUNICIPIO"].map(region_map).fillna("Otros municipios")

atus["MES_NUM"] = pd.to_numeric(atus["MES"], errors="coerce")
atus["DIA_VALIDO"] = atus["ID_DIA"].where(atus["ID_DIA"].between(1, 31))
atus["FECHA"] = pd.to_datetime(
    dict(year=atus["ANIO"], month=atus["MES_NUM"], day=atus["DIA_VALIDO"]),
    errors="coerce",
)
atus["FECHA_MES"] = pd.to_datetime(
    dict(year=atus["ANIO"], month=atus["MES_NUM"], day=1),
    errors="coerce",
)

atus["HORA_VALIDA"] = atus["ID_HORA"].where(atus["ID_HORA"].between(0, 23))
atus["RANGO_HORA"] = pd.cut(
    atus["HORA_VALIDA"],
    bins=[-0.1, 5, 11, 17, 23],
    labels=["Madrugada", "Manana", "Tarde", "Noche"],
)

atus["EDAD_CONDUCTOR"] = atus["ID_EDAD"].where(atus["ID_EDAD"].between(12, 98))

print(atus[["ANIO", "NOM_MUNICIPIO", "REGION", "TIPACCID", "CAUSAACCI", "NIVEL_GRAVEDAD", "GRAVE_BIN"]].head())
print("\nDistribucion de gravedad:")
display(atus["NIVEL_GRAVEDAD"].value_counts(dropna=False))
"""
    ),
    md("## 6. Analisis exploratorio de datos"),
    code(
        r"""
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

atus["ANIO"].value_counts().sort_index().plot(kind="bar", ax=axes[0, 0], color="#4C78A8")
axes[0, 0].set_title("Accidentes por ano")
axes[0, 0].set_xlabel("Ano")
axes[0, 0].set_ylabel("Accidentes")

atus["REGION"].value_counts().plot(kind="bar", ax=axes[0, 1], color="#F58518")
axes[0, 1].set_title("Accidentes por region")
axes[0, 1].set_xlabel("Region")
axes[0, 1].set_ylabel("Accidentes")

atus["TIPACCID"].value_counts().head(10).sort_values().plot(kind="barh", ax=axes[1, 0], color="#54A24B")
axes[1, 0].set_title("Top 10 tipos de accidente")
axes[1, 0].set_xlabel("Accidentes")

atus["CAUSAACCI"].value_counts().sort_values().plot(kind="barh", ax=axes[1, 1], color="#E45756")
axes[1, 1].set_title("Causas probables")
axes[1, 1].set_xlabel("Accidentes")

plt.tight_layout()
plt.show()
"""
    ),
    code(
        r"""
region_summary = (
    atus.groupby("REGION")
    .agg(
        accidentes=("GRAVE_BIN", "size"),
        accidentes_graves=("GRAVE_BIN", "sum"),
        pct_graves=("GRAVE_BIN", "mean"),
        heridos=("TOTAL_HERIDOS", "sum"),
        fallecidos=("TOTAL_MUERTOS", "sum"),
    )
    .sort_values("accidentes", ascending=False)
)
region_summary["pct_graves"] = (region_summary["pct_graves"] * 100).round(2)
display(region_summary)

top_municipios = (
    atus.groupby("NOM_MUNICIPIO")
    .agg(accidentes=("GRAVE_BIN", "size"), graves=("GRAVE_BIN", "sum"), fallecidos=("TOTAL_MUERTOS", "sum"))
    .sort_values("accidentes", ascending=False)
    .head(15)
)
display(top_municipios)
"""
    ),
    code(
        r"""
heat_region_cause = pd.crosstab(atus["REGION"], atus["CAUSAACCI"], normalize="index") * 100
plt.figure(figsize=(12, 5))
sns.heatmap(heat_region_cause, annot=True, fmt=".1f", cmap="YlGnBu")
plt.title("Distribucion porcentual de causas por region")
plt.xlabel("Causa probable")
plt.ylabel("Region")
plt.show()

heat_hour_day = pd.crosstab(atus["RANGO_HORA"], atus["DIASEMANA"])
plt.figure(figsize=(12, 4))
sns.heatmap(heat_hour_day, annot=True, fmt=".0f", cmap="rocket_r")
plt.title("Accidentes por rango de hora y dia de semana")
plt.xlabel("Dia de semana")
plt.ylabel("Rango de hora")
plt.show()
"""
    ),
    md("## 7. Chi-cuadrada y Cramer's V"),
    code(
        r"""
def cramers_v(confusion_matrix):
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    if n == 0:
        return np.nan
    r, k = confusion_matrix.shape
    return np.sqrt((chi2 / n) / max(min(k - 1, r - 1), 1))

def chi_square_report(df, var_a, var_b):
    table = pd.crosstab(df[var_a], df[var_b])
    chi2, p, dof, expected = chi2_contingency(table)
    cv = cramers_v(table)
    return {
        "variable_1": var_a,
        "variable_2": var_b,
        "chi2": chi2,
        "p_value": p,
        "dof": dof,
        "cramers_v": cv,
        "tabla": table,
    }

pairs = [
    ("REGION", "NIVEL_GRAVEDAD"),
    ("REGION", "CAUSAACCI"),
    ("REGION", "TIPACCID"),
    ("RANGO_HORA", "NIVEL_GRAVEDAD"),
    ("DIASEMANA", "NIVEL_GRAVEDAD"),
]

results = []
for a, b in pairs:
    result = chi_square_report(atus.dropna(subset=[a, b]), a, b)
    results.append({k: v for k, v in result.items() if k != "tabla"})

chi_results = pd.DataFrame(results).sort_values("cramers_v", ascending=False)
display(chi_results)
"""
    ),
    md("## 8. Reglas de asociacion con Apriori"),
    code(
        r"""
assoc = atus.copy()
assoc["GRAVEDAD"] = np.where(assoc["GRAVE_BIN"] == 1, "Gravedad=Alta", "Gravedad=Baja")
assoc["REGION_ITEM"] = "Region=" + assoc["REGION"].astype(str)
assoc["TIPO_ITEM"] = "Tipo=" + assoc["TIPACCID"].astype(str)
assoc["CAUSA_ITEM"] = "Causa=" + assoc["CAUSAACCI"].astype(str)
assoc["HORA_ITEM"] = "Hora=" + assoc["RANGO_HORA"].astype(str)
assoc["DIA_ITEM"] = "Dia=" + assoc["DIASEMANA"].astype(str)
assoc["MES_ITEM"] = "Mes=" + assoc["MES"].astype(str)

item_cols = ["REGION_ITEM", "TIPO_ITEM", "CAUSA_ITEM", "HORA_ITEM", "DIA_ITEM", "MES_ITEM", "GRAVEDAD"]
transactions = assoc[item_cols].fillna("No especificado")

one_hot = pd.get_dummies(transactions.stack()).groupby(level=0).max().astype(bool)

min_support = 0.02
frequent = apriori(one_hot, min_support=min_support, use_colnames=True)
rules = association_rules(frequent, metric="confidence", min_threshold=0.45)

rules_graves = rules[
    rules["consequents"].apply(lambda x: "Gravedad=Alta" in x)
].copy()

rules_graves = rules_graves.sort_values(["lift", "confidence", "support"], ascending=False)
display(rules_graves[["antecedents", "consequents", "support", "confidence", "lift"]].head(20))
"""
    ),
    md("## 9. Modelos de clasificacion de gravedad"),
    code(
        r"""
# No usar TOTAL_HERIDOS, TOTAL_MUERTOS, TOTAL_VICTIMAS ni CLASACC como predictores,
# porque se usan para construir la variable objetivo GRAVE_BIN.
model_df = atus.copy()
model_df = model_df.dropna(subset=["GRAVE_BIN"])

categorical_features = [
    "REGION", "NOM_MUNICIPIO", "MES", "DIASEMANA", "RANGO_HORA",
    "TIPACCID", "CAUSAACCI", "CAPAROD", "SEXO", "ALIENTO", "CINTURON"
]
numeric_features = ["EDAD_CONDUCTOR", "TOTAL_VEHICULOS", "INVOLUCRA_MOTO", "INVOLUCRA_BICI"]

X = model_df[categorical_features + numeric_features]
y = model_df["GRAVE_BIN"].astype(int)

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

stratify = y if y.nunique() == 2 else None
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=stratify
)

print("Distribucion del objetivo:")
display(y.value_counts(normalize=True).rename("proporcion"))
"""
    ),
    code(
        r"""
log_model = Pipeline([
    ("preprocess", preprocess),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced", n_jobs=None)),
])

log_model.fit(X_train, y_train)
log_pred = log_model.predict(X_test)

print("Regresion logistica")
print("Accuracy:", round(accuracy_score(y_test, log_pred), 4))
print(classification_report(y_test, log_pred, target_names=["No grave", "Grave"]))

ConfusionMatrixDisplay.from_predictions(y_test, log_pred, display_labels=["No grave", "Grave"], cmap="Blues")
plt.title("Matriz de confusion - Regresion logistica")
plt.show()
"""
    ),
    code(
        r"""
rf_model = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced_subsample",
        min_samples_leaf=3,
        n_jobs=-1,
    )),
])

rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

print("Random Forest")
print("Accuracy:", round(accuracy_score(y_test, rf_pred), 4))
print(classification_report(y_test, rf_pred, target_names=["No grave", "Grave"]))

ConfusionMatrixDisplay.from_predictions(y_test, rf_pred, display_labels=["No grave", "Grave"], cmap="Greens")
plt.title("Matriz de confusion - Random Forest")
plt.show()
"""
    ),
    code(
        r"""
feature_names = rf_model.named_steps["preprocess"].get_feature_names_out()
importances = rf_model.named_steps["model"].feature_importances_
importance_df = (
    pd.DataFrame({"variable": feature_names, "importancia": importances})
    .sort_values("importancia", ascending=False)
    .head(25)
)

plt.figure(figsize=(10, 8))
sns.barplot(data=importance_df, y="variable", x="importancia", color="#4C78A8")
plt.title("Top 25 variables mas importantes - Random Forest")
plt.xlabel("Importancia")
plt.ylabel("")
plt.tight_layout()
plt.show()

display(importance_df)
"""
    ),
    md("## 10. Clustering jerarquico de municipios"),
    code(
        r"""
municipal = (
    atus.groupby(["ID_MUNICIPIO", "NOM_MUNICIPIO", "REGION"])
    .agg(
        accidentes=("GRAVE_BIN", "size"),
        pct_graves=("GRAVE_BIN", "mean"),
        heridos_prom=("TOTAL_HERIDOS", "mean"),
        muertos_prom=("TOTAL_MUERTOS", "mean"),
        pct_moto=("INVOLUCRA_MOTO", "mean"),
        pct_bici=("INVOLUCRA_BICI", "mean"),
        vehiculos_prom=("TOTAL_VEHICULOS", "mean"),
    )
    .reset_index()
)

top_tipos = atus["TIPACCID"].value_counts().head(6).index.tolist()
tipo_pivot = (
    pd.crosstab(atus["ID_MUNICIPIO"], atus["TIPACCID"], normalize="index")
    .reindex(columns=top_tipos, fill_value=0)
    .add_prefix("pct_tipo_")
    .reset_index()
)

municipal = municipal.merge(tipo_pivot, on="ID_MUNICIPIO", how="left").fillna(0)

cluster_features = [
    "accidentes", "pct_graves", "heridos_prom", "muertos_prom", "pct_moto",
    "pct_bici", "vehiculos_prom"
] + [c for c in municipal.columns if c.startswith("pct_tipo_")]

scaler = StandardScaler()
X_cluster = scaler.fit_transform(municipal[cluster_features])

Z = linkage(X_cluster, method="ward")

plt.figure(figsize=(16, 7))
dendrogram(Z, labels=municipal["NOM_MUNICIPIO"].values, leaf_rotation=90, leaf_font_size=8)
plt.title("Dendrograma de municipios de Sonora")
plt.ylabel("Distancia")
plt.tight_layout()
plt.show()

municipal["CLUSTER"] = fcluster(Z, t=4, criterion="maxclust")
display(municipal.sort_values(["CLUSTER", "accidentes"], ascending=[True, False]))
"""
    ),
    md("## 11. Analisis temporal y series de tiempo exploratorias"),
    code(
        r"""
monthly = (
    atus.dropna(subset=["FECHA_MES"])
    .groupby("FECHA_MES")
    .size()
    .asfreq("MS", fill_value=0)
    .rename("accidentes")
)

plt.figure(figsize=(14, 5))
monthly.plot(marker="o", color="#4C78A8")
plt.title("Accidentes mensuales en Sonora")
plt.xlabel("Mes")
plt.ylabel("Accidentes")
plt.grid(True, alpha=0.3)
plt.show()

display(monthly.describe())
"""
    ),
    code(
        r"""
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

if len(monthly) >= 24:
    decomposition = seasonal_decompose(monthly, model="additive", period=12)
    fig = decomposition.plot()
    fig.set_size_inches(14, 8)
    plt.suptitle("Descomposicion temporal: tendencia, estacionalidad y residuo", y=1.02)
    plt.show()

    arima_model = SARIMAX(
        monthly,
        order=(1, 1, 1),
        seasonal_order=(1, 0, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    arima_fit = arima_model.fit(disp=False)
    forecast = arima_fit.get_forecast(steps=12)
    forecast_mean = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    plt.figure(figsize=(14, 5))
    monthly.plot(label="Historico", color="#4C78A8")
    forecast_mean.plot(label="Pronostico exploratorio ARIMA", color="#E45756")
    plt.fill_between(
        forecast_ci.index,
        forecast_ci.iloc[:, 0],
        forecast_ci.iloc[:, 1],
        color="#E45756",
        alpha=0.2,
    )
    plt.title("Pronostico exploratorio ARIMA")
    plt.xlabel("Mes")
    plt.ylabel("Accidentes")
    plt.legend()
    plt.show()
else:
    print("No hay suficientes meses para descomposicion o ARIMA.")
"""
    ),
    code(
        r"""
# Prophet es opcional. Si no esta instalado, esta celda no detiene el notebook.
try:
    from prophet import Prophet

    prophet_df = monthly.reset_index()
    prophet_df.columns = ["ds", "y"]

    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=12, freq="MS")
    forecast = m.predict(future)

    fig1 = m.plot(forecast)
    plt.title("Pronostico exploratorio con Prophet")
    plt.xlabel("Mes")
    plt.ylabel("Accidentes")
    plt.show()

    fig2 = m.plot_components(forecast)
    plt.show()
except Exception as exc:
    print("Prophet no esta disponible o no pudo ejecutarse en este entorno.")
    print("Detalle:", exc)
"""
    ),
    md(
        r"""
## 12. Interpretacion preventiva

Usa esta seccion para redactar conclusiones con base en los resultados:

- Regiones con mayor cantidad de accidentes
- Regiones con mayor porcentaje de accidentes graves
- Causas y tipos de accidente predominantes por region
- Reglas de asociacion con mayor confianza y lift
- Variables mas importantes del Random Forest
- Municipios agrupados por comportamiento similar
- Meses, dias u horarios de mayor concentracion

Ejemplo de recomendacion:

Si una region concentra accidentes graves asociados a motocicletas durante la noche, se pueden proponer campanas de uso de casco, vigilancia en horarios nocturnos y acciones dirigidas a motociclistas.
"""
    ),
]

notebook = {
    "cells": cells,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.x",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Notebook creado: {OUT}")
