import random
from datetime import datetime, timedelta
import mysql.connector

def generate_nim(used_nims):
    #year_list = ['20', '21', '22'  # Randomly select a prefix
    year = str(random.randint(18, 23))

    # Generate the rest of the digits
    #faculty = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    #faculty = ''.join([str(random.randint(1, 8))])
    five_digit_list = ['86204', '86205', '86202', '86201', '86203', '86206', '86250', '86207', '73201',
                        '88201', '88202', '88203', '88207', '88206', '88211', '88209', '88210', '88212',
                        '79201', '79202', '84202', '84203', '84204', '84205', '84201', '44201', '45201',
                        '46201', '47201', '49201', '87205', '87202', '87201', '87204', '87220', '80201',
                        '63201', '70201', '23902', '83211', '83212', '83201', '83202', '83207', '21201',
                        '83203', '83204', '83205', '53814', '53714', '53914', '21403', '94406', '94405',
                        '94408', '20403', '20401', '21401', '22401', '89201', '85201', '85202', '89202',
                        '62201', '61201', '87210', '87209', '87203', '62401', '61404', '63412']
    
    while True:
        five_digit = random.choice(five_digit_list)
        status = str(random.randint(1, 6))
        num = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        nim = year + five_digit + status + num
        
        if nim not in used_nims:
            used_nims.add(nim)
            return nim

def generate_name():
    first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Emma', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor']

    first = random.choice(first_names)
    last = random.choice(last_names)
    # Generate a list of student names
    student_names = first + ' ' + last

    return student_names

def generate_birth_date():
    start_date = datetime(1997, 1, 1)  # Start date
    end_date = datetime(2005, 12, 31)  # End date
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

def generate_ipk():
    return round(random.uniform(2.50, 3.95), 2)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mahasiswa"  # assuming the database exists
)

# Create a cursor
mycursor = mydb.cursor()

# Generate and insert 100 records
generated_nims = set()
for _ in range(100):
    nim = generate_nim(generated_nims)
    name = generate_name()
    birth_date = generate_birth_date()
    ipk = generate_ipk()

    # SQL query to insert data
    sql = "INSERT INTO data_mhs (nim, nama, tgl_lahir, ipk) VALUES (%s, %s, %s, %s)"
    val = (nim, name, birth_date, ipk)

    # Execute query
    mycursor.execute(sql, val)

# Commit changes and close connection
mydb.commit()
mydb.close()

# generated_numbers = set()
# num_to_generate = 10  # Change this number to generate more phone numbers

# while len(generated_numbers) < num_to_generate:
#     nim = generate_ipk()
#     if nim not in generated_numbers:
#         generated_numbers.add(nim)

# for number in generated_numbers:
#     print(number)
