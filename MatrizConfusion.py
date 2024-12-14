import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from CargaModelos import load_severidad_model, load_mortalidad_model

#CODIGO EXCLUSIVAMENTE PARA CREAR MATRIZES DE CONFUSION

if __name__ == '__main__':
    #cambiar manualmente el modelo, aqui. cambiar variables manualmente tambien
    modelo = load_severidad_model()

    # Carga datos
    data = pd.read_parquet('GRD_PUBLICO_EXTERNO_2022.parquet')

    # X y y
    X = data.drop(['IR_29301_PESO', 'IR_29301_SEVERIDAD', 'IR_29301_MORTALIDAD', "ÿþCOD_HOSPITAL"], axis=1)
    y_severidad = data['IR_29301_SEVERIDAD']
    y_mortalidad = data['IR_29301_MORTALIDAD']

    # Convierte columnas categoricas a category type
    X = X.apply(lambda x: x.astype('category') if x.dtype == 'object' else x)

    # variables de destino en números enteros
    label_encoder_severidad = LabelEncoder()
    label_encoder_mortalidad = LabelEncoder()

    y_severidad_encoded = label_encoder_severidad.fit_transform(y_severidad)
    y_mortalidad_encoded = label_encoder_mortalidad.fit_transform(y_mortalidad)

    # Divide a entrenamiento y prueba
    X_train_severidad, X_test_severidad, y_train_severidad, y_test_severidad = train_test_split(X, y_severidad_encoded, test_size=0.4, random_state=42)
    X_train_mortalidad, X_test_mortalidad, y_train_mortalidad, y_test_mortalidad = train_test_split(X, y_mortalidad_encoded, test_size=0.4, random_state=42)

    #generacion de la matriz
    X_test_mortalidad_dmatrix = xgb.DMatrix(X_test_severidad, enable_categorical=True)
    y_pred_mortalidad = modelo.predict(X_test_mortalidad_dmatrix)
    #debido a que Y puede tener 4 alternativas, para la matriz de confusion se toma el argmax puesto que este seria el dato mas probable a ser el caso del paciente
    #en la realidad segun el modelo
    y_pred_mortalidad_1d = np.argmax(y_pred_mortalidad, axis=1)
    cm = confusion_matrix(y_test_severidad, y_pred_mortalidad_1d)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.unique(y_test_severidad))
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Matriz de confusion modelo de severidad")
    plt.show()
