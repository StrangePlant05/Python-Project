import os
import json
import questionary
import re
from colorama import Fore, Back, init, Style
from custom_styles import question_style, autocomplete_style

db = {
    "users": [],
    "student_records": {},
    "default_courses": ["BSIT", "BSCS"],
    "default_subjects": ["MCS1", "CAL1", "FOC1"],
}

db = {
    "users": [],
    "student_records": {
        "student_id": {
            "name": "name",
            "course": "course",
            "year": "Freshman",
            "section": "1B-G2",
            "grades": {
                "MCS": 90,
                "MCS1": 90,
                "MCS2": 90,
                "MCS3": 90,
                "MCS4": 90,
            }
        }
    }
}

def init_db():                  # creates database if not exists
    init(autoreset=True)
    if not os.path.exists("data/db.json"):
        with open("data/db.json", "w") as file:
            json.dump({
                "users": [],
                "student_records": {},
                "default_courses": ["BSIT", "BSCS"],
                "default_subjects": ["MCS1", "CAL1", "FOC1"],
            }, file, indent=4)

    with open("data/db.json", "r") as file:
        return json.load(file)

def overwrite_db():             # save database
    with open("data/db.json", "w") as file:
        json.dump(db, file, indent=4)

def ask_question(question:str, choices:list):           # ask question and let user pick from choices
    answer = questionary.select(question, choices, style=question_style).ask()
    return choices.index(answer)

def valid_password(password:str):                       # check if password contains A - Z, a - z, 0 - 9
    return not any([not re.search(r"[0-9]", password), not re.search(r"[A-Z]", password), not re.search(r"[a-z]", password)])

def get_user(username):                                 # gets user from database, if not found, return false
    user = [user for user in db["users"] if user["username"] == username]
    return user[0] if len(user) > 0 else False

def validate_username_signup(username:str):             # checks if username is alpha-numeric
    if get_user(username):
        return "Username already exists"
    
    if not username.isalnum():
        return "Username can only contain letters and numbers"
    
    return True

def add_user(user:dict):            #adds user to database then saves database
    db["users"].append(user)
    overwrite_db()

def get_all_students() -> dict:     # gets all students from database
    return db["student_records"]

def get_student_by_id(student_id):
    return db["student_records"][student_id]

def add_student(student):
    student_records = db["student_records"]
    student_id = ""
    if len(student_records) == 0:
        student_id = "2024000000"
    else:
        student_id = str(int(list(student_records)[-1]) + 1)

    db["student_records"][student_id] = student
    overwrite_db()
    
def log_in():                       # log in function
    add = ''
    while True:                             # gets username, check if user is in database
        os.system("cls||clear")
        username=questionary.text(add+"Please enter your username (type exit to cancel):\n", style=question_style).ask()

        if username == "exit":          
            return False
        
        user = get_user(username)

        if not user:
            add = "Username not found\n"
            continue

        add = ''
        break

    while True:                             # gets password, check if password is the same as the found user's password
        os.system("cls||clear")
        password=questionary.password(add+"Please enter your password (type exit to cancel):\n", style=question_style).ask()

        if password == "exit":
            return False
        
        if password != user["password"]:
            add = "Wrong password\n"
            continue

        add = ''

        break
    return user
    
def sign_up():                          # sign up function
    os.system("cls||clear")
    username=questionary.text("Please enter your desired username (type exit to cancel):\n", 
        style=question_style,                       # enter username and use the username checker from before
        validate=validate_username_signup
    ).ask()

    if username == "exit":
        return False

    password=questionary.password("Please enter your desired password (type exit to cancel):\n",        # enter password and use the password checker from before
        style=question_style, 
        validate=lambda x:(valid_password(x) or x.lower() == "exit") or "Password must contain at least one lowercase, one uppercase, and one number."
    ).ask()

    if password == "exit":
        return False
    
    confirm = questionary.password("Please enter your password again (type exit to cancel):\n",         # simple confirm password
        style=question_style,
        validate=lambda x: (x == password or x == "exit") or "Password doesn't match").ask()
    
    if confirm == "exit":
        return False
    
    add_user({"username": username, "password": password})

def single_student_string(student_id:str|None, student:dict):
    formatted = ''
    name = student["name"]
    course = student["course"]
    year = student["year"]
    section = student["section"]
    grades = student["grades"]

    if student_id:
        formatted+=student_id + ", " + name + "\n"
    else:
        formatted+="Student name: "+name + "\n"

    formatted+="     ├" + " Course: " + course + "\n"
    formatted+="     ├" + " Year level: " + year + "\n"
    formatted+="     ├" + " Section: " + section + "\n"
    formatted+="     └" + " Grades:\n"

    if len(grades) == 0:
        formatted+="          └ No grades\n"

    total_grade = 0
    grades_count = 0

    for i, (subject, value) in enumerate(grades.items()):
        if not type(value) is str:
            total_grade += value
            grades_count += 1
        if i == len(grades) - 1:
            formatted+="          └ " + subject + ": " + str(value) + "\n"
            continue
        formatted+="          ├ " + subject + ": " + str(value) + "\n"

    if total_grade != 0:
        formatted += "     └" + " Average: "+ str(total_grade / grades_count) +"\n"

    return formatted

def student_records_string_list(student_records):
    formatted = []
    for student_id in student_records.keys():
        student = student_records[student_id]
        formatted.append(single_student_string(student_id, student))

    return formatted

def student_search_format(student_id, student):
    name = student["name"]
    return student_id + ", " + name

def student_records_search_list(student_records):
    formatted = []
    for student_id in student_records.keys():
        student = student_records[student_id]
        formatted.append(student_search_format(student_id, student))

    return formatted

def view_student_records():             # unfinished lol
    os.system('cls||clear')

    student_records = get_all_students()

    if not student_records:
        return "There are no records yet.\n"
    
    search_list = [" (Back)", " (Search)"]
    search_list.extend(student_records_search_list(student_records))

    answer = questionary.select("Select a record you would like to view", search_list, style=question_style).ask()

    if search_list.index(answer) == 0:
        return
    
    if search_list.index(answer) == 1:
        search_list.pop(0)
        search_list.pop(0)
        search_list.insert(0, "cancel")
        answer = questionary.autocomplete("Search for student (Start typing to see results, enter 'cancel' to cancel):\n", 
            choices=search_list,
            ignore_case=True,
            match_middle=True,
            style=autocomplete_style).ask()
        
        if search_list.index(answer) == 0:
            view_student_records()
            return
        

    student_id = answer[:10]      #2024102509
    student = get_student_by_id(student_id)

    os.system("cls||clear")

    print(single_student_string(student_id, student))

    match ask_question("What would you like to do with this record?", [
        " (Cancel)",
        "Modify",
        "Delete"
    ]):
        case 1:
            modify_student_record(student, student_id)
        case 2:
            if questionary.confirm("Are you sure you would like to delete this record?").ask():
                del db["student_records"][student_id]
                overwrite_db()

                return "Deleted the record!\n"



def validate_modify_record(student):
    return not any([
        student["name"] == "Undefined",
        student["course"] == "Undefined",
        student["year"] == "Undefined",
        student["section"] == "Undefined",
        len(student["grades"]) == 0])

def modify_student_record(student, student_id, add=""):
    os.system("cls||clear")

    print(single_student_string(student_id, student))

    match ask_question(add+"Select what you want to modify:", choices=[
        " (Cancel)",
        " (Save)",
        "Name",
        "Course",
        "Year",
        "Section",
        "Grades"
    ]):
        case 0:     #cancel
            return
        case 1:     #save
            if not validate_modify_record(student):
                modify_student_record(student=student, student_id=student_id, add="Please fill in all fields.\n")
                return
            
            overwrite_db()
            
        case 2:     #name
            answer = questionary.text("Please input name, (type 'cancel' to cancel):", 
                style=question_style, 
                validate=lambda x: (x != "" and any([re.search(r"[a-z]", x), re.search(r"[A-Z]", x)])) or "Invalid input",
                default=student["name"] if student["name"] != "Undefined" else "").ask()
            if answer.lower() == "cancel":
                modify_student_record(student=student, student_id=student_id)
                return
            
            student["name"] = answer.strip()
            modify_student_record(student=student, student_id=student_id)
            return
        
        case 3:     #course
            courses = [" (Cancel)", " (Add new course)"]
            courses.extend(db["default_courses"])
            answer = ask_question("Select a course", courses)
            match answer:
                case 0:
                    modify_student_record(student=student, student_id=student_id)
                    return
                case 1:
                    answer = questionary.text("Please input course, (type 'cancel' to cancel):", 
                        style=question_style, 
                        validate=lambda x: x.isalpha() or "Course can only have letters",
                        default=student["course"] if student["course"] != "Undefined" else "").ask()
                    if answer.lower() == "cancel":
                        modify_student_record(student=student, student_id=student_id)
                        return

                    if not answer in db["default_courses"]:
                        db["default_courses"].append(answer)
                    student["course"] = answer
                    modify_student_record(student=student, student_id=student_id)
                    return

                case _:
                    student["course"] = courses[answer]
                    modify_student_record(student=student, student_id=student_id)
                    return  
                
        case 4:     #year
            years = [" (Cancel)", "First Year", "Second Year", "Third Year", "Fourth Year"]
            answer = ask_question("Modifying year level", years)
            if answer == 0:
                modify_student_record(student=student, student_id=student_id)
                return
            student["year"] = years[answer]
            modify_student_record(student=student, student_id=student_id)
            return
        
        case 5:     #section
            answer = questionary.text("Please input section, (type 'cancel' to cancel):", 
                style=question_style, 
                validate=lambda x: x.isalnum() or "Section can only have letters an numbers",
                default=student["section"] if student["section"] != "Undefined" else "").ask()
            if answer.lower() == "cancel":
                modify_student_record(student=student, student_id=student_id)
                return 
            
            student["section"] = answer
            modify_student_record(student=student, student_id=student_id)
            return
        
        case 6:     #subjects
            subjects = ["Cancel", "Add new subject", "Remove subject", "Modify Grade"]
            answer = ask_question("Modifying subjects", subjects)
            match answer:
                case 0:
                    modify_student_record(student=student, student_id=student_id)
                    return
                case 1:
                    subject = [" (Cancel)", " (Add new subject)"]
                    subject.extend(db["default_subjects"])
                    answer = ask_question("Select a subject to add", subject)
                    match answer:
                        case 0:
                            modify_student_record(student=student, student_id=student_id)
                            return
                        case 1:
                            answer = questionary.text("Please input subject, (type 'cancel' to cancel):", 
                                style=question_style, 
                                validate=lambda x: x.isalnum() or "Subject can only have letters and numbers",
                            ).ask()
                            if answer.lower() == "cancel":
                                modify_student_record(student=student, student_id=student_id)
                                return

                            if not answer in db["default_subjects"]:
                                db["default_subjects"].append(answer)
                            student["grades"][answer] = "Undefined"
                            modify_student_record(student=student, student_id=student_id)
                            return

                        case _:
                            student["grades"][subject[answer]] = "Undefined"
                            modify_student_record(student=student, student_id=student_id)
                            return

                case 2:
                    subjects = list(student["grades"].keys())
                    subjects.insert(0, " (Cancel)")
                    answer = questionary.checkbox("Select what you want to remove", 
                        choices=subjects,
                        style=question_style).ask()
                    
                    if len(answer) == 1 and answer[0] == " (Cancel)":
                        modify_student_record(student=student, student_id=student_id)
                        return
                    
                    [student["grades"].pop(sub) for sub in answer]
                    modify_student_record(student=student, student_id=student_id)
                    return
                
                case 3:
                    subjects = list(student["grades"].keys())
                    subjects.insert(0, " (Cancel)")
                    answer = ask_question("Select what you would like to modify", choices=subjects)
                    match answer:
                        case 0:
                            modify_student_record(student=student, student_id=student_id)
                            return
                        case _:
                            grade = questionary.text("Enter new grade, (type 'cancel' to cancel):", style=question_style, 
                                validate=lambda x: ((x.count(".") < 2 and x.replace(".", "").isdigit() and x.count("-") == 0) or x.lower() == "cancel") or "Invalid input"
                            ).ask()
                            
                            if grade == "cancel":
                                modify_student_record(student=student, student_id=student_id)
                                return

                            grade = float(grade)
                            student["grades"][subjects[answer]] = grade
                            modify_student_record(student=student, student_id=student_id)
                            return



def new_student_record(student=None, add=""):
    os.system("cls||clear")
    if not student:
        student = {
            "name": "Undefined",
            "course": "Undefined",
            "year": "Undefined",
            "section": "Undefined",
            "grades": {}
        }

    print(single_student_string(None, student))

    match ask_question(add+"Select what you want to modify:", choices=[
        " (Cancel)",
        " (Save)",
        "Name",
        "Course",
        "Year",
        "Section",
        "Enrolled subjects"
    ]):
        case 0:     #cancel
            return
        case 1:     #save
            if not validate_modify_record(student):
                new_student_record(student=student, add="Please fill in all fields.\n")
                return
            
            add_student(student)
            
        case 2:     #name
            answer = questionary.text("Please input name, (type 'cancel' to cancel):", 
                style=question_style, 
                validate=lambda x: (x != "" and any([re.search(r"[a-z]", x), re.search(r"[A-Z]", x)])) or "Invalid input",
                default=student["name"] if student["name"] != "Undefined" else "").ask()
            if answer.lower() == "cancel":
                new_student_record(student=student)
                return
            
            student["name"] = answer.strip()
            new_student_record(student=student)
            return
        
        case 3:     #course
            courses = [" (Cancel)", " (Add new course)"]
            courses.extend(db["default_courses"])
            answer = ask_question("Select a course", courses)
            match answer:
                case 0:
                    new_student_record(student=student)
                    return
                case 1:
                    answer = questionary.text("Please input course, (type 'cancel' to cancel):", 
                        style=question_style, 
                        validate=lambda x: x.isalpha() or "Course can only have letters",
                        default=student["course"] if student["course"] != "Undefined" else "").ask()
                    if answer.lower() == "cancel":
                        new_student_record(student=student)
                        return

                    if not answer in db["default_courses"]:
                        db["default_courses"].append(answer)
                    student["course"] = answer
                    new_student_record(student=student)
                    return

                case _:
                    student["course"] = courses[answer]
                    new_student_record(student=student)
                    return  
                
        case 4:     #year
            years = [" (Cancel)", "First Year", "Second Year", "Third Year", "Fourth Year"]
            answer = ask_question("Modifying year level", years)
            if answer == 0:
                new_student_record(student=student)
                return
            student["year"] = years[answer]
            new_student_record(student=student)
            return
        
        case 5:     #section
            answer = questionary.text("Please input section, (type 'cancel' to cancel):", 
                style=question_style, 
                validate=lambda x: x.isalnum() or "Section can only have letters an numbers",
                default=student["section"] if student["section"] != "Undefined" else "").ask()
            if answer.lower() == "cancel":
                new_student_record(student=student)
                return 
            
            student["section"] = answer
            new_student_record(student=student)
            return
        
        case 6:     #subjects
            subjects = ["Cancel", "Add new subject", "Remove subject"]
            answer = ask_question("Modifying subjects", subjects)
            match answer:
                case 0:
                    new_student_record(student=student)
                    return
                case 1:
                    subject = [" (Cancel)", " (Add new subject)"]
                    subject.extend(db["default_subjects"])
                    answer = ask_question("Select a subject to add", subject)
                    match answer:
                        case 0:
                            new_student_record(student=student)
                            return
                        case 1:
                            answer = questionary.text("Please input subject, (type 'cancel' to cancel):", 
                                style=question_style, 
                                validate=lambda x: x.isalnum() or "Subject can only have letters and numbers",
                            ).ask()
                            if answer.lower() == "cancel":
                                new_student_record(student=student)
                                return

                            if not answer in db["default_subjects"]:
                                db["default_subjects"].append(answer)
                            student["grades"][answer] = "Undefined"
                            new_student_record(student=student)
                            return

                        case _:
                            student["grades"][subject[answer]] = "Undefined"
                            new_student_record(student=student)
                            return

                case 2:
                    subjects = list(student["grades"].keys())
                    subjects.insert(0, " (Cancel)")
                    answer = questionary.checkbox("Select what you want to remove", 
                        choices=subjects,
                        style=question_style).ask()
                    
                    if len(answer) == 1 and answer[0] == " (Cancel)":
                        new_student_record(student=student)
                        return
                    
                    [student["grades"].pop(sub) for sub in answer]
                    new_student_record(student=student)
                    return
    
def view_statistics():
    os.system("cls||clear")

    students = get_all_students()

    if len(students) == 0:
        print(Fore.YELLOW + "Database has no student records.")
        questionary.press_any_key_to_continue().ask()
        return
    
    # total average for all records
    total_all = 0
    all_count = 0
    subjects_with_grades = []
    courses_with_grades = []
    for key in students.keys():
        student = students[key]
        for subject in student["grades"].keys():
            if type(student["grades"][subject]) is str: continue
            total_all += student["grades"][subject]
            all_count += 1

            if not subject in subjects_with_grades:
                subjects_with_grades.append(subject)
            
            if not student["course"] in courses_with_grades:
                courses_with_grades.append(student["course"])

    print(Fore.YELLOW + "Total average grade:", Fore.CYAN + str(total_all / all_count))


    # total average for each course
    print("\n"+Fore.YELLOW + "Total per course:")
    for course in courses_with_grades:
        total_course = 0
        course_count = 0
        for key in students.keys():
            student = students[key]
            if course == student["course"]:
                for subject in student["grades"].keys():
                    if type(student["grades"][subject]) is str: continue
                    total_course += student["grades"][subject]
                    course_count += 1

        
        if courses_with_grades[-1] == course:
            print(f"     └ {Fore.BLUE}{course}:",  Fore.CYAN + str(total_course / course_count))
            continue
        print(f"     ├ {Fore.BLUE}{course}:", Fore.CYAN + str(total_course / course_count))


    # total average for each subject
    print("\n"+Fore.YELLOW + "Total per subjects:")
    for subject in subjects_with_grades:
        total_subject = 0
        subject_count = 0
        for key in students.keys():
            student = students[key]
            if subject in student["grades"].keys():
                if type(student["grades"][subject]) is str: continue
                total_subject += student["grades"][subject]
                subject_count += 1
        
        if subjects_with_grades[-1] == subject:
            print(f"     └ {Fore.BLUE}{subject}:", Fore.CYAN + str(total_subject / subject_count))
            continue
        print(f"     ├ {Fore.BLUE}{subject}:", Fore.CYAN + str(total_subject / subject_count))


    
    

    questionary.press_any_key_to_continue().ask()
