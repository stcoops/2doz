#Copyright (c) 2024, Github User Stcoops
#All rights reserved.
#This source code is licensed under the BSD-style license found in the
#LICENSE file in the root directory of this source tree. 

import csv
import datetime

class app():
    def __init__(self):
        print("Welcome to 2doz Alpha-V1.1.3 'Half-Pint'. Development still very much in progress x")
        input("Press Enter to start.")
        print("loading Files...")
        try:
            self.load() #This will soon actually load a file lol
            print("Files loaded!")
        except Exception as error_output:
            error(self.error_log, error_output, "X000", "Error Loading files")
            print("Continuing to 2doz...")

        

    def fetch_all(self): #Error codes begin with F,look like FXXX
        try:
            with open(self.file_location, "r", newline='') as file:
                return list(csv.reader(file)) #returns array of the entire csv details to be abstracted for the user
        except Exception: #add an option to create one
            self.file_location = input(error(self.error_log, error_output, "F019", "CSV File not found. Please enter path to file."))



    def load(self):
        self.file_location = "2DoList.csv" #In future this should be fetched from settings.json x
        self.file_cache = self.fetch_all() #saves the data from the file into our cache
        self.task_count = len(self.file_cache) - 1
        self.headers = self.file_cache[0]
        self.error_log=[]



    def main_menu(self):
        while True:
            print("Main Menu")
            prompt = "Select (1): View tasks, (2): Create Task, (3): Settings, or (4): Quit\n"
            menu(prompt, ["1","2","3","4"], self.view_tasks, self.create_task, self.settings_menu, quit)

    def view_tasks(self):
        print("Tasks:")
        index = 0 #NOTE: This is a super shitty solution?? but improved lol??, but needed to skip the header row in the csv file. fix later?
        for row in self.file_cache:
            if index == 0:
                index = 1
                continue
            title_index = row[self.get_attribute_index("Title")]  # weird f string behaviour
            print(f"({index}): {title_index}") #had to assign title_index due to a potential bug in f strings
            #NOTE: see f_strings_bug.py for more information. cba to find a proper fix lmao
            index += 1
        self.select_task()
        return

    def create_task(self):
        task_row = []
        for attribute in self.headers:
            task_row.append(input(f"{attribute}: "))
        self.file_cache.append(task_row)
        self.update_file()

    def settings_menu(self):
        print("placeholder")

    def quit(self):
        quit()


    def select_task(self):
        prompt = "Enter a task number to view it, or hit enter to return to the main menu: "
        choice = input(prompt)
        print("\n")
        #Input sanitizing
        if choice == "":
            return
        try:
            choice = int(choice)
        except Exception as error_output:
            error(self.error_log, error_output, "T009", "Input not of type Integer, returning to main menu.")
            return
        if choice  < 1 or choice > len(self.file_cache)-1: # -1 for header row x
            error(self.error_log, "None", "T013", f"Task number ({choice}) does not exist.")
            return
        #print task details.
        task_data = self.file_cache[choice]
        for index, attribute in enumerate(task_data):
            print(f"{self.file_cache[0][index]}: {attribute}", end=",\n")
        print("\n")
        self.__selected_task_index = choice #important to track this could cause issues
        self.task_menu()
        return
        

    def task_menu(self):
        prompt = "Do you want to (1): Mark as complete, (2): Edit details, (3): Delete task or (4): Return to main menu"
        menu(prompt, ["1","2","3","4"], self.mark_as_complete, self.edit_task, self.delete_task, self.return_)

    def mark_as_complete(self):
        # should be standardized to fetch from settings etc.                  THIS BIT 
        self.file_cache[self.__selected_task_index][self.get_attribute_index("Complete") ] = True
        self.update_file()
        return
    
    def get_attribute_index(self, attribute):
        for index, header in enumerate(self.headers):
            if header == attribute:
                return index
        error(self.error_log, None, "K302", "Attribute is not in file header") #SOlution to change headers in settings
    
    def edit_task(self):
        task_row = []
        for attribute in self.headers:
            task_row.append(input(f"{attribute}: "))
        self.file_cache[self.__selected_task_index] = (task_row)
        self.update_file()
        return

    def delete_task(self):
        self.file_cache.pop(self.__selected_task_index)
        self.update_file()
        return

    def return_(self):
        return
###############################################
#NOTE          CSV INTERACTIONS           NOTE#
###############################################


    def fetch_all(self): #Error codes begin with F,look like FXXX
        with open(self.file_location, "r", newline='') as file:
            return list(csv.reader(file)) #returns array of the entire csv details to be abstracted for the user

    def update_file(self):
        try: #Bulletproof?
            with open(self.file_location, "w", newline='') as file:
                writer = csv.writer(file)
                for row in self.file_cache:
                    writer.writerow((row))
            self.load()
            return
        except Exception as error_output:
            error(self.error_log, error_output, "U107", "Could not update file.")
            return



#This FUNction should be bulletproof now. #famouslastwords #votecasisdead
#prompt is simply the text we show the user to get their input.
#options is an array of the options the user has. must be in same order as functions examples: [0,1,2,3]

def menu(prompt, options, *functions, **kwargs): #menu is a boilerplate for each menu screen
    flag = True
    while flag:
        flag = False
        default = kwargs.get('default', None) #Allows a Default function to be chosen if input is none
        choice = str(input(prompt)) #gets user input #str shouldnt be necessart here
        for function_index, option_iterable in enumerate(options): #option_iterable goes through all possible user choices
            if option_iterable == choice:#for loop matches user input to function index and executes this function
                return (functions[function_index])()
        if choice == "" and default != None:
            functions[default]() #Default function if no input given 
        else:
            print("Invalid Choice")
            flag = True

def error(error_log, raw_output, code, message):
    error_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    error_log.append(f"at {error_time}, {code}: {message}; {raw_output}")
    print(f"Error Code {code}: {message}")
    return
    

if __name__ ==  "__main__":
    try:
        instance = app()
        instance.main_menu()

    except KeyboardInterrupt:
        print("Exiting 2doz due to KB interrupt, Goodbye")
        quit()
    except Exception as error_output:
        error(instance.error_log, error_output, "Z042", "Catastrophic Failure")
        choice = input("Catastrophic Failure, select (1) to view Error Logs or hit Enter to Exit 2doz.")
        if choice == "1":
            for log in instance.error_log:
                print(log)
        else:
            quit()
