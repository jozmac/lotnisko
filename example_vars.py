class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self._variable = 42
        self.__variable = 42
        self.method()
        self._method()
        self.__method()

    def method(self):
        self.variable_0 = 42

    def _method(self):
        self.variable_1 = 42

    def __method(self):
        self.variable_2 = 42


# Create an instance of the Person class
john = Person("John Doe", 25)

# Use vars() to get the dictionary of object attributes
john_attributes = vars(john)

# Display the attributes
print("Object attributes using vars():")
print(john_attributes)

# Modify an attribute using the dictionary obtained from vars()
john_attributes["age"] = 26

# Display the modified object
print("\nModified object using vars():")
print("Name:", john.name)
print("Age:", john.age)
print("Private variable:", john._Person__variable)

# if __name__ == "__main__":
#     print("++++++++++++++++++++++++")
