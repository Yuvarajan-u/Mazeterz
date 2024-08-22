import pandas as pd
import numpy as np

# Parameters
department_name = '' # Enter the department name
total_employees = None # enter total number of employee of that department
allocated_seats = None # enter allocated seats for the specific department
working_days_per_year = 251
working_days_per_month = working_days_per_year / 12
days_in_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
total_weeks = working_days_per_year // 5

# Ensure each employee goes to the office twice a week (8 days a month, 96 days a year)
days_required_per_year = 96

# Create an empty DataFrame to store the schedule
columns = [f"week{week}_{day}" for week in range(1, int(total_weeks)+1) for day in days_in_week]
schedule_df = pd.DataFrame(index=[f"emp{emp+1}" for emp in range(total_employees)], columns=columns)

# Function to assign days ensuring no more than allocated_seats are used
def assign_days(employee_idx):
    days_assigned = 0
    while days_assigned < days_required_per_year:
        week = np.random.randint(1, total_weeks+1)
        days = np.random.choice(days_in_week, 2, replace=False)
        
        for day in days:
            if days_assigned < days_required_per_year:
                week_day = f"week{week}_{day}"
                if schedule_df[week_day].count() < allocated_seats:
                    schedule_df.at[f"emp{employee_idx}", week_day] = 1
                    days_assigned += 1

# Generate schedule for each employee
for emp in range(1, total_employees + 1):
    assign_days(emp)

# Fill NaNs with 0 (indicating the employee is not going to the office on that day)
schedule_df.fillna(0, inplace=True)

# Convert the schedule DataFrame to integer type (1 for attending, 0 for not attending)
schedule_df = schedule_df.astype(int)

# Add the Department Name column
schedule_df.insert(0, 'Department Name', department_name)

# Save the generated schedule to a CSV file
output_file = 'Department_Schedule.csv'
schedule_df.to_csv(output_file, index_label='Employee')

print(f"Schedule generated and saved to {output_file}")
