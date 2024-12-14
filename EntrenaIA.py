import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Carga datos
data = pd.read_parquet('GRD_PUBLICO_EXTERNO_2022.parquet')

#X y y
X = data.drop(['IR_29301_PESO', 'IR_29301_SEVERIDAD', 'IR_29301_MORTALIDAD', "ÿþCOD_HOSPITAL"], axis=1)
y_severidad = data['IR_29301_SEVERIDAD']
y_mortalidad = data['IR_29301_MORTALIDAD']

# Convierte columnas categoricas a category type
X = X.apply(lambda x: x.astype('category') if x.dtype == 'object' else x)

#variables de destino en números enteros
label_encoder_severidad = LabelEncoder()
label_encoder_mortalidad = LabelEncoder()

y_severidad_encoded = label_encoder_severidad.fit_transform(y_severidad)
y_mortalidad_encoded = label_encoder_mortalidad.fit_transform(y_mortalidad)

# Divide a entrenamiento y prueba
X_train_severidad, X_test_severidad, y_train_severidad, y_test_severidad = train_test_split(X, y_severidad_encoded, test_size=0.2, random_state=42)
X_train_mortalidad, X_test_mortalidad, y_train_mortalidad, y_test_mortalidad = train_test_split(X, y_mortalidad_encoded, test_size=0.2, random_state=42)

#probar setting diferentes y compartir resultados en chat del equipo
#n_estimator 5000 tiende a llegar a 1 en validation_0_auc consistentemente. 500 tambien mantiene un numero alto, en un tiempo dramaticamente menor
model_xgboost = xgb.XGBClassifier(learning_rate=0.1,
                                  max_depth=5,
                                  n_estimators=500,
                                  subsample=0.5,
                                  colsample_bytree=0.5,
                                  eval_metric='auc',
                                  verbosity=1,
                                  tree_method="hist",
                                  enable_categorical=True,
                                  device="cuda")

eval_set = [(X_train_severidad, y_train_severidad)]

# entrena severidad
model_xgboost.fit(X_train_severidad,
                  y_train_severidad,
                  eval_set=eval_set,
                  verbose=True)

# guardar modelo
model_xgboost.save_model('model_severidad.bin')

# evaluar mse de Severidad
y_pred_severidad = model_xgboost.predict(X_test_severidad)
mse_severidad = mean_squared_error(y_test_severidad, y_pred_severidad)
print(f'MSE for Severidad: {mse_severidad}')

# entrena Mortalidad
model_xgboost.fit(X_train_mortalidad,
                  y_train_mortalidad,
                  eval_set=[(X_train_mortalidad, y_train_mortalidad)],
                  verbose=True)

# guarda modelo de Mortalidad
model_xgboost.save_model('model_mortalidad.bin')

# evalua modelo de Mortalidad (mse)
y_pred_mortalidad = model_xgboost.predict(X_test_mortalidad)
mse_mortalidad = mean_squared_error(y_test_mortalidad, y_pred_mortalidad)
print(f'MSE for Mortalidad: {mse_mortalidad}')

#preguntar a tomas (pelo) para que era este segmento:
"""
# Explicitly set the device for the booster before making predictions
model_xgboost._Booster.set_param({'predictor': 'gpu_predictor'})
"""

#antiguo:
"""
# Dividir las etiquetas individuales
y_train_peso = y_train.loc[:,"IR_29301_PESO"]
y_train_severidad = y_train.loc[:,"IR_29301_SEVERIDAD"]
y_train_mortalidad = y_train.loc[:,"IR_29301_MORTALIDAD"]

y_test_peso = y_test.loc[:,"IR_29301_PESO"]
y_test_severidad = y_test.loc[:,"IR_29301_SEVERIDAD"]
y_test_mortalidad = y_test.loc[:,"IR_29301_MORTALIDAD"]

# Crear DMatrix para cada una de las etiquetas
dtrain_peso = xgb.DMatrix(X_train, label=y_train_peso)
dtest_peso = xgb.DMatrix(X_test, label=y_test_peso)

dtrain_severidad = xgb.DMatrix(X_train, label=y_train_severidad)
dtest_severidad = xgb.DMatrix(X_test, label=y_test_severidad)

dtrain_mortalidad = xgb.DMatrix(X_train, label=y_train_mortalidad)
dtest_mortalidad = xgb.DMatrix(X_test, label=y_test_mortalidad)

# Redefinir los parámetros del modelo
params = {
    'objective': 'reg:squarederror',  # Regresión
    'max_depth': 6,
    'eta': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'seed': 42
}

# Entrenar los tres modelos
model_peso = xgb.train(params, dtrain_peso, num_boost_round=100)
model_severidad = xgb.train(params, dtrain_severidad, num_boost_round=100)
model_mortalidad = xgb.train(params, dtrain_mortalidad, num_boost_round=100)

# Realizar predicciones para cada modelo
y_pred_peso = model_peso.predict(dtest_peso)

y_pred_mortalidad = model_mortalidad.predict(dtest_mortalidad)

# Calcular el error cuadrático medio (MSE) para cada predicción
mse_peso = mean_squared_error(y_test_peso, y_pred_peso)
mse_severidad = mean_squared_error(y_test_severidad, y_pred_severidad)
mse_mortalidad = mean_squared_error(y_test_mortalidad, y_pred_mortalidad)

print(mse_peso)
print(mse_severidad)
print(mse_mortalidad)"""