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
      "source": "import numpy as np \nimport pandas as pd \nimport joblib\n",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "loaded_model = joblib.load('power_prediction.sav')",
      "metadata": {
        "trusted": true
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "#X = [['Theoretical_Power_Curve (KWh)','WindSpeed(m/s)']]\nprint(loaded_model.predict([[416.328907824861,5.31133604049682]])[0],\"KWh\")\n\n#predicted value is ['ActivePower(kW)']\n",
      "metadata": {},
      "execution_count": null,
      "outputs": []
    }
  ]
}