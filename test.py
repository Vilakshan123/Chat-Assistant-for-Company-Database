import sqlite3

# Create and connect to the database
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Create Employees table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Department TEXT,
        Salary INTEGER,
        Hire_Date DATE
    )
''')

# Create Departments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Departments (
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Manager TEXT
    )
''')

# Insert sample data into Employees (using INSERT OR IGNORE to avoid duplicates)
employees = [
    (1, 'Alice', 'Sales', 50000, '2021-01-15'),
    (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
    (3, 'Charlie', 'Marketing', 60000, '2022-03-20')
]
cursor.executemany('INSERT OR IGNORE INTO Employees VALUES (?, ?, ?, ?, ?)', employees)

# Insert sample data into Departments (using INSERT OR IGNORE to avoid duplicates)
departments = [
    (1, 'Sales', 'Alice'),
    (2, 'Engineering', 'Bob'),
    (3, 'Marketing', 'Charlie')
]
cursor.executemany('INSERT OR IGNORE INTO Departments VALUES (?, ?, ?)', departments)

# Commit and close
conn.commit()
conn.close()
