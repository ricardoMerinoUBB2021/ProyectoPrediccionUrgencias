import csv

#convierte txt a tsv (como un archivo csv pero separado por | )

def txt_to_tsv(input_file, output_file):
    encodings_to_try = ['utf-8', 'iso-8859-1', 'windows-1252']
    
    for encoding in encodings_to_try:
        try:
            with open(input_file, 'r', encoding=encoding) as txt_file:
                lines = txt_file.readlines()
                encoding_used = encoding
                break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"No se pudo decodificar el archivo {encodings_to_try}")

    with open(output_file, 'w', newline='', encoding=encoding_used) as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t')
        headers = lines[0].strip().split('|')
        tsv_writer.writerow(headers)
        for line in lines[1:]:
            row = line.strip().split('|')
            tsv_writer.writerow(row)

    print(f"creado exitosamente '{encoding_used}'.")

input_file = 'GRD_PUBLICO_EXTERNO_2022.txt'
output_file = 'GRD_PUBLICO_EXTERNO_2022.tsv'

txt_to_tsv(input_file, output_file)