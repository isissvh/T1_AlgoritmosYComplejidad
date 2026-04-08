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

    if not nombre:
        nombre = ruta_csv.parent.name

    return nombre

def cargar_todos_los_csv():
    archivos_rssdelta = sorted(SOURCE_DIR.glob("*_results_rssdelta.csv"))

    archivos = archivos_rssdelta

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos de resultados en {SOURCE_DIR}"
        )

    lista_dfs = []

    for archivo in archivos:
        df = pd.read_csv(archivo)
        df.columns = df.columns.str.strip()

        df["algorithm"] = extraer_algoritmo_desde_archivo(archivo)

        lista_dfs.append(df)

    df_total = pd.concat(lista_dfs, ignore_index=True)
    return df_total

def preparar_datos(df):

    columnas_necesarias = ["n", "time_ms", "algorithm"]

    for col in columnas_necesarias:
        if col not in df.columns:
            raise ValueError(f"Falta la columna obligatoria: {col}")

    if "rss_delta_kb" not in df.columns:
        df["rss_delta_kb"] = pd.NA

    df["n"] = pd.to_numeric(df["n"], errors="coerce")
    df["time_ms"] = pd.to_numeric(df["time_ms"], errors="coerce")
    df["rss_delta_kb"] = pd.to_numeric(df["rss_delta_kb"], errors="coerce")

    df = df.dropna(subset=["n", "time_ms", "algorithm"])

    df = df[df["n"] > 0]
    df = df[df["time_ms"] > 0]

    df["n"] = df["n"].astype(int)
    df["algorithm"] = df["algorithm"].astype(str)

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
    elif tipo == "n3":
        base = n_vals ** 3
        ref = n_ref ** 3
    elif tipo == "n2.81":
        exponente = np.log2(7)
        base = n_vals ** exponente
        ref = n_ref ** exponente
    else:
        raise ValueError("Tipo no soportado")

    return (y_ref / ref) * base

def graficar_tiempo_vs_tamano(df):

    df_plot = df.copy()

    fig, ax = plt.subplots(figsize=(12, 7))

    df_mean = (
        df_plot.groupby(["n", "algorithm"], as_index=False)["time_ms"]
        .mean()
        .sort_values("n")
    )

    tabla = df_mean.pivot(index="n", columns="algorithm", values="time_ms").sort_index()

    for algoritmo in tabla.columns:
        ax.plot(
            tabla.index,
            tabla[algoritmo],
            marker="o",
            label=algoritmo
        )

    ax.set_title("Tiempo de ejecución vs Tamaño de entrada")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_xticks([2**4, 2**6, 2**8, 2**10])
    ax.set_xticklabels(["2⁴", "2⁶", "2⁸", "2¹⁰"])
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "tiempo_vs_tamano.png")

def graficar_curvas_teoricas(df, algoritmo, casos_teoricos, nombre_archivo):
    df_plot = df[df["algorithm"] == algoritmo].copy()

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
    ax.set_xticks([2**4, 2**6, 2**8, 2**10])
    ax.set_xticklabels(["2⁴", "2⁶", "2⁸", "2¹⁰"])
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, nombre_archivo)

def curvas_teoricas_helper(df):
    graficar_curvas_teoricas(
        df,
        "naive",
        [
            ("naive teórico O(n³)", "n3", "--")
        ],
        "tiempo_naive_teorico.png"
    )

    graficar_curvas_teoricas(
        df,
        "strassen",
        [
            ("strassen teórico O(n²·⁸¹)", "n2.81", "--")
        ],
        "tiempo_strassen_teorico.png"
    )

def graficar_memoria_vs_tamano(df):

    df_plot = df.copy()

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
    ax.set_xticks([2**4, 2**6, 2**8, 2**10])
    ax.set_xticklabels(["2⁴", "2⁶", "2⁸", "2¹⁰"])
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "memoria_vs_tamano.png")

def graficar_memoria_vs_tamano2(df):
    df_plot = df.copy()

    df_plot = df_plot.dropna(subset=["rss_delta_kb"])
    # df_plot = df_plot[df_plot["rss_delta_kb"] > 0]
    df_plot = df_plot[df_plot["algorithm"].isin(["strassen", "naive"])]
    df_plot["rss_delta_mb"] = df_plot["rss_delta_kb"] / 1024

    n_objetivo = [2**4, 2**6, 2**8, 2**10]
    df_plot = df_plot[df_plot["n"].isin(n_objetivo)]

    df_mean = (
        df_plot.groupby(["n", "algorithm"], as_index=False)["rss_delta_mb"]
        .mean()
        .sort_values("n")
    )

    tabla = (
        df_mean.pivot(index="n", columns="algorithm", values="rss_delta_mb")
        .reindex(n_objetivo)
    )

    tabla = tabla.dropna(subset=["strassen", "naive"])
    tabla["diff_mb"] = tabla["strassen"] - tabla["naive"]

    fig, ax = plt.subplots(figsize=(12, 7))

    etiquetas = ["2⁴", "2⁶", "2⁸", "2¹⁰"][:len(tabla.index)]

    ax.bar(etiquetas, tabla["diff_mb"])

    ax.axhline(0, linewidth=1)
    ax.set_title("Diferencia de memoria: strassen - naive")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Diferencia de memoria RSS Delta (MB)")
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "memoria_vs_tamano2.png")

def main():
    df = cargar_todos_los_csv()
    df = preparar_datos(df)

    print("\nAlgoritmos encontrados:", sorted(df["algorithm"].unique()))

    graficar_tiempo_vs_tamano(df)
    graficar_memoria_vs_tamano(df)
    graficar_memoria_vs_tamano2(df)
    curvas_teoricas_helper(df)

    print(f"\nGráficos guardados en: {PLOTS_DIR}")

if __name__ == "__main__":
    main()