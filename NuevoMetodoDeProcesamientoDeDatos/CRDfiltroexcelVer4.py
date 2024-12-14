
import shutil
import csv

if __name__ == "__main__":
    # Leer el archivo original
    input_file = '../GRD_PUBLICO_EXTERNO_2022_mini.txt'
    output_file = input_file  # El archivo de salida será el mismo archivo de entrada

    # Lista para almacenar los síntomas únicos (solo la parte antes del punto)
    sintomas_unicos = set()

    # Leer el archivo original y extraer los síntomas, ignorando los casos "DESCONOCIDO"
    with open(input_file, mode='r', newline='') as file:
        reader = csv.DictReader(file, delimiter='|')
        for row_num, row in enumerate(reader, start=1):
            print(f"Leyendo fila {row_num}: {row['COD_HOSPITAL']}")  # Mostrar la fila actual
            # Extraer solo las columnas de diagnósticos
            for key in row.keys():
                if key.startswith('DIAGNOSTICO') and row[key] and row[key] != "DESCONOCIDO":
                    diagnostico = row[key]
                    # Tomar solo la parte antes del punto
                    sintoma_sin_punto = diagnostico.split('.')[0]
                    sintomas_unicos.add(sintoma_sin_punto)

    # Convertir el conjunto de síntomas únicos en una lista y ordenarla
    sintomas_unicos = sorted(list(sintomas_unicos))

    # Crear un archivo temporal para almacenar los resultados
    temp_file = 'temp_output.csv'

    # Crear el archivo temporal con los resultados
    try:
        with open(input_file, mode='r', newline='') as infile, open(temp_file, mode='w', newline='') as outfile:
            reader = csv.DictReader(infile, delimiter='|')
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames + sintomas_unicos, delimiter='|')

            # Escribir la cabecera original y las nuevas columnas
            writer.writeheader()

            # Procesar cada fila del archivo original
            for row_num, row in enumerate(reader, start=1):
                print(f"Procesando fila {row_num}: {row['COD_HOSPITAL']}")  # Mostrar la fila actual
                cod_hospital = row['COD_HOSPITAL']
                nuevo_registro = {key: row[key] for key in reader.fieldnames}  # Copiar las columnas originales

                # Procesar cada síntoma único
                for sintoma in sintomas_unicos:
                    for key in row.keys():
                        if key.startswith('DIAGNOSTICO') and row[key] and row[key] != "DESCONOCIDO":
                            diagnostico = row[key]
                            if diagnostico.startswith(sintoma):
                                if '.' in diagnostico:
                                    # Escribir el número después del punto
                                    nuevo_registro[sintoma] = diagnostico.split('.')[1]
                                else:
                                    # Escribir -1 si no hay punto
                                    nuevo_registro[sintoma] = '-1'
                                break  # Salir del bucle una vez que se encuentra el síntoma
                    else:
                        # Si no se encuentra el síntoma, no se escribe nada
                        nuevo_registro[sintoma] = ''

                # Escribir la fila procesada
                writer.writerow(nuevo_registro)

    except Exception as e:
        print(f"Se produjo un error durante la escritura: {e}")
        print("Guardando el archivo temporal con los datos procesados hasta ahora...")
        # No se realiza el reemplazo del archivo original si hay un error
        shutil.move(temp_file, output_file)
        print(f"Archivo '{output_file}' parcialmente actualizado debido al error.")
    else:
        # Si no hay errores, reemplazar el archivo original con el archivo temporal
        shutil.move(temp_file, output_file)
        print(f"Archivo '{output_file}' actualizado exitosamente.")