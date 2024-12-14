import xgboost as xgb

def load_severidad_model():
    """
    carga el modelo severidad de XGBoost de el archivo guardado.

    :return: modelo XGBoost.
    """
    model = xgb.Booster()
    print("Cargando Modelo de Severidad")
    model.load_model('model_severidad.bin')
    print("Modelo Cargado")
    return model

def load_mortalidad_model():
    """
    carga el modelo mortalidad de XGBoost de el archivo guardado.

    :return: modelo XGBoost.
    """
    model = xgb.Booster()
    print("Cargando Modelo de Mortalidad")
    model.load_model('model_mortalidad.bin')
    print("Modelo Cargado")
    return model