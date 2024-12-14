#LIMPIA CHARACTERES NULOS DE BASE DE DATOS DE GRD FONASA
def remove_null_characters(input_file, output_file):
    """
    Limpia characteres nulos de un archivo y guarda resultados en otro archivo

    :param input_file: archivo de ingreso
    :param output_file: archivo de salida
    """
    # Lee el archivo TXT
    with open(input_file, 'r', encoding='iso-8859-1') as file:
        content = file.read()

    # Reemplaza todas las instancias de \x00 con una cadena vacía
    cleaned_content = content.replace('\x00', '')

    # Escribe el contenido modificado en un nuevo archivo TXT
    with open(output_file, 'w', encoding='iso-8859-1') as file:
        file.write(cleaned_content)

    print(f"Caracteres nulos eliminados del archivo '{input_file}'. Resultado guardado en '{output_file}'.")

# Uso del script
input_file = 'GRD_PUBLICO_EXTERNO_2022.txt'
output_file = 'GRD_PUBLICO_EXTERNO_2022_limpio.txt'

remove_null_characters(input_file, output_file)