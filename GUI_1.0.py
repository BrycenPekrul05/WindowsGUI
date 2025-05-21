"""

SCRIPT MUST RUN IN ADMINISTRATOR MODE
    script will automatically run in admin mode 
    if prompted when the script is ran selected yes or the script will not have full capabilities 

"""
# ensures that the script is ran as an administrator
import ctypes, sys, os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    
    except:
        return False

if not is_admin():
    # Relaunch script as admin
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    
    sys.exit()

#=============================================================================================
# main GUI script

from tkinter import *
from tkinter import messagebox
from InteractiveWindowsScript_1 import *
import threading

# used for removing widgets when the screen changes
widgets = []

# init. main_window
main_window = Tk()
main_window.title("---Interactive Windows Tool---")
main_window.geometry("600x700")

main_window.columnconfigure(0, weight=1)
main_window.columnconfigure(1, weight=1)

# holds buttons and output boxes that are used for multiple different screens / functions
def info_screen(type):
    # clear the canvas of all widgets
    for widget in widgets:
        widget.grid_forget()

    # globally declare button variables so they can later be hidden 
    global ask_for_directory, ask_for_directory_input, result_box

    # result box for outputs from "InteractiveWindowsScript.py"
    result_box = Text(main_window, height=30, width=100)
    result_box.grid(column=0, row=4, columnspan=2, pady=10)
    widgets.append(result_box)
    
    # takes user back to start screen
    back_button = Button(main_window, text="Return to Start Screen", command=start_screen)
    back_button.grid(column=0, row=0, columnspan=2)
    widgets.append(back_button)

    # buttons for file searching functions
    if type == "file":
        # prompts user for a directory to search
        ask_for_directory = Label(main_window, text="Input Directory: ")
        ask_for_directory.grid(column=0, row=1)
        widgets.append(ask_for_directory)

        # box to type said directory into
        ask_for_directory_input = Entry(main_window, width=30)
        ask_for_directory_input.grid(column=1, row=1)
        widgets.append(ask_for_directory_input)

# search for file types within a directory
def file_type_search():
    # used to init. the result box and text entry boxes
    info_screen("file") 
    global ask_for_filetype, ask_for_filetypes_input, run_function

    list_of_filetypes = [
        ".txt", ".pdf", ".doc", ".docx", ".odt"  
        ".rtf", ".xls", ".xlsx", ".csv", ".ppt"  
        ".pptx", ".jpg", ".jpeg", ".png", ".gif"  
        ".bmp", ".svg", ".tiff", ".webp", ".mp4"  
        ".mov", ".avi", ".mkv", ".flv", ".wmv"  
        ".mp3", ".wav", ".aac", ".flac", ".ogg"  
        ".m4a", ".py", ".js", ".html", ".css"  
        ".c", ".cpp", ".java", ".sh", ".bat"  
        ".ps1", ".zip", ".rar", ".7z", ".tar"  
        ".gz", ".exe", ".dll", ".sys", ".iso", 
        ".lnk"
    ]

    # actually starts the running of the function
    def run_search():
        filetypes_input = ask_for_filetypes_input.get()
        file_types = [ftype.strip() for ftype in filetypes_input.split(",") if ftype.strip()]

        result = searchDirectory(ask_for_directory_input.get(), file_types)
        result_box.delete("1.0", END)
        
        if result:
            result_box.insert("1.0", "\n".join(result))
        else: 
            result_box.insert("1.0", "No files found.")

    # buttons 
    ask_for_filetype = Label(main_window, text="Input File Type: ")
    ask_for_filetype.grid(column=0, row=2)
    widgets.append(ask_for_filetype)

    ask_for_filetypes_input = Entry(main_window, width=30)
    ask_for_filetypes_input.grid(column=1, row=2)
    widgets.append(ask_for_filetypes_input)

    run_function = Button(main_window, text="Search", command=run_search)
    run_function.grid(column=0, row=3)
    widgets.append(run_function)

# search for files with a keyword in the name
def file_name_search_screen():
    info_screen("file")
    global ask_for_file, ask_for_file_input, run_function

    # run the search
    def run_search():
        result = keywordSearchExternal(ask_for_directory_input.get(), ask_for_file_input.get())
        result_box.delete("1.0", END)

        if result:
            result_box.insert("1.0", "\n".join(result))
        else: 
            result_box.insert("1.0", "No files found.")

    # buttons and labels for search
    ask_for_file = Label(main_window, text="Input File Keyword: ")
    ask_for_file.grid(column=0, row=2)
    widgets.append(ask_for_file)

    ask_for_file_input = Entry(main_window, width=30)
    ask_for_file_input.grid(column=1, row=2)
    widgets.append(ask_for_file_input)

    run_function = Button(main_window, text="Search", command=run_search)
    run_function.grid(column=0, row=3)
    widgets.append(run_function)

# search inside files for a keyword
def internal_file_search_screen():
    info_screen("file")
    global ask_for_keyword, ask_for_keyword_input, run_function

    # run the search
    def run_search():
        result = keywordSearchInternal(ask_for_directory_input.get(), ask_for_keyword_input.get())
        result_box.delete("1.0", END)

        if result:
            result_box.insert("1.0", "\n".join(result))
        else: 
            result_box.insert("1.0", "No files found.")

    # buttons and labels for search
    ask_for_keyword = Label(main_window, text="Input Keyword: ")
    ask_for_keyword.grid(column=0, row=2)
    widgets.append(ask_for_keyword)

    ask_for_keyword_input = Entry(main_window, width=30)
    ask_for_keyword_input.grid(column=1, row=2)
    widgets.append(ask_for_keyword_input)

    run_function = Button(main_window, text="Search", command=run_search)
    run_function.grid(column=0, row=3)
    widgets.append(run_function)

# sort all users by admin or not, then alphabetical 
def user_sort_screen():
    global run_function
    info_screen("user")

    # run the function ( automatically runs )
    def run_search():
        admins, non_admins = get_local_users()
        result_box.delete("1.0", END)
        result_box.insert(END, "=================================\n")

        # output administrators on a system
        if admins:
            result_box.insert(END, "Administrators:\n")
            result_box.insert(END, "\n".join(admins) + "\n\n")

        # case if no admins are found
        else:
            result_box.insert(END, "Administrators:\nNone found.\n\n")

        result_box.insert(END, "\n=================================\n")

        # output non administrators on a system
        if non_admins:
            result_box.insert(END, "Standard Users:\n")
            result_box.insert(END, "\n".join(non_admins))

        # case if no non_admins are found 
        else:
            result_box.insert(END, "Standard Users:\nNone found.")

        result_box.insert(END, "\n=================================")

    # delete a user from the system 
    def delete_local_user():
        ask_for_user = Label(main_window, text="Input user you want to delete: ")
        ask_for_user.grid(column=0, row=10)
        widgets.append(ask_for_user)

        ask_for_user_input = Entry(main_window, width=30)
        ask_for_user_input.grid(column=1, row=10)
        widgets.append(ask_for_user_input)

        def delete():
            selected_user = ask_for_user_input.get()

            # prompt the user so no user is accidentally deleted
            if selected_user:
                confirm = messagebox.askyesno("Confirm Deletion", f"Delete user '{selected_user}'")

                if confirm:
                    result = remove_user(selected_user)
                    messagebox.showinfo("Result: ", result)

        # delete user button
        run_deletion = Button(main_window, text="Delete User", command=delete)
        run_deletion.grid(column=1, row=11, columnspan=2)
        widgets.append(run_deletion)

    def add_local_user():
        ask_for_user1 = Label(main_window, text="Input user name you want to create: ")
        ask_for_user1.grid(column=0, row=12)
        widgets.append(ask_for_user1)

        ask_for_user1_input = Entry(main_window, width=30)
        ask_for_user1_input.grid(column=1, row=12)
        widgets.append(ask_for_user1_input)

        ask_for_user1_password = Label(main_window, text="Input the password for the new user: ")
        ask_for_user1_password.grid(column=0, row=13)
        widgets.append(ask_for_user1_password)

        ask_for_user1_password_input = Entry(main_window, width=30)
        ask_for_user1_password_input.grid(column=1, row=13)
        widgets.append(ask_for_user1_password_input)

        def add():
            new_user = ask_for_user1_input.get()
            new_user_password = ask_for_user1_password_input.get()

            if new_user:
                if new_user_password:
                    confirm = messagebox.askyesno("Confirm info", f"New User Name: '{new_user}'\nNew User Password: '{new_user_password}'")
                    
                    if confirm:
                        result = add_user(new_user, new_user_password)
                        messagebox.showinfo("Result: ", result)

        add_user_button = Button(main_window, text="Add User", command=add)
        add_user_button.grid(column=1, row=14, columnspan=2)
        widgets.append(add_user_button)

    def disable_user_GUI():
        ask_for_user = Label(main_window, text="Enter account name you want to disable: ")
        ask_for_user.grid(column=0, row=15)
        widgets.append(ask_for_user)

        ask_for_user_input = Entry(main_window, width=30)
        ask_for_user_input.grid(column=1, row=15)
        widgets.append(ask_for_user_input)

        def disable():
            username = ask_for_user_input.get()

            if username:
                confirm = messagebox.askyesno("Confirm info", f"User to Disable: '{username}'")

                if confirm:
                    result = disable_user(username)
                    messagebox.showinfo("Result: ", result)
            
        disable_user_button = Button(main_window, text="Disable User", command=disable)
        disable_user_button.grid(column=1, row=16)
        widgets.append(disable_user_button)

    run_search()
    delete_local_user()
    add_local_user()
    disable_user_GUI()

def set_local_policies():
    info_screen("policies")
    
    def run_script():
        result_box.delete("1.0", END)

        results = set_local_security_policies()

        if results:
            result_box.insert(END, "\n=====================================================\n")

            result_box.insert(END, "\n".join(results))

            result_box.insert(END, "\n=====================================================\n")

    run_script()

# start screen when the file is ran
def start_screen():
    # clear all widgets for when user returns to the start screen
    for widget in widgets:
        widget.grid_forget()

    global search_directory_button, filetype_search_button, internal_file_search_button, sort_users_button
    
    # buttons that take the user to different screens based on what they want to do 
    search_directory_button = Button(main_window, text="Search a Directory", command=file_name_search_screen)
    search_directory_button.grid(column=1, row=1)
    search_directory_description = Label(main_window, text="Search for files by name  ---->")
    search_directory_description.grid(column=0, row=1)
    widgets.append(search_directory_button)
    widgets.append(search_directory_description)

    filetype_search_button = Button(main_window, text="Search for Filetypes", command=file_type_search)
    filetype_search_button.grid(column=1, row=2)
    filetype_search_description = Label(main_window, text="Search for files by type  ---->")
    filetype_search_description.grid(column=0, row=2)
    widgets.append(filetype_search_button)
    widgets.append(filetype_search_description)

    internal_file_search_button = Button(main_window, text="Search Inside files for keyword", command=internal_file_search_screen)
    internal_file_search_button.grid(column=1, row=3)
    internal_file_search_description = Label(main_window, text="Search for keywords inside files  ---->")
    internal_file_search_description.grid(column=0, row=3)
    widgets.append(internal_file_search_button)
    widgets.append(internal_file_search_description)
    """
        windows_file_comparison = Button(main_window, text="Compare Windows Files", command=compare_windows_files)
        windows_file_comparison.grid(column=1, row=4)
        windows_file_comparison_description = Label(main_window, text="Compare Windows Files to Database  ---->")
        windows_file_comparison_description.grid(column=0, row=4)
        widgets.append(windows_file_comparison)
        widgets.append(windows_file_comparison_description)
    """
    sort_users_button = Button(main_window, text="Sort all Users", command=user_sort_screen)
    sort_users_button.grid(column=1, row=5)
    sort_users_description = Label(main_window, text="Sort users by type, can also delete users  ---->")
    sort_users_description.grid(column=0, row=5)
    widgets.append(sort_users_button)
    widgets.append(sort_users_description)

    set_security_policies_button = Button(main_window, text="Set Local Security Policies", command=set_local_policies)
    set_security_policies_button.grid(column=1, row=6)
    set_security_policies_label = Label(main_window, text="Sets all security policies to standard values  ---->")
    set_security_policies_label.grid(column=0, row=6)
    widgets.append(set_security_policies_button)
    widgets.append(set_security_policies_label)

# sends a msg to the user that explains that the script must be ran as an administrator 
def confirm_administrator():
    messagebox.showwarning("Important Message", "If you were prompted and selected no when the script was ran, restart the script and select yes. If you do not the script will not have full capabilities")

start_screen()
# show msg explaining that the script must be ran as an administrator 
main_window.after(100, confirm_administrator)

main_window.mainloop()
