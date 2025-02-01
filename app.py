from flask import Flask, request, render_template
import sqlite3
import re
from datetime import datetime

app = Flask(__name__)

def parse_query(user_input):
    # Regex patterns for flexible query parsing
    patterns = {
        r'(show|list|display).*employees.* (.*) department': ('employees_by_dept', 2),
        r'(who is|who\'s|who).*manager.* (.*) department': ('manager_of_dept', 2),
        r'(list|show).*employees hired after (.*)': ('employees_hired_after', 2),
        r'(total|sum).*salary.* (.*) department': ('total_salary_dept', 2)
    }

    user_input = user_input.lower().strip()
    for pattern, (func, group_num) in patterns.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            param = match.group(group_num).strip()
            return func, param
    return None, None

def get_valid_departments(cursor):
    # Fetch all valid department names from the database
    cursor.execute('SELECT Name FROM Departments')
    return [row[0] for row in cursor.fetchall()]

def execute_sql(func, param):
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    
    try:
        if func == 'employees_by_dept':
            # Check if department exists
            cursor.execute('SELECT Name FROM Departments WHERE LOWER(Name) = LOWER(?)', (param,))
            if not cursor.fetchone():
                valid_depts = get_valid_departments(cursor)
                return f"Department '{param}' not found. Valid departments: {', '.join(valid_depts)}."
            
            # Fetch employees
            cursor.execute('''
                SELECT Name, Department, Hire_Date 
                FROM Employees 
                WHERE LOWER(Department) = LOWER(?)
            ''', (param,))
            results = cursor.fetchall()
            if not results:
                return f"No employees found in the '{param}' department."
            return "\n".join([f"• {row[0]} ({row[1]}, hired {row[2]})" for row in results])
        
        elif func == 'manager_of_dept':
            cursor.execute('SELECT Manager FROM Departments WHERE LOWER(Name) = LOWER(?)', (param,))
            result = cursor.fetchone()
            if result:
                return f"Manager of {param}: {result[0]}"
            else:
                valid_depts = get_valid_departments(cursor)
                return f"Department '{param}' not found. Valid departments: {', '.join(valid_depts)}."
        
        elif func == 'employees_hired_after':
            # Validate date format
            try:
                datetime.strptime(param, '%Y-%m-%d')
                cursor.execute('''
                    SELECT Name, Department, Hire_Date 
                    FROM Employees 
                    WHERE Hire_Date > ?
                ''', (param,))
                results = cursor.fetchall()
                if not results:
                    return f"No employees hired after {param}."
                return "\n".join([f"• {row[0]} ({row[1]}, hired {row[2]})" for row in results])
            except ValueError:
                return "Invalid date format. Use YYYY-MM-DD."
        
        elif func == 'total_salary_dept':
            # Check if department exists
            cursor.execute('SELECT Name FROM Departments WHERE LOWER(Name) = LOWER(?)', (param,))
            if not cursor.fetchone():
                valid_depts = get_valid_departments(cursor)
                return f"Department '{param}' not found. Valid departments: {', '.join(valid_depts)}."
            
            # Calculate total salary
            cursor.execute('SELECT SUM(Salary) FROM Employees WHERE LOWER(Department) = LOWER(?)', (param,))
            total = cursor.fetchone()[0]
            return f"Total salary expense for {param}: ${total:,}"

    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    finally:
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def chat_assistant():
    response = None
    if request.method == 'POST':
        user_input = request.form.get('query', '').strip()
        if not user_input:
            response = "Please enter a query."
        else:
            func, param = parse_query(user_input)
            if func and param:
                response = execute_sql(func, param)
            else:
                response = '''Sorry, I couldn't understand your query. Supported queries:
                    <ul>
                        <li>"Show employees in [department] department"</li>
                        <li>"Who is the manager of [department] department?"</li>
                        <li>"List employees hired after [date]"</li>
                        <li>"Total salary expense for [department] department"</li>
                    </ul>'''
    
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
