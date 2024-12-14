from flask import Flask, request, jsonify, render_template
import pandas as pd
import ProbarModelo
from CargaModelos import load_severidad_model, load_mortalidad_model

modelo1 = load_severidad_model()
modelo2 = load_mortalidad_model()

app = Flask(__name__)

# Inputs:
features = ['FECHA_NACIMIENTO', 'ESPECIALIDAD_MEDICA', 'TIPO_ACTIVIDAD',
            'SERVICIOINGRESO', 'DIAGNOSTICO1', 'DIAGNOSTICO2', 'DIAGNOSTICO3',
            'DIAGNOSTICO4', 'DIAGNOSTICO5', 'DIAGNOSTICO6', 'DIAGNOSTICO7',
            'DIAGNOSTICO8', 'DIAGNOSTICO9', 'DIAGNOSTICO10', 'DIAGNOSTICO11',
            'DIAGNOSTICO12', 'DIAGNOSTICO13', 'DIAGNOSTICO14', 'DIAGNOSTICO15',
            'DIAGNOSTICO16', 'DIAGNOSTICO17', 'DIAGNOSTICO18', 'DIAGNOSTICO19',
            'DIAGNOSTICO20', 'DIAGNOSTICO21', 'DIAGNOSTICO22', 'DIAGNOSTICO23',
            'DIAGNOSTICO24', 'DIAGNOSTICO25', 'DIAGNOSTICO26', 'DIAGNOSTICO27',
            'DIAGNOSTICO28', 'DIAGNOSTICO29', 'DIAGNOSTICO30', 'DIAGNOSTICO31',
            'DIAGNOSTICO32', 'DIAGNOSTICO33', 'DIAGNOSTICO34', 'DIAGNOSTICO35',
            'ESPECIALIDADINTERVENCION']

# lee Excel file y extrae "Descripción" y "Código"
cie10_df = pd.read_excel('cie-10.xlsx')
cie10_options = cie10_df[['Descripción', 'Código']].to_dict('records')


@app.route('/')
def home():
    return render_template('index.html', cie10_options=cie10_options)


@app.route('/predict_severidad', methods=['POST'])
def predict_severidad():
    data = request.json
    print(f"data recivida:\n{data}")
    input_data = pd.DataFrame([data], columns=features)
    input_data = input_data.apply(lambda x: x.astype('category') if x.dtype == 'object' else x)
    print(f"fdata procesada:\n{input_data}")
    prediction = ProbarModelo.predict(input_data, modelo1)
    print(f"Prediccion generada:\n{prediction}")

    # predicciones a porcentajes para mayor legibilidad e interpretacion de los datos
    prediction_percentages = [(1 - pred) * 100 for pred in prediction[0]]
    prediction_percentages_str = [f"{percentage:.2f}%" for percentage in prediction_percentages]

    return jsonify({'prediction': prediction_percentages_str})


@app.route('/predict_mortalidad', methods=['POST'])
def predict_mortalidad():
    data = request.json
    print(f"data recivida:\n{data}")
    input_data = pd.DataFrame([data], columns=features)
    input_data = input_data.apply(lambda x: x.astype('category') if x.dtype == 'object' else x)
    print(f"fdata procesada:\n{input_data}")
    prediction = ProbarModelo.predict(input_data, modelo2)
    print(f"Prediccion generada:\n{prediction}")

    # predicciones a porcentajes para mayor legibilidad e interpretacion de los datos
    prediction_percentages = [(1 - pred) * 100 for pred in prediction[0]]
    prediction_percentages_str = [f"{percentage:.2f}%" for percentage in prediction_percentages]

    return jsonify({'prediction': prediction_percentages_str})


if __name__ == '__main__':
    app.run(debug=True)