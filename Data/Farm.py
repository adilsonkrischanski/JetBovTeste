class Farm():
    def __init__(self):
        self.__name = None
        self.__id = None
        self.__location = None

    def set_name(self, name):
        self.__name = name

    def set_id(self, id):
        self.__id = id

    def set_location(self, location):
        self.__location = location

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id

    def get_location(self):
        return self.__location
