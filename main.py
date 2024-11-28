import utils

user = {}
utils.db = utils.init_db()

def land_page():                # landing page menu, ask if you wanna sign in or sign up
    utils.os.system("cls||clear")
    match utils.ask_question("To start viewing student records, you will need an account.", [
        "Log in",               
        "Sign up",                  
        " (Exit)"
    ]):
        case 0:
            global user
            user = utils.log_in()
            if user: main_menu()
        case 1:
            if utils.sign_up(): main_menu()
        case 2:
            return
        
    land_page()

add_message = ''

def main_menu():                # main menu, ask if you wanna do the main functions of the program
    global add_message
    utils.os.system("cls||clear")
    match utils.ask_question(f"{add_message}Welcome, {user['username']}! What would you like to do?", [
        "View/delete/modify all student records",
        "Add new student record",
        "View statistics",
        " (Exit)"
    ]):
        case 0:
            add_message = ''
            err = utils.view_student_records()
            if err:
                add_message = err
        case 1:
            add_message = ''
            result = utils.new_student_record()
            if result:
                add_message = result
            pass
        case 2:
            add_message = ''
            utils.view_statistics()
            pass
        case 3:
            add_message = ''
            return
        
    main_menu()

# utils.questionary.autocomplete("Search (Start typing to see results):\n", ["apple", "banana", "cherry", "durianduriandurianduriandurianduriandurian", "elephant", "fig"], ignore_case=True, match_middle=True, style=utils.autocomplete_style).ask()

land_page()
