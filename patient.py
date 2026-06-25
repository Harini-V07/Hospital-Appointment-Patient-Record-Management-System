class Patient:

    def __init__(self, name, age, gender, phone):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone

    def get_details(self):
        return (
            self.name,
            self.age,
            self.gender,
            self.phone
        )