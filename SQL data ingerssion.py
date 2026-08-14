import pandas as pd
import random
import mysql.connector

# SQL Server connection details
host = "localhost"
database = "pl_mission_de"
username = "root"
password = "Root"


# Create connection
connection = mysql.connector.connect(
    host=host,
    port=3306,
    user=username,
    password=password,
    database=database
)

# Sample names list
names_list = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan",
    "Fiona", "George", "Hannah", "Ian", "Julia",
    "Kevin", "Laura", "Michael", "Nina", "Oscar",
    "Paula", "Quentin", "Rachel", "Sam", "Tina"
]

# Departments and salary ranges
departments = {
    "employee": (50, 100),
    "sr_manager": (200, 300),
    "manager": (100, 200),
    "hr": (150, 200)
}

# Generate 100 rows
data = []
for emp_id in range(1, 101):
    name = random.choice(names_list)
    dept = random.choice(list(departments.keys()))
    salary_range = departments[dept]
    salary = random.randint(salary_range[0], salary_range[1])

    data.append({
        "emp_id": emp_id,
        "name": name,
        "department": dept,
        "salary": salary
    })

# Convert to DataFrame
df = pd.DataFrame(data)
# print(df)

cursor = connection.cursor()

# SQL ingestion

# SQL operation create table
query_use = "USE pl_mission_de;"
query_delete ="DROP TABLE IF EXISTS EMPLOYEE;"

query_create = """
CREATE TABLE IF NOT EXISTS pl_mission_de.EMPLOYEE (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50),
    salary INT
);
"""

# Execute Table Creation and queries
cursor.execute(query_use)
cursor.execute(query_delete)
cursor.execute(query_create)

# Insert rows into EMPLOYEE table
insert_query = """
INSERT INTO EMPLOYEE (emp_id, name, department, salary)
VALUES (%s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        int(row['emp_id']),
        row['name'],
        row['department'],
        int(row['salary'])
    ))


# Commit changes
connection.commit()

#cursor close
cursor.close()

# Connection close
connection.close()

print("table created on the Database successfully!")

