import csv

def view_tasks(file_dir):
        choice = None
        while choice != "0":
            try:
                with open(file_dir, "r", newline='') as file:
                    reader = csv.reader(file)
                    next(reader, None) #skip the Header row
                    print("tasks:")
                    index = 1
                    for line in reader:
                        print(f"({index}): ", end = "")
                        print(line[0])
                        index+=1
                    print("\n")

                    choice = input("Enter a task number to view it, or (0) to return to the main menu: ")
                    print("\n")
                    if  choice == "0":
                        return
                    else:
                        try:
                            task_number = int(choice)
                            display_details(task_number, file_dir)
                        except:
                            print("Invalid selection \n")
                            return
                            
                    
                
            except:
                print("Error Code X002: File not found")
                choice_two = input("Do you want to (1): Create file in local directory? (default) , (2): Create file in a specific directory, or (3): Quit")
                if choice_two == "1" or choice_two == None:
                    try:
                        setup()
                    except:
                        print("Error Code X099: Conflict creating 2DoList.csv. Try creating in a Different directory")
                        return
                elif choice_two == "2":
                    file_dir = input("Path to csv file: ")
                elif choice_two == "3":
                    return


    
def create_task(file_dir):
    header_names = ["task","priority","location","notes"] #Make this adjustable in settings.csv #NOTE
    data = dict(task = input("Title: "), priority = input("Priority? "), location = input("Location? "), notes = input("Additional Notes: "))
    with open(file_dir, "a", newline='') as file:
        writer = csv.DictWriter(file,header_names) #Header names should already be on the csv file
        writer.writerow(data)
        


def setup():
    header_names = ["task","priority","location","notes"]
    print("Creating 2DoList.csv...")
    with open("2DoList.csv", "w", newline='') as file:
        writer = csv.DictWriter(file,header_names)
        writer.writeheader()
        print("Done")



def display_details(task_number, file_dir):
    with open(file_dir, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    for n in range(len(rows[0])):
        print(f"{rows[0][n]}: ",end="")
        print(rows[task_number][n])

    print("\n")
    return



def Main():
    while True:
        print("Main Menu")
        choice = input("Select (1): View tasks, (2): Create Task, or (3): Quit\n")
        while choice != "1" and choice != "2" and choice != "3":
            print("Error Code X001: Invalid selection.")
            choice = input("Select (1): View tasks, (2): Create Task, or (3): Quit\n")

        print("\n")
        if choice == "1":
            view_tasks("2DoList.csv")

        elif choice == "2":
            create_task("2DoList.csv")

        elif choice == "3":
            quit()

if __name__ ==  "__main__":
    print("Welcome to 2doz Version Alpha. Development still very much in progress x")
    choice = input("Select (1) for first-time setup, or hit Enter to skip.")
    if choice == "1":
        try:
            setup()
            print("Setup Complete! Launching 2doz...")
        except:
            print("Error Code X000: Setup Failed")
    else:
        print("Launching 2doz...")
    Main()
