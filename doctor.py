class Doctor:

    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization

    def get_details(self):
        return (
            self.name,
            self.specialization
        )