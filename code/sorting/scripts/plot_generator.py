import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import numpy as np


SOURCE_DIR = Path(__file__).resolve().parent.parent / "data" / "measurements"
PLOTS_DIR = Path(__file__).resolve().parent.parent / "data" / "plots"


def extraer_algoritmo_desde_archivo(ruta_csv):
    nombre = ruta_csv.stem
    nombre = re.sub(r"_results_rssdelta$", "", nombre)
    nombre = re.sub(r"_results$", "", nombre)

    if not nombre:
        nombre = ruta_csv.parent.name

    return nombre

def extraer_tipo_fuente(ruta_csv):

    nombre = ruta_csv.name

    if nombre.endswith("_results_rssdelta.csv"):
        return "rssdelta"
    elif nombre.endswith("_results.csv"):
        return "results"
    else:
        return "desconocido"

def cargar_todos_los_csv():
    archivos_rssdelta = sorted(SOURCE_DIR.glob("*_results_rssdelta.csv"))
    archivos_results = sorted(SOURCE_DIR.glob("*_results.csv"))

    archivos = archivos_results + archivos_rssdelta

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos de resultados en {SOURCE_DIR}"
        )

    lista_dfs = []

    for archivo in archivos:
        df = pd.read_csv(archivo)
        df.columns = df.columns.str.strip()

        df["algorithm"] = extraer_algoritmo_desde_archivo(archivo)
        df["source_type"] = extraer_tipo_fuente(archivo)

        lista_dfs.append(df)

    df_total = pd.concat(lista_dfs, ignore_index=True)
    return df_total

def preparar_datos(df):

    columnas_necesarias = ["n", "time_ms", "algorithm", "source_type"]

    for col in columnas_necesarias:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria: {col}")

    if "rss_delta_kb" not in df.columns:
        df["rss_delta_kb"] = pd.NA

    df["n"] = pd.to_numeric(df["n"], errors="coerce")
    df["time_ms"] = pd.to_numeric(df["time_ms"], errors="coerce")
    df["rss_delta_kb"] = pd.to_numeric(df["rss_delta_kb"], errors="coerce")

    df = df.dropna(subset=["n", "time_ms", "algorithm", "source_type"])

    df = df[df["n"] > 0]
    df = df[df["time_ms"] > 0]

    df["n"] = df["n"].astype(int)
    df["algorithm"] = df["algorithm"].astype(str)
    df["source_type"] = df["source_type"].astype(str)

    return df

def guardar_figura(fig, nombre_archivo):
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    ruta_salida = PLOTS_DIR / nombre_archivo
    fig.savefig(ruta_salida, dpi=300, bbox_inches="tight")
    plt.close(fig)

def curva_teorica_comparativa(n_vals, n_ref, y_ref, tipo="nlogn"):
    n_vals = np.asarray(n_vals, dtype=float)

    if tipo == "nlogn":
        base = n_vals * np.log2(n_vals)
        ref = n_ref * np.log2(n_ref)
    elif tipo == "n2":
        base = n_vals ** 2
        ref = n_ref ** 2
    else:
        raise ValueError("Tipo no soportado")

    return (y_ref / ref) * base

def graficar_tiempo_vs_tamano(df):

    df_plot = df[df["source_type"] == "rssdelta"].copy()

    fig, ax = plt.subplots(figsize=(12, 7))

    df_mean = (
        df_plot.groupby(["n", "algorithm"], as_index=False)["time_ms"]
        .mean()
        .sort_values("n")
    )

    tabla = df_mean.pivot(index="n", columns="algorithm", values="time_ms").sort_index()

    # colores = {
    #     "mergesort": "blue",
    #     "quicksort": "orange",
    #     "sort": "green"
    # }

    for algoritmo in tabla.columns:
        ax.plot(
            tabla.index,
            tabla[algoritmo],
            marker="o",
            # color=colores[algoritmo],
            label=algoritmo
        )

    ax.set_title("Tiempo de ejecución vs Tamaño de entrada")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "tiempo_vs_tamano.png")

def graficar_curvas_teoricas(df, algoritmo, casos_teoricos, nombre_archivo):
    df_plot = df[df["source_type"] == "rssdelta"].copy()
    df_plot = df_plot[df_plot["algorithm"] == algoritmo].copy()

    if df_plot.empty:
        print(f"No hay datos para {algoritmo}")
        return

    df_mean = (
        df_plot.groupby("n", as_index=False)["time_ms"]
        .mean()
        .sort_values("n")
    )

    n_vals = df_mean["n"].to_numpy(dtype=float)
    y_vals = df_mean["time_ms"].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(
        n_vals,
        y_vals,
        marker="o",
        linewidth=2,
        label=f"{algoritmo} real"
    )

    n_ref = float(n_vals[-1])
    y_ref = float(y_vals[-1])

    for etiqueta, tipo, estilo in casos_teoricos:
        y_teo = curva_teorica_comparativa(n_vals, n_ref, y_ref, tipo=tipo)
        ax.plot(
            n_vals,
            y_teo,
            linestyle=estilo,
            linewidth=2,
            label=etiqueta
        )

    ax.set_title(f"Tiempo de ejecución: {algoritmo}")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, nombre_archivo)

def curvas_teoricas_helper(df):
    graficar_curvas_teoricas(
        df,
        "mergesort",
        [
            ("mergesort teórico O(n log n)", "nlogn", "--")
        ],
        "tiempo_mergesort_teorico.png"
    )

    graficar_curvas_teoricas(
        df,
        "sort",
        [
            ("sort teórico O(n log n)", "nlogn", "--")
        ],
        "tiempo_sort_teorico.png"
    )

    graficar_curvas_teoricas(
        df,
        "quicksort",
        [
            ("quicksort teórico O(n log n)", "nlogn", "--"),
            ("quicksort teórico O(n²)", "n2", ":")
        ],
        "tiempo_quicksort_teorico.png"
    )

def graficar_memoria_vs_tamano(df):

    df_plot = df[df["source_type"] == "rssdelta"].copy()

    df_plot = df_plot.dropna(subset=["rss_delta_kb"])
    df_plot = df_plot[df_plot["rss_delta_kb"] > 0]

    df_plot["rss_delta_mb"] = df_plot["rss_delta_kb"] / 1024

    fig, ax = plt.subplots(figsize=(12, 7))

    df_mean = (
        df_plot.groupby(["n", "algorithm"], as_index=False)["rss_delta_mb"]
        .mean()
        .sort_values("n")
    )

    tabla = df_mean.pivot(index="n", columns="algorithm", values="rss_delta_mb").sort_index()

    for algoritmo in tabla.columns:
        ax.plot(
            tabla.index,
            tabla[algoritmo],
            marker="o",
            label=algoritmo
        )

    ax.set_title("Consumo de memoria vs Tamaño de entrada")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Memoria RSS Delta (MB)")
    ax.set_xscale("log")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "memoria_vs_tamano.png")

def graficar_memoria_vs_tamano_2(df):
    df_plot = df[df["source_type"] == "rssdelta"].copy()

    df_plot = df_plot.dropna(subset=["rss_delta_kb"])
    df_plot = df_plot[df_plot["rss_delta_kb"] > 0]
    df_plot = df_plot[df_plot["algorithm"].isin(["mergesort", "sort"])]

    n_objetivo = [10, 10**3, 10**5, 10**7]
    df_plot = df_plot[df_plot["n"].isin(n_objetivo)]

    df_mean = (
        df_plot.groupby(["n", "algorithm"], as_index=False)["rss_delta_kb"]
        .mean()
        .sort_values("n")
    )

    tabla = (
        df_mean.pivot(index="n", columns="algorithm", values="rss_delta_kb")
        .reindex(n_objetivo)
    )

    tabla = tabla.dropna(subset=["mergesort", "sort"])
    tabla["diff_kb"] = tabla["mergesort"] - tabla["sort"]

    fig, ax = plt.subplots(figsize=(12, 7))

    etiquetas = ["10", "10³", "10⁵", "10⁷"][:len(tabla.index)]

    ax.bar(etiquetas, tabla["diff_kb"])

    ax.axhline(0, linewidth=1)
    ax.set_title("Diferencia de memoria: mergesort - sort")
    ax.set_xlabel("Cantidad de valores (n)")
    ax.set_ylabel("Diferencia de memoria RSS Delta (KB)")
    ax.grid(True, axis="y", alpha=0.4)
    guardar_figura(fig, "memoria_vs_tamano_2.png")

def graficar_memoria_vs_tamano_3(df):
    df_plot = df[df["source_type"] == "rssdelta"].copy()

    df_plot = df_plot.dropna(subset=["rss_delta_kb"])
    df_plot = df_plot[df_plot["rss_delta_kb"] > 0]
    df_plot = df_plot[df_plot["algorithm"].isin(["mergesort", "quicksort"])]

    n_objetivo = [10, 10**3, 10**5, 10**7]
    df_plot = df_plot[df_plot["n"].isin(n_objetivo)]

    df_mean = (
        df_plot.groupby(["n", "algorithm"], as_index=False)["rss_delta_kb"]
        .mean()
        .sort_values("n")
    )

    tabla = (
        df_mean.pivot(index="n", columns="algorithm", values="rss_delta_kb")
        .reindex(n_objetivo)
    )

    tabla = tabla.dropna(subset=["mergesort", "quicksort"])
    tabla["diff_kb"] = tabla["mergesort"] - tabla["quicksort"]
    tabla["diff_mb"] = tabla["diff_kb"] / 1024

    fig, ax = plt.subplots(figsize=(12, 7))

    etiquetas = ["10", "10³", "10⁵", "10⁷"][:len(tabla.index)]

    ax.bar(etiquetas, tabla["diff_mb"])

    ax.axhline(0, linewidth=1)
    ax.set_title("Diferencia de memoria: mergesort - quicksort")
    ax.set_xlabel("Cantidad de valores (n)")
    ax.set_ylabel("Diferencia de memoria RSS Delta (MB)")
    ax.grid(True, axis="y", alpha=0.4)
    guardar_figura(fig, "memoria_vs_tamano_3.png")

def graficar_comparacion_tiempo(df):

    fig, ax = plt.subplots(figsize=(12, 7))

    df_mean = (
        df.groupby(["n", "algorithm", "source_type"], as_index=False)["time_ms"]
        .mean()
        .sort_values("n")
    )

    for algoritmo in sorted(df_mean["algorithm"].unique()):
        datos_alg = df_mean[df_mean["algorithm"] == algoritmo]

        datos_results = datos_alg[datos_alg["source_type"] == "results"]
        datos_rssdelta = datos_alg[datos_alg["source_type"] == "rssdelta"]

        colores = {
            "mergesort": "#1f77b4",
            "quicksort": "#ff7f0e",
            "sort": "#2ca02c"
        }

        if not datos_results.empty:
            ax.plot(
                datos_results["n"],
                datos_results["time_ms"],
                marker="o",
                linestyle="--",
                color=colores[algoritmo],
                alpha=0.8,
                label=f"{algoritmo} (primera ejecución)"
            )

        if not datos_rssdelta.empty:
            ax.plot(
                datos_rssdelta["n"],
                datos_rssdelta["time_ms"],
                marker="o",
                linestyle="-",
                color=colores[algoritmo],
                alpha=0.8,
                label=f"{algoritmo} (segunda ejecución)"
            )

    ax.set_title("Comparación de tiempo entre ambas ejecuciones")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "comparacion_tiempo.png")

def main():
    df = cargar_todos_los_csv()
    df = preparar_datos(df)

    print("\nAlgoritmos encontrados:", sorted(df["algorithm"].unique()))

    graficar_tiempo_vs_tamano(df)
    graficar_memoria_vs_tamano(df)
    graficar_memoria_vs_tamano_2(df)
    graficar_memoria_vs_tamano_3(df)
    curvas_teoricas_helper(df)

    graficar_comparacion_tiempo(df)

    print(f"\nGráficos guardados en: {PLOTS_DIR}")


if __name__ == "__main__":
    main()