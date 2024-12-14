Este segemneto desarrolla un nuevo método para la interpretación de datos en la Inteligencia Artificiall.
La base de datos
utilizada contiene información sobre diagnósticos de pacientes, donde cada diagnóstico representa una 
enfermedad o condición médica

# Problema

la IA no puede distinguir entre diagnósticos 
que representan la misma enfermedad en diferentes columnas (por ejemplo, `DIAGNOSTICO1` vs `DIAGNOSTICO2`), 
lo que genera resultados inconsistentes.

# Solucion

Desarrollar un nuevo método que permita a la IA interpretar correctamente los diagnósticos, 
independientemente de la columna en la que aparezcan. Para lograr esto, se propone
que cada enfermedad o condición médica se represente en su propia columna, 
eliminando así la confusión entre diagnósticos.

# Resultado

este proceso generará más de 1900 columnas adicionales lo cual presenta dificultad a la hora de generar el 
archivo de entrenamiento

Se han desarrollado varios scripts en Python para implementar este nuevo método. 

- **`CRDfiltroexcel.py`**: Versión inicial que utiliza el módulo `csv` para procesar los datos. no funcional
- **`CRDfiltroexcelVer3.py`**: 3ra Versión, continuada por lo que ahora mimso es la actual. aun presenta problemas
- **`CRDfiltroexcelVer4.py`**: cuarta version no funcional

debido a errores de codificacion y el largo tiempo de procesamiento se rechaza la propuesta temporalmente,
revisitar en algun momento

-Ricardo merino