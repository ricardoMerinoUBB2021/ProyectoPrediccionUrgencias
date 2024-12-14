from io import StringIO
import pandas as pd

if __name__ == "__main__":
    # archivos de entrada y salida
    input_file = "GRD_PUBLICO_EXTERNO_2022_limpio.txt"
    output_file = "GRD_PUBLICO_EXTERNO_2022.parquet"

    # número de campos
    expected_fields = 129

    # columnas a eliminar
    columns_to_remove = [
        "CIP_ENCRIPTADO", "SEXO", "ETNIA", "PROVINCIA", "COMUNA", "NACIONALIDAD", "PREVISION", "SERVICIO_SALUD",
        "TIPO_PROCEDENCIA", "TIPO_INGRESO", "FECHA_INGRESO", "FECHAALTA", "SERVICIOALTA", "TIPOALTA", "FECHATRASLADO1",
        "SERVICIOTRASLADO1", "FECHATRASLADO2", "SERVICIOTRASLADO2", "FECHATRASLADO3", "SERVICIOTRASLADO3",
        "FECHATRASLADO4", "SERVICIOTRASLADO4", "FECHATRASLADO5", "SERVICIOTRASLADO5", "FECHATRASLADO6",
        "SERVICIOTRASLADO6", "FECHATRASLADO7", "SERVICIOTRASLADO7", "FECHATRASLADO8", "SERVICIOTRASLADO8",
        "FECHATRASLADO9", "SERVICIOTRASLADO9", "CONDICIONDEALTANEONATO1", "PESORN1", "SEXORN1", "RN1ESTADO",
        "CONDICIONDEALTANEONATO2", "PESORN2", "SEXORN2", "RN2ESTADO", "CONDICIONDEALTANEONATO3", "PESORN3",
        "SEXORN3", "RN3ESTADO", "CONDICIONDEALTANEONATO4", "PESORN4", "SEXORN4", "RN4ESTADO", "MEDICOINTERV1_ENCRIPTADO",
        "FECHAPROCEDIMIENTO1", "FECHAINTERV1", "MEDICOALTA_ENCRIPTADO", "USOSPABELLON", "IR_29301_COD_GRD", "HOSPPROCEDENCIA",
        "PROCEDIMIENTO1", "PROCEDIMIENTO2", "PROCEDIMIENTO3", "PROCEDIMIENTO4", "PROCEDIMIENTO5", "PROCEDIMIENTO6",
        "PROCEDIMIENTO7", "PROCEDIMIENTO8", "PROCEDIMIENTO9", "PROCEDIMIENTO10", "PROCEDIMIENTO11", "PROCEDIMIENTO12",
        "PROCEDIMIENTO13", "PROCEDIMIENTO14", "PROCEDIMIENTO15", "PROCEDIMIENTO16", "PROCEDIMIENTO17", "PROCEDIMIENTO18",
        "PROCEDIMIENTO19", "PROCEDIMIENTO20", "PROCEDIMIENTO21", "PROCEDIMIENTO22", "PROCEDIMIENTO23", "PROCEDIMIENTO24",
        "PROCEDIMIENTO25", "PROCEDIMIENTO26", "PROCEDIMIENTO27", "PROCEDIMIENTO28", "PROCEDIMIENTO29", "PROCEDIMIENTO30"
    ]
    # columnas eliminadas decididas por equipo medico

    # Lee archivo línea por línea y filtra las líneas con campos adicionales
    valid_lines = []
    with open(input_file, "r", encoding="ISO-8859-1") as file:
        header = file.readline().strip()  # Lee línea de encabezado
        valid_lines.append(header)

        for line in file:
            fields = line.strip().split("|")
            if len(fields) == expected_fields:
                valid_lines.append(line.strip())

    # Une líneas válidas
    valid_data = "\n".join(valid_lines)

    # Lee los datos en un DataFrame de pandas
    df = pd.read_csv(StringIO(valid_data), delimiter="|", encoding="ISO-8859-1")

    # Filtra líneas que no tienen el valor "URGENCIA" debido a enfoque a antencion de urgencias
    df_filtered = df[df['TIPO_INGRESO'] == 'URGENCIA']

    # Elimina columnas
    df_filtered = df_filtered.drop(columns=columns_to_remove)

    # Filtra líneas que contienen "DESCONOCIDO" en las columnas IR_29301_MORTALIDAD o IR_29301_SEVERIDAD debido a dato inutilizable
    df_filtered = df_filtered[~df_filtered['IR_29301_MORTALIDAD'].str.contains('DESCONOCIDO', na=False)]
    df_filtered = df_filtered[~df_filtered['IR_29301_SEVERIDAD'].str.contains('DESCONOCIDO', na=False)]

    #DataFrame a archivo Parquet
    df_filtered.astype(str).to_parquet(output_file, engine="pyarrow")  # o usar engine="fastparquet" si es necesario