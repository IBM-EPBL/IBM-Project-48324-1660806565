{
  "metadata": {
    "language_info": {
      "codemirror_mode": {
        "name": "python",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8"
    },
    "kernelspec": {
      "name": "python",
      "display_name": "Python (Pyodide)",
      "language": "python"
    }
  },
  "nbformat_minor": 4,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "code",
      "source": "import numpy as np\nfrom flask import Flask, request, jsonify, render_template\nimport joblib\nimport requests",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "app = Flask(__name__)\nmodel = joblib.load(\"power_prediction.sav\")",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "@app.route('/windapi',methods=['POST'])\ndef windapi():\n    city=request.form.get('city')\n    apikey=\"d377e14318fb678ccad77358918c544f\"\n    url=\"http://api.openweathermap.org/data/2.5/weather?q=\"+city+\"&appid=\"+apikey\n    resp = requests.get(url)\n    resp=resp.json()\n    temp = str(resp[\"main\"][\"temp\"])+\" °C\"\n    humid = str(resp[\"main\"][\"humidity\"])+\" %\"\n    pressure = str(resp[\"main\"][\"pressure\"])+\" mmHG\"\n    speed = str(resp[\"wind\"][\"speed\"])+\" m/s\"\n    return render_template('predict.html', temp=temp, humid=humid, pressure=pressure,speed=speed)",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "@app.route('/')\ndef home():\n    return render_template('intro.html')",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "@app.route('/predict')\ndef predict():\n    return render_template('predict.html')",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "@app.route('/y_predict',methods=['POST'])\ndef y_predict():",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "For rendering results on HTML GUI\n    '''\n    x_test = [[float(x) for x in request.form.values()]]",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "prediction = model.predict(x_test)\n    print(prediction)\n    output=prediction[0]\n    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "if __name__ == \"__main__\":\n    app.run(debug=True)",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "",
      "metadata": {},
      "execution_count": null,
      "outputs": []
    }
  ]
}