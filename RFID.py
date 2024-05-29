import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # replace with your database username
    password="March@1313",   # replace with your database password
    database="ONGC"
)
cursor = conn.cursor()

# Function to check if a row in 'Tag' is in 'Employees'
def check_employee():
    # Check if the Tag table is empty
    cursor.execute("SELECT COUNT(*) FROM Tag")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Is a Visitor")
        return

    # Fetch the details from the Tag table
    cursor.execute("SELECT ID, Name FROM Tag")
    tags = cursor.fetchall()

    for tag in tags:
        tag_id, tag_name = tag

        # Check if the tag details are in the Employees table
        query = "SELECT e.ID, e.Name FROM Employees e WHERE e.ID = %s AND e.Name = %s"
        cursor.execute(query, (tag_id, tag_name))
        result = cursor.fetchone()

        if result:
            print(f"Employee ID: {result[0]}, Name: {result[1]} is an Employee")
        else:
            print(f"ID: {tag_id}, Name: {tag_name} is not an employee")

    # Clear all the rows in the Tag table
    cursor.execute("DELETE FROM Tag")
    conn.commit()

# Call the function to check employees
check_employee()

# Close the database connection
conn.close()



