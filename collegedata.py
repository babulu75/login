import csv
import MySQLdb

# Connect to MySQL
db = MySQLdb.connect(host="localhost", user="root", passwd="Vinni@02#feb", db="record_writer_platform")
cursor = db.cursor()

# Path to your colleges CSV file
csv_file_path = r"C:\Users\babul\OneDrive\Desktop\final_data.csv"

# Open and read the CSV file
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Skip the header if there is one
    next(csv_reader)  # Remove this line if there is no header
    
    # Insert each row into the colleges table
    for row in csv_reader:
        # Assuming the columns in the CSV are: name, city, state, country
        name = row[0]
        city = row[1]
        state = row[2]
        country = row[3]

        # Insert into the colleges table
        try:
            cursor.execute("""
                INSERT INTO colleges (name, city, state, country) 
                VALUES (%s, %s, %s, %s)
            """, (name, city, state, country))
            db.commit()  # Commit the transaction
        except Exception as e:
            print(f"Error inserting {name}: {e}")
            db.rollback()  # Rollback in case of error

# Close the database connection
cursor.close()
db.close()

print("Data inserted successfully!")
