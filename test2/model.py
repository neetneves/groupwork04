import pandas as pd
import numpy as np
from statsmodels.tsa.ar_model import AR
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("train_dataset.csv")
time_index = np.array(pd.to_datetime(df.iloc[:, 0]))
df.index = time_index
data = df.iloc[:, 1].astype("float")

# Split data set
train = np.array(data[:"2020-07-09"])


# Detrend and add trend
def detrend(data_series, degree):
    X = [x for x in range(len(data_series))]
    coef = np.polyfit(X, data_series, degree)
    trend = list()
    for i in range(len(data_series)):
        value = coef[-1]
        for d in range(degree):
            value += i ** (degree - d) * coef[d]
        trend.append(value)

    for i in range(len(data_series)):
        data_series[i] = data_series[i] - trend[i]

    return data_series, degree, coef


def addtrend(data_series, start, degree, coef):
    trend = list()
    for i in range(len(data_series)):
        value = coef[-1]
        for d in range(degree):
            value += (start + i) ** (degree - d) * coef[d]
        trend.append(value)

    for i in range(len(data_series)):
        data_series[i] = data_series[i] + trend[i]

    return data_series


train, trend_degree, trend_coef = detrend(train, 2)

# AR modeling
model = AR(train)
model_fit = model.fit()
predictions = model_fit.predict(start=len(train), end=len(train) + 16, dynamic=False)
predictions = addtrend(predictions, len(train) - 1, trend_degree, trend_coef)
print(predictions)

# Draw the figure
plt.plot([x for x in range(0, len(data[:"2020-07-09"]))], data[:"2020-07-09"].values,
         color="blue", label="Actual Values")
plt.plot([x for x in range(len(data[:"2020-07-09"]) + 1, len(data[:"2020-07-09"]) + 18)], predictions,
         color="red", label="Predicted Values")
plt.xlabel("Time (Monthly)")
plt.ylabel("Value")
plt.legend()
plt.show()
