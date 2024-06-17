from models.exceptions import InvalidAccountInformationException


class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if isinstance(value, str) and value:
            self._first_name = value
        else:
            raise InvalidAccountInformationException("First Name must be non-empty strings!")
        
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if isinstance(value, str) and value:
            self._last_name = value
        else:
            raise InvalidAccountInformationException("Last Name must be non-empty strings!")
        

    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if isinstance(value,int) and value > 0:
            self._age = value
        else:
            raise InvalidAccountInformationException("Age must be a positive integer")
