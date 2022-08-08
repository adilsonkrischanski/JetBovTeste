# JetBovTeste

Informações Iniciais 

    Python
        O codigo foi desenvolvido em python, logo, é necessario ter o python instalado para o bom funcionamento
        Documentação do python <https://www.python.org/>

    Banco de Dados
        O sistema esta interligado com um banco de dados Postgres
        informações disponiveis sobre o banco em <https://www.postgresql.org/>

        Para o bom funcionamento é nessario uma base de bados com as seguintes informações
            * Usuario: postgres
            * Password: 15032001
            * Nome Database: JetBov
            * host: localhost
            * Exite um arquivo chamado DataBaseJetBov esse arquivo contem um script de backup, esse script deve ser executado no query da Database criada anteriormente para a criação das tabelas
            * A base de dados ja possui fazendas zonas e animais incluidas para testes iniciais, você tem a opção de detetar todos os valores ali presentes no menu de sistema.
            * Para executar o o query de criacao da database recomendase o uso do pgadmin, informacoes disponiveis em <https://www.pgadmin.org/>

        É nessesario um driver para a comunicação do Codigo com o Banco de Dados
        O Driver usado foi o psycopg2 informações sobre o driver e forma de instalação disponiveis em <https://pypi.org/project/psycopg2/>

    
Suporte:
    Email: adilson.krischanski@outlook.com
    Whatsapp: (47) 9 9225-7527


Menu de sistema:

    O menu de sistema possui 7 opções 

    Opção 0 - Fecha o programa

    Opção 1 - Mostra as instruções 

    Opção 2 - Cadastra uma nova Fazenda 
            * Para isso é Necessario Informar nome e Localização da Fazenda
            * Não é permitido nome de fazendas Repitidos (O bando permite, o Sistema não)

    Opção 3 - Entrar em uma fazenda
            * Semelhante a um Loguin, é necessario informar o nome da fazenda
            * O sistema NÃO está Case sentitive para loguin, é permitido caractere numerico também
            * após digitar o nome da fazenda ele é verificada a sua exixtencia e então é liberado o acesso ao menu principal (interno da fazenda)

    Opção 4 - Exibe Todos os Brincos com os pesos cadastrados no sistema (Requisito do teste)

    Opção 5 - Exibe uma lista de todas as fazendas cadastradas no sistema 

    Opção 6 - Reseta a base de Dados do sistema
    

Menu Principal (Fazenda):

    Opção 0 - Fecha o programa

    Opção 1 - Cadastra uma Nova Zona na Fazenda
            * É necessario informar
                -Quantidade de animais suportados pela zona
                -Ganho Medio Diario(GMD) da zona 
                -Tempo de Recuperação da zona após a saida dos animais

    Opção 2 -  Inserir um novo Animal
            * É necessario informar
                -Numero do Brinco
                    *Após a insersao do numero é feita uma verificacao para saber se o animal ja existe (Numero do brinco é identificador)
                - Raça do Gado
                - Peso ideal dessa raça para o Abate
                - Peso atual o Gado
                - Data de Nascimento do Gado 
                - Zona de Alocação do gado

    Opção 3 - Mover um animal de Zona 
            * É necessario informar
                -Numero do Brinco
                    *Após a insersao do numero é feita uma verificacao para saber se o animal ja existe e é propiedade da fazenda (Numero do brinco é identificador)
                -Zona de destino 
                    * checando a possibilidade de translado e se possivel o gado é transladado e tem seu peso atualizado, se não for possivel o gado permanece na sua zona atual e tem seu peso mantido.
                - se o gado movido for o ultimo presente na zona a zona entra em estado de recuperação

    Opção 4 - Mover animais de uma Zona para Outra
            * É necessario informar
                -Numero da Zona que deseja Mover 
                -Numero de Zona de destino
                -Checando a possibilidade de Mudança, se possivel todos os gados são movidos para a nova zona e tem seus pesos atualizados e a zona anterior entra em estado de Recuperação, se não for possivel os gados são mantidos sem alteração na zona em que estavam

    Opção 5 - Deleta um animal 
                * É necessario informar
                -Numero do Brinco
                    *Após a insersao do numero é feita uma verificacao para saber se existe e é propiedade da fazenda (Numero do brinco é identificador), se  gado for da fazenda ele é deletado e deixa de existir no Banco de Dados.

    Opção 6 - Deleta uma zona
            * É necessario informar
                -Numero da Zona que deseja Deletar
                    * É verificado de a zona existe, se sim e verificado a existencia de animais na zona, se ouver o usuario pode mover os animais, ou deletalos junto com a zona, em seguida a zona é deletada, se a zona não existir na fazendo o usuario é notificado e nada acontece.

    Opção 7 - Buscar Informações de um Gado
            * É necessario informar
                -Numero do Brinco
                    *Após a insersao do numero é feita uma verificacao se existe e é propiedade da fazenda, se sim é mostrado um dossie com todas as informções do adm.

    Opção 8 - imprime na tela uma lista de brincos e Pesos dos Animais da Fazenda
    
    Opção 9 - imprime na tela uma lista de brincos e Pesos dos Animais de uma zona especifica da Fazenda
                * É necessario informar
                    -Numero da zona, se a zona existir na fazenda imprime uma lista com os brincos e os pesos daquela zona em especifico 

    Opção 10 - Buscar Informacoes de uma Zona
               * É necessario informar
                    -Numero da zona, se a zona existir na fazenda, é mostrado um dossie da zona 

    Opção 11 - Mostra um dossie da Fazenda



Analizes para o Desenvovimento da aplicação:

    Sistema: 
        O sistema pode conter varias Fazendas


    Fazenda:
        Cada fazenda pode conter varias zonas
        Cada fazenda pode conter varios animais que precisam estar alocados em sua zonas
        Cada fazenda deve exibir suas informações Gerais 



    Zonas: 
        Cada Zona pode Conter ate N animais
        Cada Zona possui um gmd 
        Cada Zona Possui um campo para ultima data de entrada do primeiro animal a entrar na zona 
        Cada Zona Possui um campo para ultima data de saida do ultimo animal a sair da zona 
        
        Quando ocorrer uma mudança de zona o peso dos animais deve ser atualizado 


    Animais:
        Cada Animal deve Conter um numero de Brinco
        Cada Animal deve Conter uma Raça
        Cada Animal deve Conter um peso ideal de abate
        Cada Animal deve Conter um peso atual
        Cada Animal deve Conter uma data de nascimento
        Cada Animal deve Conter uma dada de entrada na zona
        Cada Animal deve Conter uma data de entrada na fazenda
        Cada Animal deve Conter a zona atual de alocação 
        Cada Animal deve Conter um identificador da fazenda propietaria
      



Proximas melhorias:
    Criar uma tabela vinculando Raças para não precisar informar pesos ideiais para abate na criação de cada Gado
    Otimizar consultas ao banco, algumas consultas acabaram sendo bem repetitivas e podem ser otimizas
    Remoldagem, em alguns momentos a validação foi feita antes da função principal e em outros ela feita dentro da função principal, deixar padronizado.


