import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re

# -------------------------------------------------------------------
# RUTAS
# -------------------------------------------------------------------
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


def graficar_tiempo_vs_tamano(df):

    df_plot = df[df["source_type"] == "rssdelta"].copy()

    fig, ax = plt.subplots(figsize=(12, 7))

    df_mean = (
        df_plot.groupby(["n", "algorithm"], as_index=False)["time_ms"]
        .mean()
        .sort_values("n")
    )

    tabla = df_mean.pivot(index="n", columns="algorithm", values="time_ms").sort_index()

    for algoritmo in tabla.columns:
        ax.plot(
            tabla[algoritmo],
            tabla.index,
            marker="o",
            label=algoritmo
        )

    ax.set_title("Tiempo de ejecución vs Tamaño de entrada")
    ax.set_ylabel("Tamaño de entrada (n)")
    ax.set_xlabel("Tiempo (ms)")
    ax.set_xscale("log")
    ax.set_xlim(0, 100000000)
    ax.set_ylim(10,100000000)
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "tiempo_vs_tamano.png")


def graficar_memoria_vs_tamano(df):
    """
    Gráfico final de memoria: solo usa rssdelta y memoria válida.
    """
    df_plot = df[df["source_type"] == "rssdelta"].copy()

    # Aquí sí exigimos memoria válida
    df_plot = df_plot.dropna(subset=["rss_delta_kb"])
    df_plot = df_plot[df_plot["rss_delta_kb"] > 0]

    fig, ax = plt.subplots(figsize=(12, 7))

    df_mean = (
        df_plot.groupby(["n", "algorithm"], as_index=False)["rss_delta_kb"]
        .mean()
        .sort_values("n")
    )

    tabla = df_mean.pivot(index="n", columns="algorithm", values="rss_delta_kb").sort_index()

    for algoritmo in tabla.columns:
        ax.plot(
            tabla.index,
            tabla[algoritmo],
            marker="o",
            label=algoritmo
        )

    ax.set_title("Consumo de memoria vs Tamaño de entrada")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Memoria RSS Delta (KB)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(0, 50000)
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "memoria_vs_tamano.png")


def graficar_comparacion_tiempo(df):
    """
    Compara tiempos entre ambas ejecuciones:
    - results: línea punteada
    - rssdelta: línea continua
    """
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

        if not datos_results.empty:
            ax.plot(
                datos_results["time_ms"],
                datos_results["n"],
                marker="o",
                linestyle="--",
                alpha=0.8,
                label=f"{algoritmo} (results)"
            )

        if not datos_rssdelta.empty:
            ax.plot(
                datos_rssdelta["time_ms"],
                datos_rssdelta["n"],
                marker="o",
                linestyle="-",
                alpha=0.8,
                label=f"{algoritmo} (rssdelta)"
            )

    ax.set_title("Comparación de tiempo entre ambas ejecuciones")
    ax.set_xlabel("Tamaño de entrada (n)")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.4)

    guardar_figura(fig, "comparacion_tiempo.png")


def resumen_consistencia_tiempo(df):
    """
    Resumen numérico opcional para ver qué tan parecidas son ambas ejecuciones.
    """
    df_mean = (
        df.groupby(["n", "algorithm", "source_type"], as_index=False)["time_ms"]
        .mean()
    )

    tabla = df_mean.pivot_table(
        index=["n", "algorithm"],
        columns="source_type",
        values="time_ms"
    ).reset_index()

    if "results" in tabla.columns and "rssdelta" in tabla.columns:
        tabla["diff_abs_ms"] = (tabla["rssdelta"] - tabla["results"]).abs()
        tabla["diff_pct"] = (
            tabla["diff_abs_ms"] / tabla[["rssdelta", "results"]].mean(axis=1)
        ) * 100

        print("\nResumen de consistencia de tiempo:")
        print(tabla.head(20))

        print("\nPromedio de diferencia porcentual por algoritmo:")
        resumen = tabla.groupby("algorithm", as_index=False)["diff_pct"].mean()
        print(resumen.sort_values("diff_pct"))
    else:
        print("\nNo se pudieron comparar ambas ejecuciones para el tiempo.")


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
def main():
    df = cargar_todos_los_csv()
    df = preparar_datos(df)

    print("\nTipos de fuente encontrados:")
    print(df["source_type"].value_counts())

    print("\nAlgoritmo + fuente:")
    print(
        df.groupby(["algorithm", "source_type"])
        .size()
        .reset_index(name="filas")
    )

    print("\nAlgoritmos encontrados:", sorted(df["algorithm"].unique()))
    print("Tipos de fuente encontrados:", sorted(df["source_type"].unique()))
    print("Total de filas cargadas:", len(df))

    # Gráficos finales
    graficar_tiempo_vs_tamano(df)
    graficar_memoria_vs_tamano(df)

    # Comparación de tiempos
    graficar_comparacion_tiempo(df)

    # Resumen opcional
    resumen_consistencia_tiempo(df)

    print(f"\nGráficos guardados en: {PLOTS_DIR}")


if __name__ == "__main__":
    main()