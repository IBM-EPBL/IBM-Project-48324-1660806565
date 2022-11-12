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
      "source": "#%%\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pylab as plt\nimport os\n\nos.chdir(\"/home/skystone/Documents/TimeSeries\")\ndf = pd.read_csv('T1.csv', delimiter=',')\n\n#%%\n\ndataset = df[['Date/Time','Wind Speed (m/s)']]\ndataset = dataset.rename(columns = {\"Date/Time\" :\"timeStamp\",\"Wind Speed (m/s)\":\"windSpeed\"})\ndataset = dataset[:5000]\n\n# MISSING DATA POINTS\n# 2018-01-26 06:20:00  to  2018-01-30 14:40:00\n# 2018-09-28 21:20:00  to  2018-10-02 16:30:00\n# 2018-11-10 21:10:00  to  2018-11-14 12:00:00\n\nnewTime = []\nfor i in dataset['timeStamp']:\n    # YYYY-MM-DD HH:MM:SS   => Required\n    # DD MM YYYY HH:MM      => my format\n    #print(\"{0}-{1}-{2} {3}:00\".format(i[6:10],i[3:5],i[:2],i[11:16]))\n    newTime.append(i[6:10] + \"-\" + i[3:5] + \"-\" + i[:2] + \" \" + i[11:16] + \":00\")\ndataset['timeStamp'] = newTime\n\n\n#%%\n\ndataset.index = pd.to_datetime(dataset.timeStamp)\n# dataset.index = pd.DatetimeIndex(dataset.index).to_period('H')\ndataset.index = pd.DatetimeIndex(dataset.index)\ndataset = dataset.drop('timeStamp', axis=1)\n\ndataset.plot()\n\ndataset = dataset.sort_index()\ndataset.fillna(df.mean())\n\n#%%\n\n# Testing whether there are null values\ndataset[dataset.isnull()]\nlen(dataset[dataset.isnull()])\ndataset = dataset.sort_index()\ndataset.index\n\n#%%\n\n# Replacing NaN values with the previous effective data\ndataset.windSpeed.fillna(method='pad', inplace=True)\ndataset[dataset.windSpeed.isnull()]\n\ndataset.describe()\n\n#%%\n\ndataset['Ticks'] = range(0,len(dataset.index.values))\n#dataset = dataset.drop('Ticks', axis=1)\n\n#very simple plotting\nfig = plt.figure(1)\nax1 = fig.add_subplot(111)\nax1.set_xlabel('Ticks')\nax1.set_ylabel('windSpeed')\nax1.set_title('Original Plot')\nax1.plot('Ticks', 'windSpeed', data = dataset);\n\n#%%\n\nfrom statsmodels.tsa.stattools import adfuller\ndef stationarity_check(ts):    \n    # Determing rolling statistics\n    #roll_mean = pd.rolling_mean(ts, window=12)\n    roll_mean = ts.rolling(12).mean()\n    \n    # Plot rolling statistics:\n    plt.plot(ts, color='green',label='Original')\n    plt.plot(roll_mean, color='blue', label='Rolling Mean')\n    plt.legend(loc='best')\n    plt.title('Rolling Mean')\n    plt.show(block=False)\n    \n    # Perform Augmented Dickey-Fuller test:\n    print('Augmented Dickey-Fuller test:')\n    df_test = adfuller(ts)\n    print(\"type of df_test: \",type(df_test))\n    print(\"df_test: \",df_test)\n    df_output = pd.Series(df_test[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])\n    print(\"df_output: \\n\",df_output)\n    for key,value in df_test[4].items():\n        df_output['Critical Value (%s)'%key] = value\n    print(df_output)\n    \nstationarity_check(dataset.windSpeed)\n\n#%%\n\n#dfIndia['Roll_Mean'] = pd.rolling_mean(dfIndia.AverageTemperature, window=12)\ndataset['Roll_Mean'] = dataset.windSpeed.rolling(12).mean()\ndataset.windSpeed.rolling(12)\n\nfrom statsmodels.graphics.tsaplots import plot_pacf,plot_acf\nplot_acf(dataset.windSpeed, lags=50)\nplot_pacf(dataset.windSpeed, lags=50)\nplt.xlabel('lags')\nplt.show()\n\n#%%\n\nfrom statsmodels.tsa.arima_model import ARMA\n\nimport itertools\np = q = range(0, 4)\npq = itertools.product(p, q)\nfor param in pq:\n    try:\n        mod = ARMA(dataset.windSpeed,order=param)\n        results = mod.fit()\n        print('ARMA{} - AIC:{}'.format(param, results.aic))\n    except:\n        continue\n    \nmodel = ARMA(dataset.windSpeed, order=(3,3))  \nresults_MA = model.fit(method=\"css-mle\")  \n\n#%%\n\nplt.plot(dataset.windSpeed)\nplt.plot(results_MA.fittedvalues, color='red')\nplt.title('Fitting data _ MSE: %.2f'% (((results_MA.fittedvalues-dataset.windSpeed)**2).mean()))\nplt.show()\n\n#%%\n#Check\n\nfrom pandas.tseries.offsets import DateOffset\nfuture_dates=[dataset.index[-1]+ DateOffset(months=x)for x in range(0,24)]\n\nfuture_datest_df=pd.DataFrame(index=future_dates[1:],columns=dataset.columns)\n\nfuture_datest_df.tail()\n\nfuture_df=pd.concat([dataset,future_datest_df])\n\n# future_df['forecast'] = results_MA.predict(start = 104, end = 120, dynamic= True)\nfuture_df['forecast'] = results_MA.predict('2019-10-09')  \n#future_df[['Sales', 'forecast']].plot(figsize=(12, 8))\n\n#%%\n\n#predictions = results_MA.predict('2018-03-02 18:50:00')\npredictions = results_MA.predict('4000')\npredictions\n\n#%%\n\nfrom sklearn.externals import joblib \njoblib.dump(results_MA, 'humidityModel.pkl') ",
      "metadata": {},
      "execution_count": null,
      "outputs": []
    }
  ]
}