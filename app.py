from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        department_name = request.form['department']
        today = datetime.datetime.now().strftime('%A')

        # Example result for the current day
        result = {
            'Friday': {'DWA': 1, 'PTL': 5, 'CRR': 3, 'MOP': 0}
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

        if today in result:
            value = result[today]
            if value.get(department_name, 0) > 2:
                prediction["success"] = "You can find a seat in your own bay"
            else:
                for dept, probability in value.items():
                    if dept != department_name:
                        failure_lambda[dept] = float(probability / department_seats.get(dept))
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
