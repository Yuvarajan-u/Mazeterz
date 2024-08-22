from flask import Flask, render_template, request, jsonify
import datetime
from source.model import seat_availability

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        department_name = request.form['department']
        today = datetime.datetime.now().strftime('%A')
        result = seat_availability(today)
        # sai and tsi need to be removed
        result = {
            'Monday': {'DWA': 7, 'PTL': 5, 'CRR': 3, 'MOP': 0}
        }
        department_seats = {
            'DWA': 197, 
            'PTL': 201,  
            'MOP': 96,  
            'CRR': 82 
        }
        prediction = {}
        failure_lambda = {}
        sorted_departments = {}
        for day, value in result.items():
            if day == today:
                if value.get(department_name) >2:
                    prediction["success"] = "you can find seat in your own bay"
                else:
                    for dept, probability in value.items():
                        if (dept == department_name):
                            continue
                        else:
                            failure_lambda["dept"] = float(probability / department_seats.get(dept))      
                    sorted_departments = sort_departments_by_value(failure_lambda)
                    prediction["failure"] = sorted_departments

        return jsonify(department=department_name, result=prediction)
    return render_template('index.html')

def sort_departments_by_value(department_dict):
    # Sort the dictionary by values
    sorted_departments = dict(sorted(department_dict.items(), key=lambda item: item[1]))
    return sorted_departments


if __name__ == '__main__':
    app.run(debug=True)
