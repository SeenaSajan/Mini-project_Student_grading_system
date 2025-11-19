import sqlite3
conn = sqlite3.connect('student_grading.db')
cursor = conn.cursor()
cursor.execute('''
      CREATE TABLE IF NOT EXISTS Teacher(
               Teachers_id INTEGER PRIMARY KEY AUTOINCREMENT,
               Name TEXT,
               Subject TEXT,
               Email VARCHAR(50),
               Password VARCHAR(50),
               Admin INTEGER DEFAULT 0
               )
''')


cursor.execute('''
      CREATE TABLE IF NOT EXISTS Student(
               Student_id INTEGER PRIMARY KEY AUTOINCREMENT ,
               Name TEXT,
               Class TEXT,
               Email VARCHAR(50),
               Teachers_id INTEGER,
               FOREIGN KEY (Teachers_id) REFERENCES Teacher(Teachers_id)

               )
''')

cursor.execute('''
      CREATE  TABLE IF NOT EXISTS Subject(
               Subject_id INTEGER PRIMARY KEY AUTOINCREMENT ,
               Subject_Name TEXT,
               Teachers_id INTEGER,
               FOREIGN KEY (Teachers_id) REFERENCES Teacher(Teachers_id)


               )
''')


cursor.execute('''
      CREATE  TABLE IF NOT EXISTS Grade(
               Grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
               Subject_id INTEGER,
               Marks INTEGER,
               Grade TEXT,
               Student_id INTEGER,
               FOREIGN KEY (Student_id) REFERENCES Student(Student_id),
               FOREIGN KEY (Subject_id) REFERENCES Subject(Subject_id)
               )
         ''')

conn.commit()
conn.close()
#________Register / Main Menu_______

def register_or_login():
     
     print("------STUDENT GRADING SYSTEM------")
     print("\n1.👩‍🏫 Teacher Registration")
     print("2.👩‍🏫Teacher Login")
     print("3.🧑‍🏫 Admin Login")
     print("4. 👧Student Login")
     choice = input("Enter choice: ")

     # 1. Teacher Registration
     if choice == "1":
        try:
            conn = sqlite3.connect('student_grading.db')
            cursor = conn.cursor()

            print("\n--- Create Teacher Account ---")
            name = input("Enter Name: ")
            subject = input("Enter Subject: ")
            email = input("Enter Email: ")
            password = input("Enter Password: ")

            
            admin_value = 0

            cursor.execute('''
                INSERT INTO Teacher (Name, Subject, Email, Password, Admin)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, subject, email, password, admin_value))

            conn.commit()
            conn.close()

            print("\nTeacher account created successfully👩‍🏫!")
            print("Please login now.\n")

        except Exception as e:
            print("Database Error:❌", e)
            
     # 2. Teacher Login
     elif choice == "2":
        login()

     # 3. Admin Login (FIXED)
     elif choice == "3":
        admin_login()

     # 4. Student Login
     elif choice == "4":
        student_login()

     else:
        print("Invalid choice. Please try again.")
        register_or_login()

#_______ ADMIN LOGIN _______

def admin_login():
    admin_name = input("\nEnter Admin Name: ")
    admin_password = input("Enter Admin Password: ")

   
    if admin_name == "admin" and admin_password == "admin123":
        print("\nAdmin Login Successful!")
        Admin_menu()
    else:
        print("Invalid Admin Credentials!")


#_______Login________

def login():
    Name = input("\n Enter your Name: ")
    Password = input("\n Enter your Password: ")

    try:
        conn = sqlite3.connect('student_grading.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Teachers_id, Name, Admin 
            FROM Teacher
            WHERE Name=? AND Password=? 
        ''', (Name, Password))

        result = cursor.fetchone()  

        if result:
            Teacher_id, Name, Admin = result
            print(f'\nWelcome {Name}!')

            if Admin == 1:
                Admin_menu()       
            else:
                Teacher_menu(Teacher_id)  
        else:
            print("Invalid credentials. Please try again.❌")

        conn.close()

    except Exception as e:
        print("Database Error:", e)

#________Student login_________
def student_login():
    sid = input("\nEnter Student ID: ")
    name = input("Enter Student Name: ")

    conn = sqlite3.connect('student_grading.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Student_id FROM Student 
        WHERE Student_id = ? AND Name = ?
    ''', (sid, name))

    result = cursor.fetchone()

    if result:
        print("\nLogin successful!✅")
        student_view(sid)
    else:
        print("Invalid student credentials.")




#__________ADMIN MENU____________

def Admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Teacher")
        print("2. View Teachers")
        print("3. Delete Teacher")
        print("4. Logout")

        choice = input("Enter choice: ")
        if choice == "1":
            add_teacher()
        elif choice == "2":
            view_teachers()
        elif choice == "3":
            delete_teacher()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

# ADD TEACHER
def add_teacher():
    try:
        conn = sqlite3.connect('student_grading.db')
        cursor = conn.cursor()
        name = input("Enter Teacher Name: ")
        subject = input("Enter Subject: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        admin = int(input("Admin (1 for Yes, 0 for No): "))

        cursor.execute('''INSERT INTO Teacher (Name, Subject, Email, Password, Admin) VALUES (?,?,?,?,?)''',
            (name, subject, email, password, admin)
        )
        print("Teacher added successfully!✅")
    except Exception as e:
        print("Error:", e)

        conn.close()
# VIEW TEACHER    

def view_teachers():
    conn = sqlite3.connect('student_grading.db')
    cursor = conn.cursor()

    print("\n1. View ALL teachers")
    print("2. View specific teacher")
    choice = input("Enter choice: ")

    # VIEW ALL
    if choice == "1":
        cursor.execute("SELECT Teachers_id, Name, Subject, Email, Admin FROM Teacher")
        data = cursor.fetchall()

        if not data:
            print("No teachers found.")
        else:
            print("\n--------------------------------------------------------------")
            print("{:<5} {:<15} {:<15} {:<25} {:<6}".format("ID", "Name", "Subject", "Email", "Admin"))
            print("--------------------------------------------------------------")

            for i in data:
                print("{:<5} {:<15} {:<15} {:<25} {:<6}".format(i[0], i[1], i[2], i[3], i[4]))

    # VIEW SPECIFIC
    elif choice == "2":
        tid = input("Enter Teacher ID: ")
        cursor.execute("SELECT Teachers_id, Name, Subject, Email, Admin FROM Teacher WHERE Teachers_id=?", (tid,))
        data = cursor.fetchall()

        if not data:
            print("Teacher not found.")
        else:
            print("\n--------------------------------------------------------------")
            print("{:<5} {:<15} {:<15} {:<25} {:<6}".format("ID", "Name", "Subject", "Email", "Admin"))
            print("--------------------------------------------------------------")

            for i in data:
                print("{:<5} {:<15} {:<15} {:<25} {:<6}".format(i[0], i[1], i[2], i[3], i[4]))

    else:
        print("Invalid choice.")

    conn.close()

# DELETE TEACHER
def delete_teacher():
    
        conn = sqlite3.connect('student_grading.db')
        cursor = conn.cursor()
        id=int(input('enter your Teacher id: '))
        choice=input('Are you sure to delete the data Y/N: ')
        if choice == 'Y':
            cursor.execute('''
               DELETE FROM Teacher WHERE Teachers_id =?
             ''',(id,))
            print('Task Deleted') 
        
        else:
            print('Task not Deleted')
            
            
        conn.commit()
        conn.close()
      
def logout():
    logout=input('Do you want to logout Y/N : ')
    if logout=='Y':
        print('Logged out')
    else:
        print('You are not logged out ')


#__________TEACHER MENU____________
def Teacher_menu(Teachers_id):
    while True:
        print("\n--- Teacher Menu👩‍🏫 ---")
        print("1. Manage Students")
        print("2. Manage Subjects")
        print("3. Manage Grades")
        print("4. Logout")

        choice = input('Enter choice: ')

        if choice == "1":
            manage_students(Teachers_id)
        elif choice == "2":
            manage_subjects(Teachers_id)
        elif choice == "3":
            manage_grades()
        elif choice == "4":
            print("\nLogging out...")
            break
        else:
            print("Invalid choice.")

   
                  
def manage_students(Teachers_id):
    print("\n1. Add Student\n2. View Students\n3. Edit Student\n4. Delete Student")
    choice = input("Enter choice: ")

    conn = sqlite3.connect('student_grading.db')
    cursor = conn.cursor()

    # ADD STUDENT
    if choice == "1":
        name = input("Enter Student Name: ")
        sclass = input("Enter Class: ")
        email = input("Enter Email: ")

        cursor.execute('''
            INSERT INTO Student (Name, Class, Email, Teachers_id)
            VALUES (?, ?, ?, ?)
        ''', (name, sclass, email, Teachers_id))

        conn.commit()
        print("Student added successfully!✅")

    # VIEW STUDENTS
    elif choice == "2":
        cursor.execute('''
            SELECT Student_id, Name, Class, Email 
            FROM Student 
            WHERE Teachers_id = ?
        ''', (Teachers_id,))

        alldata = cursor.fetchall()

        if not alldata:
            print("No students found.")
        else:
            print("\n----------------------------------------------------------")
            print("{:<10} {:<20} {:<10} {:<25}".format("ID", "Name", "Class", "Email"))
            print("----------------------------------------------------------")

            for i in alldata:
                print("{:<10} {:<20} {:<10} {:<25}".format(i[0], i[1], i[2], i[3]))
                
    # EDIT STUDENT
    elif choice == "3":
        sid = input("Enter Student ID to edit: ")

        new_name = input("Enter new name: ")
        new_class = input("Enter new class: ")
        new_email = input("Enter new email: ")

        cursor.execute('''
            UPDATE Student 
            SET Name=?, Class=?, Email=?
            WHERE Student_id=? AND Teachers_id=?
        ''', (new_name, new_class, new_email, sid, Teachers_id))

        conn.commit()
        print("Student updated successfully.✅")

    # DELETE STUDENT
    elif choice == "4":
        sid = input("Enter Student ID to delete: ")

        cursor.execute('''
            DELETE FROM Student 
            WHERE Student_id=? AND Teachers_id=?
        ''', (sid, Teachers_id))

        conn.commit()
        print("Student deleted successfully.✅")

    else:
        print("Invalid choice!")

    conn.close()


def manage_subjects(Teachers_id):
    conn = sqlite3.connect('student_grading.db')
    cursor = conn.cursor()

    print("\n1. Add Subject\n2. View Subjects\n3. Delete Subject")
    choice = input("Enter choice: ")

    # ADD SUBJECT
    if choice == "1":
        sid = int(input("Enter subject_id: "))
        sname = input("Enter subject_name: ")

        cursor.execute('''
            INSERT INTO Subject (Subject_id, Subject_Name, Teachers_id)
            VALUES (?, ?, ?)
        ''', (sid, sname, Teachers_id))

        conn.commit()
        print("Subject added successfully!✅")

    # VIEW SUBJECTS
    elif choice == "2":
        cursor.execute('''
            SELECT Subject_id, Subject_Name
            FROM Subject
            WHERE Teachers_id = ?
        ''', (Teachers_id,))

        alldata = cursor.fetchall()

        if not alldata:
            print("No subjects found.")
        else:
           print("\n--------------------------------------")
           print("{:<10} {:<20}".format("ID", "Subject Name"))
           print("--------------------------------------")
        for i in alldata:
            print("{:<10} {:<20}".format(i[0], i[1]))

    # DELETE SUBJECT
    elif choice == "3":
        sid = int(input("Enter subject_id to delete: "))

        cursor.execute('''
            DELETE FROM Subject 
            WHERE Subject_id=? AND Teachers_id=?
        ''', (sid, Teachers_id))

        conn.commit()
        print("Subject deleted successfully!✅")

    else:
        print("Invalid selection!")

    conn.close()

#_________GRADE________________
        
def manage_grades():
    conn = sqlite3.connect('student_grading.db')
    cursor = conn.cursor()

    print("\n1. Add Grade\n2. View Grades\n3. Edit Grade\n4. Delete Grade")
    choice = input("Enter choice: ")

    # 1. ADD GRADE
    if choice == "1":
        student_id = input("Enter Student ID: ")
        subject_id = input("Enter Subject ID: ")
        marks = input("Enter Marks: ")
        grade = input("Enter Grade (A/B/C etc): ")
        
        cursor.execute('''
            INSERT INTO Grade (Student_id,Subject_id, Marks, Grade )
            VALUES (?, ?,?,?)
        ''', (student_id,subject_id, marks, grade ))

        conn.commit()
        print("Grade added successfully!✅")

    # 2. VIEW GRADES
    elif choice == "2":
        cursor.execute('''
            SELECT Grade_id, Student_id, Subject_id, Marks, Grade
            FROM Grade
        ''')

        alldata = cursor.fetchall()

        if not alldata:
            print("No grades found.")
        else:
           print("\n----------------------------------------------------------------")
           print("{:<8} {:<12} {:<12} {:<10} {:<8}".format("ID", "Student", "Subject", "Marks", "Grade"))
           print("----------------------------------------------------------------")
        for i in alldata:
                print("{:<8} {:<12} {:<12} {:<10} {:<8}".format(i[0], i[1], i[2], i[3], i[4]))

    # 3. EDIT GRADE
    elif choice == "3":
        gid = input("Enter Grade ID to edit: ")

        new_marks = input("Enter new Marks: ")
        new_grade = input("Enter new Grade (A/B/C etc): ")

        cursor.execute('''
            UPDATE Grade
            SET Marks = ?, Grade = ?
            WHERE Grade_id = ?
        ''', (new_marks, new_grade, gid))

        conn.commit()
        print("Grade updated successfully.✅")

    # 4. DELETE GRADE
    elif choice == "4":
        gid = input("Enter Grade ID to delete: ")

        cursor.execute('''
            DELETE FROM Grade 
            WHERE Grade_id = ?
        ''', (gid,))

        conn.commit()
        print("Grade deleted successfully!✅")

    else:
        print("Invalid choice!")

    conn.close()
      
               

# ---------------------- Student View Only ----------------------
def student_view(student_id):
    conn = sqlite3.connect('student_grading.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Student.Name, Subject.Subject_Name, Grade.Marks, Grade.Grade
        FROM Student
        JOIN Grade ON Student.Student_id = Grade.Student_id
        JOIN Subject ON Grade.Subject_id = Subject.Subject_id
        WHERE Student.Student_id = ?
    ''', (student_id,))

    data = cursor.fetchall()

    print("\n--- Your Grades ---")

    if not data:
        print("No grades found for this student.")
    else:
        print("\n---------------------------------------------------------------")
        print("{:<20} {:<20} {:<10} {:<10}".format("Name", "Subject", "Marks", "Grade"))
        print("---------------------------------------------------------------")
    for row in data:
            print("{:<20} {:<20} {:<10} {:<10}".format(row[0], row[1], row[2], row[3]))
    conn.close()




register_or_login()



