# This is the awesome github version. HI MOM
# In this assignment, you will design and implement a Rolodex-style application in Python that allows users to manage information about people (e.g., name and contact details). 
# The program will include the following features:
#1. A Person class with attributes for the person's name and contact information.
#2. A ContactInfo class to represent individual contact details (like email, phone, etc.).
#3. Methods for serializing and deserializing the Person class and its associated contacts to and from a file.
#4. Attributes to manage and store multiple contacts per person, with indexing for primary contacts and addresses.
#5. The ability to store all data (both people and their contact info) in a single file on serialization.

import json

class ContactInfo:
    def __init__(self, contact_type: str, contact_value: str):
        self.__contact_type = contact_type
        self.contact_value = contact_value
    
    def __str__(self):
        return f"{self.__contact_type}: {self.contact_value}"
    
    def serialize(self):
        return {
            "type": "ContactInfo",
            "contact_type": self.__contact_type,
            "contact_value": self.contact_value
        }
    
    #creates a contactInfo object, removes things from the dictionary
    def deserialize(self, data: dict):
        return ContactInfo(data["contact_type"], data["contact_value"])
    
class Person:
    def __init__(self, first_name: str, last_name: str, primeContactIndex:int=None, primeAddressIndex:int=None):
        self.first_name = first_name
        self.last_name = last_name
        self.contacts = []
        self.primary_contact_index = primeContactIndex
        self.primary_address_index = primeAddressIndex
    
    def add_contact(self, contact: ContactInfo, set_primary: bool = False):
        self.contacts.append(contact)
        
        #if no primary contact exists, set the first contact as primary (if not type "address")
        if self.primary_contact_index is None and contact.__contact_type != "address":
            self.primary_contact_index = len(self.contacts) - 1
        
        if set_primary:
            if contact.__contact_type == "address":
                self.primary_address_index = len(self.contacts) - 1
            else:
                self.primary_contact_index = len(self.contacts) - 1
    
    #if statement to check if the index is valid
    def get_contact(self, index: int):
        if 0 <= index < len(self.contacts):
            return self.contacts[index]
        return None
    
    def set_primary_contact(self, index: int):
        if 0 <= index < len(self.contacts):
            if self.contacts[index].contact_type != "address":
                self.primary_contact_index = index
    
    def set_primary_address(self, index: int):
        if 0 <= index < len(self.contacts):
            if self.contacts[index].contact_type == "address":
                self.primary_address_index = index
    
    #Source: https://docs.python.org/3/library/pickle.html
    #Why is it called "pickle"
    def serialize(self):
        return {
            "type": "Person",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "contacts": [contact.serialize() for contact in self.contacts],
            "primary_contact_index": self.primary_contact_index,
            "primary_address_index": self.primary_address_index
        }
    
    def deserialize(self, dct: dict):
        person = Person(dct["first_name"], dct["last_name"])
        person.contacts = [ContactInfo().deserialize(c) for c in dct["contacts"]]
        person.primary_contact_index = dct["primary_contact_index"]
        person.primary_address_index = dct["primary_address_index"]
        return person
    
#Source: https://docs.python.org/3/library/json.html
def save_to_file(people: list, filename: str = "rolodex.json"):
    #serializes a list of Person objects to a JSON file.
    serialized_people = [person.serialize() for person in people]
    with open(filename, "w") as file:
        json.dump(serialized_people, file)
    print(f"Data saved to {filename}")

def load_from_file(filename: str = "rolodex.json"):
    #deserializes Person objects from a JSON file.

    #I added the try/except to try and fix any errors what would occur when there was no file created before running this code.
    #This mainly happens if you try and open the program for the first time, when there is no file present.
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        people = [Person("", "").deserialize(person_data) for person_data in data]
        print(f"Data loaded from {filename}")
        return people
    except FileNotFoundError:
        print(f"File {filename} not found.")
        #returns a list to start over with
        return []
    
def main():
    people = load_from_file()
    
    while True:
        print("\n--- Cool, and Epic Rolodex Application ---")
        print("1. Create a new person")
        print("2. Add contact to a person")
        print("3. View person's contacts")
        print("4. Set primary contact")
        print("5. Set primary address")
        print("6. Save and exit")
        print("7. Exit without saving")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            person = Person(first_name, last_name)
            people.append(person)
            print(f"Person '{first_name} {last_name}' created.")
            input("Click enter to continue")
        
        elif choice == "2":
            if not people:
                print("No people in the rolodex. Create a person first.")
                input("Click enter to continue")
                continue
            
            print("\nSelect a person:")
            for i, person in enumerate(people):
                print(f"{i}. {person.first_name} {person.last_name}")
            
            person_index = int(input("Enter person index: "))
            if 0 <= person_index < len(people):
                contact_type = input("Enter contact type (email, phone, address): ")
                contact_value = input("Enter contact value: ")
                contact = ContactInfo(contact_type, contact_value)
                
                set_primary = input("Set as primary? (yes/no): ").lower() == "yes"
                people[person_index].add_contact(contact, set_primary)
                print(f"Contact added to {people[person_index].first_name}.")
                input("Click enter to continue")
            else:
                print("Invalid person index.")
                input("Click enter to continue")
        
        elif choice == "3":
            if not people:
                print("No people in the rolodex.")
                input("Click enter to continue")
                continue
            
            print("\nSelect a person:")
            for i, person in enumerate(people):
                print(f"{i}. {person.first_name} {person.last_name}")
            
            person_index = int(input("Enter person index: "))
            if 0 <= person_index < len(people):
                person = people[person_index]

                print(f"\nContacts for {person.first_name} {person.last_name}: ")
                for i, contact in enumerate(person.contacts):
                    primary_marker = ""
                    if i == person.primary_contact_index and contact.serialize()["contact_type"] != "address":
                        primary_marker = " (PRIMARY CONTACT)"
                    elif i == person.primary_address_index and contact.serialize()["contact_type"] == "address":
                        primary_marker = " (PRIMARY ADDRESS)"
                    print(f"{i}. {contact}{primary_marker}")
                input("\nClick enter to continue")
            else:
                print("Invalid person index.")
                input("Click enter to continue")
        
        elif choice == "4":
            if not people:
                print("No people in the rolodex.")
                continue
            
            print("\nSelect a person:")
            for i, person in enumerate(people):
                print(f"{i}. {person.first_name} {person.last_name}")
            
            person_index = int(input("Enter person index: "))
            if 0 <= person_index < len(people):
                person = people[person_index]
                contact_index = int(input("Enter contact index to set as primary: "))
                person.set_primary_contact(contact_index)
                print("Primary contact updated.")
                input("Click enter to continue")
            else:
                print("Invalid person index.")
                input("Click enter to continue")
        
        elif choice == "5":
            if not people:
                print("No people in the rolodex.")
                input("Click enter to continue")
                continue
            
            print("\nSelect a person:")
            for i, person in enumerate(people):
                print(f"{i}. {person.first_name} {person.last_name}")
            
            person_index = int(input("Enter person index: "))
            if 0 <= person_index < len(people):
                person = people[person_index]
                contact_index = int(input("Enter address contact index to set as primary: "))
                person.set_primary_address(contact_index)
                print("Primary address updated.")
                input("Click enter to continue")
            else:
                print("Invalid person index.")
                input("Click enter to continue")
        
        elif choice == "6":
            save_to_file(people)
            print("Data saved. Exiting...")
            break
        
        elif choice == "7":
            print("Exiting without saving...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()