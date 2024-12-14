import pandas as pd
import xgboost as xgb
from sklearn.metrics import precision_score, recall_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

#NO FUNCIONA!!
#de felipe serey

# Cargar el modelo XGBoost entrenado
# Aquí asumimos que el modelo se ha guardado previamente en un archivo .json o .model
model = xgb.Booster()
model.load_model('model_mortalidad.bin')  # Cambia 'modelo_xgboost.model' por la ruta de tu modelo
# Cargar los datos
data = pd.read_parquet('GRD_PUBLICO_EXTERNO_2022.parquet')

# Definir X y y
X = data.drop(['IR_29301_PESO', 'IR_29301_SEVERIDAD', 'IR_29301_MORTALIDAD', "ÿþCOD_HOSPITAL"], axis=1)
y_severidad = data['IR_29301_SEVERIDAD']
y_mortalidad = data['IR_29301_MORTALIDAD']

# Convert categorical columns to category type
X = X.apply(lambda x: x.astype('category') if x.dtype == 'object' else x)

# Encode target variables to integers
label_encoder_severidad = LabelEncoder()
label_encoder_mortalidad = LabelEncoder()

y_severidad_encoded = label_encoder_severidad.fit_transform(y_severidad)
y_mortalidad_encoded = label_encoder_mortalidad.fit_transform(y_mortalidad)

# Dividir en entrenamiento y prueba
X_train_severidad, X_test_severidad, y_train_severidad, y_test_severidad = train_test_split(X, y_severidad_encoded, test_size=0.2, random_state=42)
X_train_mortalidad, X_test_mortalidad, y_train_mortalidad, y_test_mortalidad = train_test_split(X, y_mortalidad_encoded, test_size=0.2, random_state=42)

# Convertir los datos de prueba a un formato DMatrix (requerido por XGBoost)
dtest = xgb.DMatrix(X_test_mortalidad, enable_categorical=True)

# Realizar predicciones con el modelo
y_pred = model.predict(dtest)

# Convertir las predicciones a clases si es un problema de clasificación
# (por ejemplo, si es binario, redondear las predicciones)
if len(y_pred.shape) > 1 and y_pred.shape[1] > 1:
    # Para clasificación multiclase
    y_pred_classes = y_pred.argmax(axis=1)
else:
    # Para clasificación binaria o regresión
    y_pred_classes = (y_pred > 0.5).astype(int)  # Ajusta el umbral si es necesario

# Calcular métricas
if len(set( y_test_mortalidad)) > 2:  # Si es clasificación multiclase
    precision = precision_score( y_test_mortalidad, y_pred_classes, average='weighted')
    recall = recall_score( y_test_mortalidad, y_pred_classes, average='weighted')
else:  # Si es clasificación binaria
    precision = precision_score( y_test_mortalidad, y_pred_classes)
    recall = recall_score( y_test_mortalidad, y_pred_classes)

# Calcular el error cuadrático medio (MSE)
mse = mean_squared_error(y_test_mortalidad, y_pred)

# Imprimir las métricas
print(f"Precisión (Precision): {precision}")
print(f"Recall: {recall}")
print(f"Error Cuadrático Medio (MSE): {mse}")