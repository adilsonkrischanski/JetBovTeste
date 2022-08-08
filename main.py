from system import System
from system import checkDataFormat
from Data.Zone import Zone
from Data.Cattle import Cattle
from Data.Farm import Farm
from prints import farmMenu
from prints import principalMenu
from prints import instructions
from prints import welcome
from prints import exit


if __name__ == '__main__':

    welcome()
    instructions()
    s = System()
    systemdate = None

    print("Insira a Data de Hoje DD/MM/AAAA")
    systemdate = input()
    while not checkDataFormat(systemdate):
        print("Data Incosistente")
        print("Por Favor insira Novamente")
        print("DD/MM/AAAA")
        systemdate = input()

    s.set_Systemdata(systemdate)
    opition = 1

    while opition != 0:
        farmMenu()
        opition = int(input())

        if opition == 1:
            instructions()
        elif opition == 2:
            print("Para Cadastrar uma Fazenda Infome o Nome e a Localização")
            farmname = input("Nome: ").upper()
            farmlocation = input("Localizacao: ").upper()
            if not s.checkFarmNameExist(farmname):
                newfarm = Farm()
                newfarm.set_name(farmname)
                newfarm.set_location(farmlocation)
                print(newfarm.get_location(), newfarm.get_name())
                test = s.createNewFarm(newfarm)
                if test:
                    print("Fazenda Criada Com sucesso")
                else:
                    print("Ocorreu um erro interno, Tente Novamente")
            else:
                print(
                    f"Nao foi possivel criar, Ja existe uma fazenda chamada {farmname}")

        elif opition == 3:
            print("Para entrar em uma fazenda digite Nome da fazenda")
            farmname = input("Nome: ").upper()
            if s.checkFarmNameExist(farmname):
                farmid = s.returnfarmid(farmname)

                while opition != 0:
                    principalMenu()
                    opition = int(input())
                    if opition == 1:
                        newzone = Zone()
                        newzone.set_farmid(farmid)
                        newzone.set_amountcattlesuport(
                            int(input("Quantos Animais essa zona Suporta: ")))
                        newzone.set_gmd(
                            float(input("Qual o Ganho Medio Diario em Kg dessa zona: ")))
                        newzone.set_recoverytime(int(
                            input("Qual o tempo de reuperacao da zona apos a saida dos animais (dias): ")))
                        test = s.createNewZone(newzone)
                        print(f"Zona numero {test} Criada com sucesso")

                    elif opition == 2:
                        cattle = Cattle()
                        cattle.set_earringnumber(
                            int(input("Insira o numero do Brinco: ")))
                        if not s.cattleExist(cattle.get_earringnumber()):
                            cattle.set_breed(
                                input("Qual a Raca do gado: ").upper())
                            cattle.set_idealweight(
                                float(input("Qual o peso ideal para o abate dessa raca: ")))
                            cattle.set_weight(
                                float(input("Qual o peso atual do gado: ")))
                            cattle.set_birth(
                                input("Data de nascimento (DD/MM/AAAA): ").upper())
                            while not checkDataFormat(cattle.get_birth()):
                                print("Data Incosistente")
                                print("Por Favor insira Novamente")
                                cattle.set_birth(
                                    input("Data de nascimento (DD/MM/AAAA): ").upper())
                            cattle.set_farmid(farmid)
                            cattle.set_zoneid(int(input("Zona de Alocacao:")))
                            while not(s.checkZoneExist(farmid, cattle.get_zoneid()) and s.dispzone(farmid, cattle.get_zoneid()) > 0):
                                print(
                                    "Zona indisponivel ou não cadastrada, tente novamente")
                                cattle.set_zoneid(
                                    int(input("Zona de Alocacao:")))

                            cattle.set_inputdatefarm(s.get_Systemdata())
                            cattle.set_inputdatezone(s.get_Systemdata())
                            s.createNewCattle(cattle)

                            print("Gado cadastrado com sucesso")

                        else:
                            print("Brinco ja existente")

                    elif opition == 3:
                        number = int(
                            input("Insira o numero do Brinco que deseja mover: "))
                        newzone = int(
                            input("Insira o numero da zona para a qual deseja mover mover: "))
                        test = s.moveCattle(number, newzone, farmid)
                        if test == 1:
                            print("Gado Movido com sucesso")
                        else:
                            print("Zona de destino indisponivel")

                    elif opition == 4:
                        atualzone = int(
                            input("Insira o numero da zona atual: "))
                        newzone = int(
                            input("Insira o numero da zona para a qual deseja mover mover: "))

                        if s.checkZoneExist(farmid, atualzone) and s.checkZoneExist(farmid, newzone):
                            test = s.moveGroupCattle(
                                atualzone, newzone, farmid)
                            if test:
                                print("Gados Movidos com Sucesso")
                            else:
                                print("Zona de destino indisponivel")
                        else:
                            print(
                                "Não foi possivel realizar o translado, por favor verifique as zonas")

                    elif opition == 5:
                        earringnumber = int(
                            input("Insira o numero do Brinco que deseja Deletar: "))
                        if s.CattleFromFarm(farmid, earringnumber):
                            s.DeleteCattle(earringnumber)
                            print("Gado Deletado Com Sucesso")
                        else:
                            print("Este Gado não exite em sua fazenda ")

                    elif opition == 6:
                        zone = int(
                            input("Insira o numero da Zona que deseja Deletar: "))
                        if not s.checkZoneExist(farmid, zone):
                            print("Zona Inserida nao existe na Fazendo")
                        else:
                            if s.Cattlesinzone(farmid, zone) > 0:
                                var = int(input(
                                    "Esta Zona tem Animais, para Realocalos digite (1) para deletalos digite (0): "))
                                if var == 0 or var == 1:
                                    if var:
                                        newzone = int(
                                            input("Insira o numero da zona para a qual deseja mover mover: "))
                                        test = s.moveGroupCattle(
                                            zone, newzone, farmid)
                                        if test == 1:
                                            print("Gados Movidos com Sucesso")
                                            s.deleteZone(farmid, zone)
                                            print("Zona Deletada")
                                        else:
                                            print(
                                                "Zona de destino indisponivel")
                                    else:
                                        s.DeleteCattlesinZone(farmid, zone)
                                        s.deleteZone(farmid, zone)
                                        print("Zona Deletada")
                                else:
                                    print("Entrada Invalida")
                            else:
                                s.deleteZone(farmid, zone)
                                print("Zona Deletada")

                    elif opition == 7:
                        earringnumber = int(
                            input("Insira o numero do Brinco que deseja Mostar: "))
                        if s.CattleFromFarm(farmid, earringnumber):
                            s.searchCattle(earringnumber)

                        else:
                            print("Este Gado não exite em sua fazenda ")

                    elif opition == 8:
                        s.listallcattlesfarm(farmid)
                    elif opition == 9:
                        zone = int(
                            input("Insira o numero da zona que deseja Mostar: "))

                        if s.checkZoneExist(farmid, zone):
                            s.listallcattleszone(farmid, zone)
                        else:
                            print("Esta zona nao existe em sua fazenda")

                    elif opition == 10:
                        zone = int(
                            input("Insira o numero da zona que deseja Mostar: "))

                        if s.checkZoneExist(farmid, zone):
                            s.generalViewZone(farmid, zone)
                        else:
                            print("Esta zona nao existe em sua fazenda")

                    elif opition == 11:
                        s.generalViewFam(farmid)

                    elif opition == 0:  # exit program
                        pass
                    else:
                        print("Opcao Invalida")

        elif opition == 4:
            s.listallCattles()
        elif opition == 5:
            s.listallfarms()
        elif opition == 6:
            s.ResetDataBase()

        else:
            print("Opcao Invalida")

    s.conn.closeConnection()

    exit()
