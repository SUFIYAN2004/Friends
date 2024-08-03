from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Adjust the URI as needed
db = client["school"]  # Database name
collection = db["students"]  # Collection name

while True:
    user = input("Add, Delete, Show, Showall, or Exit: ").strip().lower()

    if user == "add":
        name = input("Enter the Name: ")

        while True:
            rollno = input("Enter the Rollno: ")

            # Check if the roll number already exists
            existing_student = collection.find_one({"rollno": rollno})
            if existing_student:
                print("Rollno already exists. Please enter a different Rollno.")
            else:
                break  # Rollno is unique, exit the loop

        number = int(input("Enter the Phone Number: "))
        dept = input("Enter the Department: ")
        address = input("Enter the Address: ")

        # Create a document
        student = {
            "name": name,
            "rollno": rollno,
            "number": number,
            "dept": dept,
            "address": address
        }

        # Insert the document into the collection
        result = collection.insert_one(student)
        print("Data added successfully with id:", result.inserted_id)

    elif user == "delete":
        rollno = input("Enter the Rollno to delete: ")

        # Delete the document
        result = collection.delete_one({"rollno": rollno})

        if result.deleted_count > 0:
            print("Data deleted successfully.")
        else:
            print("No record found with that Rollno.")

    elif user == "show":
        rollno = input("Enter the Rollno to show: ")

        # Find the student by rollno
        student = collection.find_one({"rollno": rollno})

        if student:
            print("Student Details:")
            print(f"Name: {student['name']}")
            print(f"Rollno: {student['rollno']}")
            print(f"Phone Number: {student['number']}")
            print(f"Department: {student['dept']}")
            print(f"Address: {student['address']}")
        else:
            print("No record found with that Rollno.")

    elif user == "showall":
        students = list(collection.find())  # Retrieve all documents from the collection and convert to list

        if students:  # Check if the list is not empty
            print("All Students:")
            for student in students:
                print(
                    f"Name: {student['name']}, Rollno: {student['rollno']}, Phone Number: {student['number']}, Department: {student['dept']}, Address: {student['address']}")
        else:
            print("No students found.")

    elif user == "exit":
        print("Exiting the program.")
        break

    else:
        print("Invalid option. Please choose 'Add', 'Delete', 'Show', 'Showall', or 'Exit'.")
