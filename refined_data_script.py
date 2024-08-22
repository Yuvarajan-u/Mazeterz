import pandas as pd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error

department_seats = {'DWA': 197, 'TIS': 75, 'PTL': 201, 'OOC': 157, 'MOP': 125,'CHS': 96, 'CES': 172, 'SAI': 200, 'CGR': 196, 'CRR': 82, 'RCB': 200}

df = pd.read_csv('final_data.csv')

numeric_columns = df.select_dtypes(include=['number'])
skewness = numeric_columns.skew()


department_agg = df.groupby('Department Name').sum()
department_agg.reset_index(inplace=True)
department_agg.columns
department_agg=department_agg.drop('Employee', axis=1)
print(department_agg)

df_columns = ['week-day',department_agg['Department Name'][0], department_agg['Department Name'][1], department_agg['Department Name'][2], department_agg['Department Name'][3], department_agg['Department Name'][4], department_agg['Department Name'][5]]
data = []
for col in department_agg.columns:
    if(col != 'Department Name'):
        temp_list = [col, department_agg[col][0], department_agg[col][1], department_agg[col][2], department_agg[col][3], department_agg[col][4], department_agg[col][5]]
        data.append(temp_list)

df = pd.DataFrame(data)
df.columns = ['week-day',department_agg['Department Name'][0], department_agg['Department Name'][1], department_agg['Department Name'][2], department_agg['Department Name'][3], department_agg['Department Name'][4], department_agg['Department Name'][5]]

def find_list(dept):
  required_data = department_agg[department_agg['Department Name']== dept]
  res = {'_Monday': [], '_Tuesday':[],'_Wednesday':[],'_Thursday':[], '_Friday':[]}

  for col in required_data.columns:
    if '_' in col:
      a = col[col.find('_'): ]
      res[a].extend(required_data[col])
  print(len(res['_Friday']))
  return res

def seat_availability(day):
    avil_dept = ['CRR', 'DWA', 'MOP', 'PTL']
    result = {}
    for i in avil_dept:
        dept_day_list = find_list(i)[f'_{day}']
        dept_seat = department_seats[i]
        dept_day_list = [x if x<dept_seat else 0 for x in dept_day_list]
        dept_day_list_available = [dept_seat-x if x > 0 else 0 for x in dept_day_list]

        train, test = dept_day_list_available[:45], dept_day_list_available[45:]

        # Fit ARIMA model
        model = ARIMA(train, order=(3,1,1))
        model_fit = model.fit()

        # Make predictions
        predictions = model_fit.forecast(steps=len(test))
        actual_values = np.array(test)

        print("Predicted seat availability:", predictions)

        mae = mean_absolute_error(actual_values, predictions)

        print(f'Accuracy: {100-mae}')
        result[i] = predictions[0]
    return result

