# Chat-Assistant-for-Company-Database

Welcome to the **Chat Assistant for Company Database**—a Python-based interactive assistant designed to respond to user queries by interacting with an SQLite database.

---

## 🌟 Features  
- Natural language query processing  
- Supports a variety of queries:
  - Show all employees in a department  
  - Retrieve the manager of a department  
  - List employees hired after a specific date  
  - Calculate the total salary expense of a department  
- Error handling for invalid inputs  
- Friendly and clear response formatting  

---

## 🚀 Getting Started  

### Prerequisites  
Ensure you have Python installed on your system.  

### Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/Chat-Assistant-for-Company-Database.git
2. Navigate to the project directory:

    cd Chat-Assistant-for-Company-Database
4. Install dependencies:

    pip install -r requirements.txt

## 🛡️ Error Handling
- Handles invalid department names
- Provides messages when no results are found
- Ensures input validation for date formats

## 🛠️ Database Initialization

 The project requires an SQLite database (company.db) for storing employee and department data.
 To set up the database, use the provided test.py file:
  #### What Happens in test.py
  - Ensure you have Python installed.
  - Inserts sample data into both tables:
    - Example employees: Alice (Sales), Bob (Engineering), Charlie (Marketing).
    - Example departments: Sales, Engineering, Marketing.

   #### Important Note

If company.db already exists, running test.py will not overwrite it but may insert duplicate records. Delete the company.db file before rerunning if you want a fresh database setup.


## 🚀 Future Improvements
- Support for more complex queries
- Enhanced UI for better user experience
- Integration with machine learning models for smarter query processing





   
