"""Practicing Object Oriented Programming For Ramp Backend First Round"""

"""
Todos:
    inheritence
    enumerated classes
    constructors -> done
    destructors -> done
    class vs static -> easy
"""
# imports
from enum import Enum


# define enumerated classes
class Size(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Color(Enum):
    BLACK = "black"
    BROWN = "brown"
    WHITE = "white"


class Animal:
    entity = "animal"

    # Constructor
    def __init__(self, name, species, size, color):
        self.name = name
        self.species = species
        self.size = size
        self.color = color
        self.alive = True

    # Destructor
    def __del__(self):
        self.kill()

    def the_color(self):
        """Returns the value of the enumerated class"""
        return self.color.value

    def kill(self):
        """Kills the animal :D"""
        self.alive = False
        print(self.name + " has been killed :(")

    def is_alive(self):
        if self.alive:
            print(self.name + " is alive")
        else:
            print(self.name + " is dead")

    def what_am_i(self):
        if not self.alive:
            print("I am simply dead.")
        else:
            print("I am an " + self.entity)


dog = Animal("steve", "dog", Size.LARGE, Color.BLACK)
print(dog.the_color())
dog.what_am_i()
dog.is_alive()
dog.kill()
dog.what_am_i()
