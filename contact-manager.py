class Contact:
    def __init__(self, name, age, number):
        self.name = name
        self.age = age
        self.number = number

    def __str__(self):
        return f"{self.name} -> Number: {self.number} Age: {self.age} year(s)."
      
contact_collection = {}


def add_contact(name, age, number):
    contact = Contact(name, age, number)
    contact_collection[name] = contact
    print(f"{name} has been added to the collection.")

def remove_contact(name):
    try:
        del contact_collection[name]
        print(f"{name} has been removed from the collection.")
    except KeyError:
        print(f"{name} is not in the collection.")


def list_contacts():
    if len(contact_collection) == 0:
        print("No contacts in the collection.")
    else:
        for contact in contact_collection.values():
            print(contact)

while True:
    print("\nContact Manager")
    print("1. Add Contact")
    print("2. Remove Contact")
    print("3. List Contacts")
    print("4. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        name = input("Enter contacts's name: ")
        try:
            age = int(input("Enter contact's age: "))
        except ValueError:
            print("Invalid age. Please enter a valid number.")
            continue
        number = input("Enter contact's number: ")
        add_contact(name, age, number)
    elif choice == 2:
        name = input("Enter pet's name: ")
        remove_contact(name)
    elif choice == 3:
        list_contacts()
    elif choice == 4:
        break
    else:
        print("Invalid choice. Please try again.")
