#Copyright (c) 2024, Github User Stcoops
#All rights reserved.
#This source code is licensed under the BSD-style license found in the
#LICENSE file in the root directory of this source tree. 

#Imports
import json
import csv
import datetime
import os
from pathlib import Path

class app():

###############################################
#NOTE           LOADING/STARTUP           NOTE#
###############################################

    def __init__(self):
        self.file_cache = []
        #Initial Startup
        print("Welcome to 2doz Alpha-V1.1.3 'Half-Pint'. Development still very much in progress x")
        input("Press Enter to start.")
        os.chdir(Path.home())
        try:
            os.chdir("2doz")
            
        except FileNotFoundError:
            print("2doz Folder not found, launching first time setup...")
            self.first_time_setup()

        except Exception as error_output:
            error(error_log, error_output, "I020", "Could not change directory.")
        
        self.file_cache = []

        print("loading settings...")
        self.load_settings()

        print("loading Files...")
        print(self.file_location)
        self.load_to_do() #saves the data from the file into our cache
        print("file loaded")
        self.task_count = len(self.file_cache) - 1
        self.headers = self.file_cache[0]
        print("init complete.")
            

   
        

    def load_to_do(self): #Error codes begin with F,look like FXXX
        try:
            with open(self.file_location, "r", newline='') as file:
                self.file_cache = list(csv.reader(file)) #returns array of the entire csv details to be abstracted for the user
        except Exception: #add an option to create one
            self.file_location = input(error(error_log, error_output, "F019", "CSV File not found. Please enter path to file."))




    def load_settings(self):
        #handles loading the settings.json file, fairly elegantly compared to previous versions
        #More detailed description to follow?
        #
        try:
            with open("settings.json", "r", encoding = "UTF-8") as settings_file:
                self.settings = json.load(settings_file) #######
            
        except FileNotFoundError:
            error(error_log, "FileNotFoundError", "S808", "Settings file not found")
            return


        #NOTE Unsure whether to create a settings file, load defaults or make user specify one, maybe a menu() with all options is necessary with defaults as a default option?
        #Loading these as and when throuhout the program to reduce RAM usage. This could be optimised by loading all settings on startup.
    
        print("settings load complete")
        self.file_location = str(self.settings.get("lists")[0])
        print(self.file_location)
        return



    def first_time_setup(self):
        #Creates all files required, and fills them with default values that cause no problems 
        #Detailed description to follow

        #create a directory to host to do lists and settings
        try:
            os.mkdir("2doz")
        except FileExistsError:
            print("2doz directory already exists")

        os.chdir("2doz")
        #Create both files
        

        with open("settings.json", "x") as settings_file:
            print(f"settings.json created in {os.getcwd()}")

        list_name = str(input("Enter To-Do list name or hit (Enter) for default:\n"))
        if list_name == "":
            list_name = "to-do"
        self.create_file(list_name)

        with open("settings.json", "w", encoding = "UTF-8") as settings_file:
            json.dump(settings_defaults_dict, settings_file)

        self.load_settings()

        #with open     
        

###############################################
#NOTE            MAIN MENUS               NOTE#
###############################################



    def main_menu(self):
        while True:
            print("Main Menu")
            prompt = "(1): View tasks, (2): Create Task, (3): Settings, or (4): Quit:\n"
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
        prompt = "Enter a task number to view it, or hit enter to return to the main menu:\n "
        choice = input(prompt)
        print("\n")
        #Input sanitizing
        if choice == "":
            return
        try:
            choice = int(choice)
        except Exception as error_output:
            error(error_log, error_output, "T009", "Input not of type Integer, returning to main menu.")
            return
        if choice  < 1 or choice > len(self.file_cache)-1: # -1 for header row x
            error(error_log, "None", "T013", f"Task number ({choice}) does not exist.")
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
        complete_prefix = ""
        if (self.file_cache[self.__selected_task_index][self.get_attribute_index("Complete")]) == "True": #see NOTE in toggle_complete
            complete_prefix = "in"
        prompt = f"(1): Mark as {complete_prefix}complete, (2): Edit details, (3): Delete task or (4): Return to main menu:\n"
        menu(prompt, ["1","2","3","4"], self.toggle_complete, self.edit_task, self.delete_task, self.return_)
        return



    def toggle_complete(self):
        # should be standardized to fetch from settings etc.                  THIS BIT 
        if self.file_cache[self.__selected_task_index][self.get_attribute_index("Complete")] == "True": 
            self.file_cache[self.__selected_task_index][self.get_attribute_index("Complete")] = "False"
        else: #NOTE Would be much better to use boolean or binary for this than string, but will be implemented along with settings
            self.file_cache[self.__selected_task_index][self.get_attribute_index("Complete")] = "True"
        self.update_file()
        return
    


    def get_attribute_index(self, attribute):
        for index, header in enumerate(self.headers):
            if header == attribute:
                return index
        error(error_log, None, "K302", "Attribute is not in file header") #SOlution to change headers in settings
    


    def edit_task(self):
        print("Enter details to change, no input will keep previous details.")
        task_row = []
        for index, attribute in enumerate(self.headers):
            change = input(f"{attribute}: ")
            if change != "":
                task_row.append(change)
            else:
                task_row.append(self.file_cache[self.__selected_task_index][index])
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
        try:
            with open(self.file_location, "r", newline='') as file:
                try:
                    return list(csv.reader(file)) #returns array of the entire csv details to be abstracted for the user
                except Exception as error_output:
                    error(error_log, error_output, "F097", "CSV File exists but could not be read")
        
        except FileNotFoundError as error_output: #change exception to if File not found then use a menu and create_file to rectify
            error(error_log, error_output, "F902", " CSV File not found")
            #for dev purposes only
            for log in error_log:
                print(log)
            #end of dev purposes
            prompt = "(1)(default): Create file in current working directory, (2): Create file in Specified directory, (3): Specify new path to file.\n"
            menu(prompt, [1,2,3],self.create_file, self.dev_placeholder, self.dev_placeholder, default=self.create_file)


    def update_file(self):
        try: #Bulletproof?
            with open(self.file_location, "w", newline='') as file:
                writer = csv.writer(file)
                for row in self.file_cache:
                    writer.writerow((row))
            
            self.load_to_do()
            return
        
        except Exception as error_output:
            error(error_log, error_output, "U107", "Could not update file.")
            return


    def create_file(self,list_name):
        with open(f"{list_name}.csv", "x") as list_file:
            print(f"{list_name}.csv created in {os.getcwd()}")
                    
        self.file_location = os.sep.join([os.getcwd(), f"{list_name}.csv"]) #change current to do list path to this
        settings_defaults_dict.get("lists").append(self.file_location)
        self.file_cache.append(settings_defaults_dict.get("headers"))
        self.update_file()
        return

    def dev_placeholder(self):
        print("placeholder\n")
        return
    


###############################################
#NOTE        NON-CLASS FUNCTIONS          NOTE#
###############################################



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
    print(f"Error Code {code}: {message}\n")
    return


#GLOBAL variables are bad right?

global settings_defaults_dict #this doesnt need to be global
settings_defaults_dict = {
    'lists': [],
    'headers': ["Title","Priority","Complete","Date","Time","Location","Notes"]
    }


global error_log #this might need to be global
error_log = []

    

if __name__ ==  "__main__":
    try:
        instance = app()
        instance.main_menu()

    except KeyboardInterrupt:
        print("Exiting 2doz due to KB interrupt, Goodbye")
        quit()
    except Exception as error_output:
        error(error_log, error_output, "Z042", "Catastrophic Failure")
        #x = 1 / 0
        choice = input("Catastrophic Failure, select (1) to view Error Logs first or hit Enter to quit.")
        if choice == "1":
            for log in error_log:
                print(log)
        else:
            quit()
