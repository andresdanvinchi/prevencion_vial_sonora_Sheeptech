from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datos" / "originales" / "conjunto_de_datos"
CAT = ROOT / "datos" / "originales" / "catalogos" / "tc_municipio.csv"
OUT = ROOT / "presentacion_assets" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

YEARS = range(2015, 2025)
SONORA_ID = "26"

dead_cols = ["CONDMUERTO", "PASAMUERTO", "PEATMUERTO", "CICLMUERTO", "OTROMUERTO", "NEMUERTO"]
injury_cols = ["CONDHERIDO", "PASAHERIDO", "PEATHERIDO", "CICLHERIDO", "OTROHERIDO", "NEHERIDO"]
vehicle_cols = [
    "AUTOMOVIL", "CAMPASAJ", "MICROBUS", "PASCAMION", "OMNIBUS", "TRANVIA",
    "CAMIONETA", "CAMION", "TRACTOR", "FERROCARRI", "MOTOCICLET", "BICICLETA", "OTROVEHIC",
]

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


def read_clean(path):
    df = pd.read_csv(path, dtype=str, skipinitialspace=True, encoding="utf-8", low_memory=False, index_col=False)
    df.columns = df.columns.str.strip()
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().replace({"nan": np.nan, "None": np.nan})
    return df


def load_atus():
    frames = []
    for year in YEARS:
        df = read_clean(DATA / f"atus_anual_{year}.csv")
        entidad_norm = pd.to_numeric(df["ID_ENTIDAD"], errors="coerce").astype("Int64").astype(str).str.zfill(2)
        df = df[entidad_norm == SONORA_ID].copy()
        frames.append(df)
    atus = pd.concat(frames, ignore_index=True)
    atus["ID_ENTIDAD"] = pd.to_numeric(atus["ID_ENTIDAD"], errors="coerce").astype("Int64").astype(str).str.zfill(2)
    atus["ID_MUNICIPIO"] = atus["ID_MUNICIPIO"].astype(str).str.zfill(3)
    atus = atus[atus["TIPACCID"].ne("Certificado cero")].copy()

    mun = read_clean(CAT)
    mun["ID_ENTIDAD"] = pd.to_numeric(mun["ID_ENTIDAD"], errors="coerce").astype("Int64").astype(str).str.zfill(2)
    mun["ID_MUNICIPIO"] = mun["ID_MUNICIPIO"].astype(str).str.zfill(3)
    atus = atus.merge(mun[["ID_ENTIDAD", "ID_MUNICIPIO", "NOM_MUNICIPIO"]], on=["ID_ENTIDAD", "ID_MUNICIPIO"], how="left")

    for col in dead_cols + injury_cols + vehicle_cols + ["ANIO", "ID_HORA", "ID_DIA", "MES"]:
        if col in atus.columns:
            atus[col] = pd.to_numeric(atus[col], errors="coerce")
    atus["TOTAL_MUERTOS"] = atus[dead_cols].fillna(0).sum(axis=1)
    atus["TOTAL_HERIDOS"] = atus[injury_cols].fillna(0).sum(axis=1)
    atus["TOTAL_VICTIMAS"] = atus["TOTAL_MUERTOS"] + atus["TOTAL_HERIDOS"]
    atus["TOTAL_VEHICULOS"] = atus[vehicle_cols].fillna(0).sum(axis=1)
    atus["GRAVE_BIN"] = ((atus["TOTAL_VICTIMAS"] > 0) | atus["CLASACC"].isin(["Fatal", "No fatal"])).astype(int)
    atus["NIVEL_GRAVEDAD"] = np.select(
        [atus["TOTAL_MUERTOS"] > 0, atus["TOTAL_HERIDOS"] > 0],
        ["Fatal", "Con heridos"],
        default="Solo daños",
    )
    atus["REGION"] = atus["ID_MUNICIPIO"].map(region_map).fillna("Otros municipios")
    return atus


def save_fig(path):
    plt.tight_layout()
    plt.savefig(OUT / path, dpi=190, bbox_inches="tight")
    plt.close()


def label_bars(ax, fmt="{:,.0f}", xpad=3):
    for patch in ax.patches:
        width = patch.get_width()
        y = patch.get_y() + patch.get_height() / 2
        ax.text(width + xpad, y, fmt.format(width), va="center", fontsize=8, color="#18324a")


atus = load_atus()
sns.set_theme(style="whitegrid", font="DejaVu Sans")

# Slide 7: EDA general that includes volume, severity, regions, and accident type.
fig, axes = plt.subplots(2, 2, figsize=(12, 7))
annual = atus["ANIO"].value_counts().sort_index()
axes[0, 0].plot(annual.index, annual.values, marker="o", color="#207e76", linewidth=2.5)
axes[0, 0].set_title("Accidentes por año")
axes[0, 0].set_xlabel("")
axes[0, 0].set_ylabel("Accidentes")

sev = atus["NIVEL_GRAVEDAD"].value_counts().reindex(["Solo daños", "Con heridos", "Fatal"])
axes[0, 1].pie(sev.values, labels=sev.index, autopct="%1.1f%%", startangle=90, colors=["#8fb9aa", "#d87e36", "#8c2f39"])
axes[0, 1].set_title("Distribución de gravedad")

regions = atus["REGION"].value_counts().sort_values()
axes[1, 0].barh(regions.index, regions.values, color="#207e76")
axes[1, 0].set_title("Accidentes por región")
axes[1, 0].set_xlabel("Accidentes")
label_bars(axes[1, 0], xpad=600)

types = atus["TIPACCID"].value_counts().head(6).sort_values()
axes[1, 1].barh(types.index, types.values, color="#d87e36")
axes[1, 1].set_title("Top tipos de accidente")
axes[1, 1].set_xlabel("Accidentes")
label_bars(axes[1, 1], xpad=800)
fig.suptitle("Panorama exploratorio ATUS Sonora 2015-2024", fontsize=16, fontweight="bold", color="#18324a")
save_fig("eda_general_con_gravedad.png")

# Slide 8: Region and municipality specific evidence.
fig, axes = plt.subplots(1, 2, figsize=(12, 5.4), gridspec_kw={"width_ratios": [1.1, 1]})
region_summary = (
    atus.groupby("REGION")
    .agg(accidentes=("GRAVE_BIN", "size"), pct_graves=("GRAVE_BIN", lambda s: s.mean() * 100))
    .sort_values("accidentes", ascending=True)
)
axes[0].barh(region_summary.index, region_summary["accidentes"], color="#207e76", label="Accidentes")
ax2 = axes[0].twiny()
ax2.plot(region_summary["pct_graves"], region_summary.index, color="#d87e36", marker="o", linewidth=2, label="% graves")
axes[0].set_title("Región: volumen y porcentaje grave")
axes[0].set_xlabel("Accidentes")
ax2.set_xlabel("% graves")
axes[0].grid(axis="x", alpha=0.25)

top_mun = atus["NOM_MUNICIPIO"].value_counts().head(10).sort_values()
axes[1].barh(top_mun.index, top_mun.values, color="#4c78a8")
axes[1].set_title("Top 10 municipios por accidentes")
axes[1].set_xlabel("Accidentes")
label_bars(axes[1], xpad=450)
fig.suptitle("Hermosillo lidera en volumen; Sierra destaca por gravedad proporcional", fontsize=15, fontweight="bold", color="#18324a")
save_fig("region_municipio_riesgo.png")

# Slide 9: Direct ranking for accident type and probable cause.
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
types = atus["TIPACCID"].value_counts().head(8).sort_values()
axes[0].barh(types.index, types.values, color="#207e76")
axes[0].set_title("Tipos de accidente más frecuentes")
axes[0].set_xlabel("Accidentes")
label_bars(axes[0], xpad=800)
causes = atus["CAUSAACCI"].value_counts().sort_values()
axes[1].barh(causes.index, causes.values, color="#d87e36")
axes[1].set_title("Causa probable registrada")
axes[1].set_xlabel("Accidentes")
label_bars(axes[1], xpad=800)
fig.suptitle("Colisión vehicular y causa 'Conductor' dominan el registro", fontsize=15, fontweight="bold", color="#18324a")
save_fig("tipo_causa_ranking.png")

# Slide 13: Model setup congruent with classification description.
fig, ax = plt.subplots(figsize=(12, 5.2))
ax.axis("off")
items = [
    ("Objetivo", "GRAVE_BIN\\n0 = no grave\\n1 = heridos o fallecidos", "#207e76"),
    ("Predictores", "Región, municipio, mes, día, hora,\\ntipo, causa, superficie, edad, vehículos", "#4c78a8"),
    ("Preprocesamiento", "Imputación\\nOne-Hot Encoding\\nEscalamiento numérico", "#6f8f72"),
    ("Modelos", "Árbol de Decisión\\nRegresión Logística\\nRandom Forest ajustado", "#d87e36"),
    ("Evaluación", "Matriz de confusión\\nPrecision, recall, F1\\nROC-AUC", "#8c2f39"),
]
x = 0.03
for title, body, color in items:
    rect = plt.Rectangle((x, 0.23), 0.16, 0.5, facecolor=color, edgecolor="none", transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x + 0.08, 0.64, title, ha="center", va="center", color="white", fontsize=12, fontweight="bold", transform=ax.transAxes)
    ax.text(x + 0.08, 0.43, body, ha="center", va="center", color="white", fontsize=9, transform=ax.transAxes)
    if x < 0.75:
        ax.annotate("", xy=(x + 0.205, 0.48), xytext=(x + 0.165, 0.48), xycoords=ax.transAxes,
                    arrowprops=dict(arrowstyle="->", color="#18324a", lw=1.8))
    x += 0.195
ax.text(0.03, 0.88, "Pipeline de clasificación de gravedad", fontsize=17, fontweight="bold", color="#18324a", transform=ax.transAxes)
ax.text(0.03, 0.08, "Nota: se excluyeron TOTAL_HERIDOS, TOTAL_MUERTOS, TOTAL_VICTIMAS y CLASACC para evitar fuga de información.", fontsize=10, color="#576574", transform=ax.transAxes)
save_fig("modelos_pipeline_gravedad.png")

print("Visuales generados en", OUT)
