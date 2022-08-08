# import Data
from Connection.Connection import Connection
from Data.Cattle import Cattle

from datetime import datetime


class System():
    def __init__(self):
        self.conn = Connection()
        self.__Systemdata = None

    def set_Systemdata(self, Systemdata):
        self.__Systemdata = Systemdata

    def get_Systemdata(self):
        return self.__Systemdata

    # CONNECTION WITH DATABASE

    def conexao(self):
        self.conn.initConnection()

    # CREATE FUNCTIONS

    def createNewFarm(self, farm):
        id = self.createNewFarmId()
        sql = f"INSERT INTO farms (farmid,farmname, location) VALUES ({id},'{farm.get_name()}','{farm.get_location()}')"
        self.conn.SqlInsertCommand(sql)
        return id

    def createNewZone(self, zone):
        zone.set_zoneid(self.createNewZoneId(zone.get_farmid()))
        sql = f"INSERT INTO zones (farmid, zoneid, gmd, recoverytime, amountcattlesuported) VALUES ({zone.get_farmid()},{zone.get_zoneid()},{zone.get_gmd()},{zone.get_recoverytime()},{zone.get_amountcattlesuport()})"
        self.conn.SqlInsertCommand(sql)
        return zone.get_zoneid()

    def createNewCattle(self, cattle):
        sql = f"INSERT INTO cattles (earringnumber,farmid, weight, breed, idealweight, zoneid, inputdatefarm,inputdatezone, birth) VALUES ({cattle.get_earringnumber()},{cattle.get_farmid()},{cattle.get_weight()},'{cattle.get_breed()}',{cattle.get_idealweight()},{cattle.get_zoneid()},'{cattle.get_inputdatefarm()}','{cattle.get_inputdatezone()}','{cattle.get_birth()}')"
        self.conn.SqlInsertCommand(sql)
        if self.Cattlesinzone(cattle.get_farmid(), cattle.get_zoneid()) == 1:
            self.updateinputdatezone(
                cattle.get_earringnumber(), self.__Systemdata)

        if self.Cattlesinzone(cattle.get_farmid(), cattle.get_zoneid()) == 1:
            self.updateinputzone(cattle.get_farmid(),
                                 cattle.get_zoneid(), self.__Systemdata)
        return True

    # MOVE FUNCTIONS

    def moveCattle(self, earring, newZone, farmid):

        if not self.CattleFromFarm(farmid, earring):
            return 0

        sql = f"SELECT farmid,zoneid weight FROM cattles WHERE earringnumber={earring}"
        result0 = self.conn.SqlResultCommand(sql)
        farmid = result0[0][0]
        atualzone = result0[0][1]
        check = self.dispzone(farmid, newZone)

        if check > 0:
            sql = f"SELECT inputzone from zones WHERE zoneid={newZone}"
            result1 = self.conn.SqlResultCommand(sql)
            if result1[0][0] == None:
                self.updateinputzone(farmid, newZone, self.__Systemdata)
            sql = f"UPDATE cattles set zoneid = {newZone} WHERE earringnumber={earring}"
            self.conn.SqlInsertCommand(sql)
            self.updateweight(earring, self.__Systemdata)
            self.updateinputdatezone(earring, self.__Systemdata)
        else:
            return 0

        if self.Cattlesinzone(farmid, newZone) == 1:
            self.updateinputzone(farmid, newZone, self.__Systemdata)

        if self.Cattlesinzone(farmid, atualzone) == 0:
            self.updatelastexist(farmid, atualzone, self.__Systemdata)

        return 1

    def moveGroupCattle(self, atualzone, futurezone, farmid):
        sql = f"SELECT earringnumber FROM cattles c JOIN zones z on c.zoneid=z.zoneid and z.zoneid={atualzone} and z.farmid={farmid}"
        result = self.conn.SqlResultCommand(sql)
        countCattles = len(result)
        if countCattles + self.Cattlesinzone(farmid, futurezone) < self.MaxCattlesinzone(farmid, futurezone):
            for cattlenumber in result:
                test = self.moveCattle(cattlenumber[0], futurezone, farmid)
                print(cattlenumber[0], test)
                if test == 0:
                    return 0
        else:
            return 0

        return 1

    # SEARCH FUNCTION

    def searchCattle(self, earring):
        sql = f"SELECT farmid, zoneid, weight, idealweight, breed, inputdatefarm, birth, inputdatezone  FROM cattles where earringnumber={earring}"
        result = self.conn.SqlResultCommand(sql)[0]
        cattle = Cattle()
        cattle.set_earringnumber(earring)
        cattle.set_farmid(result[0])
        cattle.set_zoneid(result[1])
        cattle.set_weight(result[2])
        cattle.set_idealweight(result[3])
        cattle.set_breed(result[4])
        cattle.set_inputdatefarm(result[5])
        cattle.set_birth(result[6])
        cattle.set_inputdatezone(result[7])
        cattle.to_String(self.returnfarmname(cattle.get_farmid()),
                         self.mediumGMDfarm(cattle.get_farmid()))

    # DELETES

    def DeleteCattle(self, earring):
        sql = f"DELETE FROM cattles where earringnumber={earring}"
        self.conn.SqlInsertCommand(sql)

    def DeleteCattlesinZone(self, farmid, zoneid):
        cattleszone = self.listCattlesinzone(farmid, zoneid)
        for cattle in cattleszone:
            self.DeleteCattle(cattle)

    def deleteZone(self, farmid, zoneid):
        sql = f"DELETE FROM zones where farmid={farmid} and zoneid={zoneid}"
        self.conn.SqlInsertCommand(sql)

    def ResetDataBase(self):
        sql = f"DELETE FROM cattles"
        self.conn.SqlInsertCommand(sql)
        sql = f"DELETE FROM zones"
        self.conn.SqlInsertCommand(sql)
        sql = f"DELETE FROM farms"
        self.conn.SqlInsertCommand(sql)
        print("Informacoes Removidas")


# AUXILIAR FUNCTIONS

    # CATTLES

    def Cattlesinzone(self, farm, zone):
        sql = f"SELECT COUNT(earringnumber) FROM cattles where farmid={farm} and zoneid={zone}"
        return self.conn.SqlResultCommand(sql)[0][0]

    def listCattlesinzone(self, farm, zone):
        sql = f"SELECT COUNT(earringnumber) FROM cattles where farmid={farm} and zoneid={zone}"
        result = self.conn.SqlResultCommand(sql)
        earringzone = []
        for earring in result:
            earringzone.append(earring[0])
        return earringzone

    def MaxCattlesinzone(self, farm, zone):
        sql = f"SELECT amountcattlesuported FROM zones where farmid={farm} and zoneid={zone}"
        return self.conn.SqlResultCommand(sql)[0][0]

    def updateinputdatezone(self, earringnumber, date):
        sql = f"UPDATE cattles SET inputdatezone='{date}' WHERE earringnumber = {earringnumber}"
        self.conn.SqlInsertCommand(sql)

    def updateweight(self, earringnumber, day):
        sql = f"SELECT z.gmd,c.inputdatezone,c.weight FROM zones z JOIN cattles c on c.zoneid= z.zoneid and c.earringnumber={earringnumber}"
        result = self.conn.SqlResultCommand(sql)

        gmd = result[0][0]
        inputdatezone = result[0][1]
        weight = result[0][2]
        timeinzone = diffdateNative(inputdatezone, day)
        increment = timeinzone*gmd
        weight += increment
        sql = f"UPDATE cattles set weight = {weight} WHERE earringnumber={earringnumber}"
        self.conn.SqlInsertCommand(sql)

    # ZONES
    def updatelastexist(self, farm, zone, date):
        sql = f"UPDATE zones SET lastexit='{date}' WHERE zoneid= {zone} and farmid = {farm}"
        self.conn.SqlInsertCommand(sql)

    def updateinputzone(self, farm, zone, date):
        sql = f"UPDATE zones SET inputzone='{date}' WHERE zoneid= {zone} and farmid = {farm}"
        self.conn.SqlInsertCommand(sql)

# CHECK FARM, ZONE, CATTLE EXISTS

    # FARM

    def checkFarmNameExist(self, name):
        sql = f"SELECT * FROM farms WHERE farmid in (SELECT farmid FROM farms) and farmname = '{name}'"
        result = self.conn.SqlResultCommand(sql)
        if len(result) == 0:
            return False
        return True

    def returnfarmid(self, name):
        sql = f"SELECT farmid FROM farms WHERE farmid in (SELECT farmid FROM farms) and farmname = '{name}'"
        return self.conn.SqlResultCommand(sql)[0][0]

    def checkFarmExist(self, idfarm):
        sql = f"SELECT * FROM farms WHERE farmid in (SELECT farmid FROM farms) and farmid = {idfarm}"
        result = self.conn.SqlResultCommand(sql)
        if len(result) == 0:
            return False
        return True

    def mediumGMDfarm(self, farmid):
        sql = f"SELECT AVG(gmd) FROM zones WHERE farmid ={farmid}"
        result = self.conn.SqlResultCommand(sql)
        if result[0][0] != None:
            return result[0][0]
        return 0

    def returnfarmname(self, farmid):
        sql = f"SELECT farmname FROM farms WHERE farmid = {farmid}"
        return self.conn.SqlResultCommand(sql)[0][0]

    # ZONE
    def checkZoneExist(self, idfarm, idzone):
        sql = f"SELECT * FROM zones WHERE zoneid in (SELECT zoneid FROM zones where farmid={idfarm}) and zoneid = {idzone}"
        result = self.conn.SqlResultCommand(sql)
        if len(result) == 0:
            return False
        return True

    # CATTLE
    def cattleExist(self, earringnumber):
        sql = f"SELECT * FROM cattles WHERE earringnumber={earringnumber}"
        result = self.conn.SqlResultCommand(sql)
        if len(result) == 0:
            return False
        return True

    def CattleFromFarm(self, idfarm, earringnumber):
        sql = f"SELECT * FROM cattles WHERE earringnumber={earringnumber} and farmid={idfarm}"
        result = self.conn.SqlResultCommand(sql)
        if len(result) == 0:
            return False
        return True

# GENERATE NEW ID's

    def createNewZoneId(self, farmid):
        sql = f"SELECT MAX(zoneid) FROM zones z WHERE z.farmid = {farmid}"
        id = self.conn.SqlResultCommand(sql)
        if id[0][0] == None:  # id[0][0] para pegar o primeiro elemento da primeira tupla resultado da funcao de agregacao
            return 1
        return (id[0][0]+1)

    def createNewFarmId(self):
        # funcao de agregacao retorna uma uma lista com uma tupla de 1 elemento
        sql = 'SELECT MAX(farmid) FROM farms'
        id = self.conn.SqlResultCommand(sql)
        if id[0][0] == None:  # id[0][0] para pegar o primeiro elemento da primeira tupla resultado da funcao de agregacao
            return 1
        return (id[0][0]+1)


# VISUAL FUNCTIONS

    def listallCattles(self):
        sql = f"SELECT earringnumber, weight FROM cattles"
        result = self.conn.SqlResultCommand(sql)
        if len(result) > 0:
            print("---------------GADOS--------------")
            for i in result:
                print(f"Gado {i[0]} peso Atual {i[1]} Kg")
            print("-----------------------------")
        else:
            print("Nao ha gados")

    def listallcattlesfarm(self, idfarm):
        sql = f"SELECT earringnumber, weight FROM cattles WHERE farmid ={idfarm} "
        result = self.conn.SqlResultCommand(sql)
        if len(result) > 0:
            print(
                f"---------GADOS  Fazenda {self.returnfarmname(idfarm)}-----------")
            for i in result:
                print(f"Gado {i[0]} peso Atual {i[1]} Kg")
            print("-----------------------------------------------------")

        else:
            print(f"Nao ha gados na Fazenda {self.returnfarmname(idfarm)}")

    def listallcattleszone(self, idfarm, idzone):
        sql = f"SELECT earringnumber, weight FROM cattles WHERE farmid ={idfarm} and zoneid={idzone} "
        result = self.conn.SqlResultCommand(sql)
        if len(result) > 0:
            print(
                f"------GADOS Fazenda {self.returnfarmname(idfarm)} Zona {idzone}---------")
            for i in result:
                print(f"Gado {i[0]} peso Atual {i[1]} Kg")

            print("-----------------------------------------------------")
        else:
            print(f"Nao ha gados na Zona {idzone}")

    def listallfarms(self):
        sql = f"SELECT farmid, farmname, location FROM farms "
        result = self.conn.SqlResultCommand(sql)

        print("\n--------------FAZENDAS CADASTRADAS---------------")
        for i in result:
            print(f"FARM {i[1]}, localizacao: {i[2]}")

        print("-------------------------------------------------\n")

    def generalViewZone(self, farmid, zoneid):  # TODO
        sql = f"SELECT farmid, zoneid, gmd, recoverytime, amountcattlesuported, lastexit, inputzone FROM zones WHERE farmid={farmid} and zoneid={zoneid} "
        result = result = self.conn.SqlResultCommand(sql)[0]
        print(f"--------------ZONA {result[1]}---------------------")
        print(f"Quantidade de animais Suportados: {result[4]}")
        print(
            f"Quantidade no Aminais Alocados: {self.Cattlesinzone(farmid,zoneid)}")
        print(f"GMD: {result[2]:.2f}kg")
        print(f"ultima entrada de Animais: {result[6]}")
        print(f"ultima saida de animais: {result[5]} ")
        if self.Cattlesinzone(farmid, zoneid) > 0:
            print(f"Status: Zona Alocada")
        elif diffdateNative(result[5], self.__Systemdata) < result[3]:
            print(f"Status: Zona Em Recuperacao ")
        else:
            print(f"Status: Zona Disponivel")
        print("-----------------------------------------------------")

    def generalViewFam(self, farmid):
        sql = f"SELECT farmid, zoneid, gmd, recoverytime, amountcattlesuported, lastexit, inputzone  FROM zones WHERE farmid ={farmid}  "
        result = self.conn.SqlResultCommand(sql)
        recovery = 0
        totalzones = len(result)

        for i in result:
            print(i[5], self.__Systemdata, i[3])
            if self.dispzone(i[0], i[1]) == 0:
                recovery += 1

        sql = f"SELECT earringnumber, weight, idealweight   FROM cattles WHERE farmid ={farmid}  "
        result = self.conn.SqlResultCommand(sql)
        slaughter = 0
        for i in result:
            if i[1] >= i[2]:
                slaughter += 1

        totalcattles = len(result)
        print(
            f"---------Fazenda {self.returnfarmname(farmid)} VISAO GERAL-----------")
        print(f"Total de Zonas na Fazenda: {totalzones}")
        print(f"Total de Zonas em recuperacao: {recovery}")
        print(f"Total de Animais na Fazenda: {totalcattles}")
        print(f"Total de Animais na Fazenda Pronto para Abate: {slaughter}")
        print(f"GMD da fazenda {self.mediumGMDfarm(farmid):.2f}Kg")
        print("----------------------------------------------")

# OTHERS FUNCTIONS

    def dispzone(self, idfarm, idzone):

        sql1 = f"SELECT amountcattlesuported,lastexit,recoverytime FROM zones where farmid={idfarm} and zoneid={idzone} "
        result = self.conn.SqlResultCommand(sql1)
        if result[0][1] != None:
            if diffdateNative(result[0][1], self.__Systemdata) < int(result[0][2]):
                return 0
        max = result[0][0]
        sql2 = f"SELECT COUNT(zoneid) FROM cattles where farmid={idfarm} and zoneid={idzone} "
        countCattles = self.conn.SqlResultCommand(sql2)[0][0]
        disp = max-countCattles
        return disp

# GENERICS DATE DIFERENCE AND VALIDATION FORMAT


def diffdateNative(d1, d2):
    if checkDataFormat(d1) and checkDataFormat(d2):
        # '%Y-%m-%d'
        dt1 = datetime.strptime(d1, '%d/%m/%Y')
        dt2 = datetime.strptime(d2, '%d/%m/%Y')

        return abs((dt2-dt1).days)
    else:
        return 0


def checkDataFormat(date):
    if date is None:
        return False
    if len(date) != 10:
        return False
    if date[2] != '/':
        return False
    if date[5] != '/':
        return False
    dia = int(date[0])*10 + int(date[1])
    mes = int(date[3])*10 + int(date[4])
    ano = int(date[6])*1000 + int(date[7])*100+int(date[8])*10 + int(date[9])

    if mes > 12:
        return False

    if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
        if dia > 31:
            return False
    elif mes == 2:
        if ((ano % 4 == 0 and ano % 100 != 0) or (ano % 100 == 0 and ano % 400 == 0)):
            if dia > 29:
                return False
        elif dia > 28:
            return False
    elif dia > 30:
        return False

    return True
