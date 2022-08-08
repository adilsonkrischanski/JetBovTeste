class Cattle():
    def __init__(self):
        self.__farmid = None
        self.__zoneid = None
        self.__earringnumber = None
        self.__weight = None
        self.__idealweight = None
        self.__breed = None

        self.__inputdatefarm = None
        self.__birth = None
        self.__inputdatezone = None

    def set_farmid(self, farmid):
        self.__farmid = farmid

    def set_zoneid(self, zoneid):
        self.__zoneid = zoneid

    def set_earringnumber(self, earringnumber):
        self.__earringnumber = earringnumber

    def set_weight(self, weight):
        self.__weight = weight

    def set_idealweight(self, idealweight):
        self.__idealweight = idealweight

    def set_breed(self, breed):
        self.__breed = breed

    def set_inputdatefarm(self, inputdatefarm):
        self.__inputdatefarm = inputdatefarm

    def set_birth(self, birth):
        self.__birth = birth

    def set_inputdatezone(self, inputdatezone):
        self.__inputdatezone = inputdatezone

    def get_farmid(self):
        return self.__farmid

    def get_zoneid(self):
        return self.__zoneid

    def get_earringnumber(self):
        return self.__earringnumber

    def get_weight(self):
        return self.__weight

    def get_idealweight(self):
        return self.__idealweight

    def get_breed(self):
        return self.__breed

    def get_inputdatefarm(self):
        return self.__inputdatefarm

    def get_birth(self):
        return self.__birth

    def get_inputdatezone(self):
        return self.__inputdatezone

    def to_String(self, farmname, gmdfarm):
        print("----------------------------------------------------")
        print(f"Numero de Identicacao (BRINCO) {self.__earringnumber}")
        print(f"Nascimento em {self.__birth}")
        print(f"Fazenda Propietaria {farmname}")
        print(f"Zona de Alocacao Numero:{self.__zoneid}")
        print(f"Peso Atual {self.__weight} Kg")
        print(f"Peso Ideal Para Abate: {self.__idealweight} Kg")
        print(f"Data de entrada Na Fazenda: {self.__inputdatefarm}")
        print(f"Entrou na Zona {self.__zoneid} no Dia {self.__inputdatezone}")
        if self.timeidealweight(gmdfarm) > 0:
            print(
                f"Faltam Aproximadamente {self.timeidealweight(gmdfarm)}dias para atingir o peso de Ideal Abate")
        else:
            print("Gado pronto para Abate")
        print("----------------------------------------------------\n")

    def timeidealweight(self, gmdfarm):
        missingweight = self.__idealweight - self.__weight
        return missingweight/gmdfarm + 1
