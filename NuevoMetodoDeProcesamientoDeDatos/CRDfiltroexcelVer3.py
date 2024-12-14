import pandas as pd
import concurrent.futures
from tqdm import tqdm  # For progress bar


def process_row(row, sintomas_unicos, original_columns):
    """Procesa una fila individual y extrae los síntomas."""
    nuevo_registro = {col: row[col] for col in original_columns}
    for col in row.index:
        if col.startswith('DIAGNOSTICO') and pd.notna(row[col]) and row[col] != "DESCONOCIDO":
            diagnostico = row[col]
            sintoma = diagnostico.split('.')[0]
            if '.' in diagnostico:
                nuevo_registro[sintoma] = diagnostico.split('.')[1]
            else:
                nuevo_registro[sintoma] = '-1'
    return nuevo_registro


if __name__ == '__main__':
    # Leer el archivo original
    input_file = '../GRD_PUBLICO_EXTERNO_2022_limpio.txt'
    output_file = 'output_file.parquet'  # Nuevo archivo de salida en formato Parquet

    # Leer el archivo original con un límite de 129 campos
    print(f"Leyendo el archivo '{input_file}'...")
    df = pd.read_csv(input_file, delimiter='|', usecols=range(129), encoding='ISO-8859-1')
    print(f"Archivo leído correctamente. Filas procesadas: {len(df)}")

    # Lista para almacenar los síntomas únicos (solo la parte antes del punto)
    sintomas_unicos = set()

    # Extraer los síntomas únicos de las columnas de diagnósticos
    print("Extrayendo síntomas únicos...")
    for col in df.columns:
        if col.startswith('DIAGNOSTICO'):
            # Filtrar valores no nulos y diferentes de "DESCONOCIDO"
            diagnosticos = df[col].dropna().loc[df[col] != "DESCONOCIDO"]
            # Extraer la parte antes del punto y agregar a los síntomas únicos
            sintomas_unicos.update(diagnostico.split('.')[0] for diagnostico in diagnosticos)

    # Convertir el conjunto de síntomas únicos en una lista y ordenarla
    sintomas_unicos = sorted(sintomas_unicos)
    print(f"Síntomas únicos extraídos: {len(sintomas_unicos)}")

    # Crear un nuevo DataFrame con todas las columnas necesarias
    print("Creando un nuevo DataFrame con todas las columnas necesarias...")
    all_columns = [col for col in df.columns if not col.startswith('DIAGNOSTICO')] + sintomas_unicos
    df_procesado = pd.DataFrame(columns=all_columns)

    # Columnas originales excluyendo las de diagnósticos
    original_columns = [col for col in df.columns if not col.startswith('DIAGNOSTICO')]

    # Procesar cada fila del DataFrame usando multithreading
    registros_procesados = []
    print("Procesando filas en paralelo...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for index, row in tqdm(df.iterrows(), total=len(df), desc="Procesando filas"):
            futures.append(executor.submit(process_row, row, sintomas_unicos, original_columns))

        # Recopilar resultados en chunks para evitar consumo excesivo de memoria
        chunk_size = 10000  # Tamaño del chunk
        chunk = []
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Recopilando resultados"):
            chunk.append(future.result())
            if len(chunk) >= chunk_size:
                df_procesado = pd.concat([df_procesado, pd.DataFrame(chunk)], ignore_index=True)
                chunk = []

        # Añadir el último chunk si no está vacío
        if chunk:
            df_procesado = pd.concat([df_procesado, pd.DataFrame(chunk)], ignore_index=True)

    # Eliminar las columnas de diagnósticos originales
    df_procesado = df_procesado.drop(columns=[col for col in df_procesado.columns if col.startswith('DIAGNOSTICO')])

    # Escribir el DataFrame en un archivo Parquet
    print(f"Escribiendo el archivo de salida '{output_file}'...")
    df_procesado.to_parquet(output_file, engine='pyarrow', index=False)

    print(f"Archivo '{output_file}' creado exitosamente.")