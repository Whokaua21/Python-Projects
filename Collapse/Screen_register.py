from colorama import Fore
from colorama import Style
import requests
import json
import sqlite3
sql_Adm = sqlite3.connect('Python-Projects/Collapse/Bank_Collapse.db')
cursor_sql = sql_Adm.cursor()
cursor_sql.execute('''
Create table if not exists CollapseRegister(
Cpf varchar primay key,
Name varchar,
Nacimento varchar,
Address varchar,
Profisson varchar,
Wage varchar
);
''')
def ApiEstados():
    # Api what i'm have use
    # Api_request = requests.get('https://brasilapi.com.br/api/ibge/uf/v1') 
    with open('Python-Projects/Collapse/ApiRegioes.json','r') as ApiFile:
        apiReceive = json.load(ApiFile)
    c = 0
    dictApiEstados = {}
    for i in range(27):
        estado = apiReceive[c]['nome']
        sigla = apiReceive[c]['sigla']
        dictApiEstados[estado] = sigla
        c = c + 1
    return dictApiEstados

class Into_Collapse_Config():
    """
    This object it's all configs from register use SQLite

    You need: name,Birthday,cpf,address,profission,weger
    to you can use the function  
    """
    def __init__(self,name:str,Birthday:str,Cpf:str,address:str,profission:str,Wage:float) -> None:
        self.allname = name
        self.birthday = Birthday
        self.cpf = Cpf
        self.address = address
        self.profission = profission
        self.wega = Wage
    def Put_sql_register_user(self):
        """
        Put informat important from register in SQLite
        of table CollapseRegister 
        """
        cursor_sql.execute(f'''
        insert into CollapseRegister values ('{self.cpf}','{self.allname},
        '{self.birthday}','{self.address}'{self.profission},'{self.wage}')''')
        sql_Adm.commit()



ApiEstado = ApiEstados()
format_ = '-'*30
colorRed = Fore.RED
colorMagenta = Fore.MAGENTA
colotBlue = Fore.BLUE
colorGreen = Fore.GREEN
Reset = Style.RESET_ALL

while True: 
    print(format_)
    print(colorMagenta + '        Collapse Bank' + Reset)
    print(format_)
    print('''[C] Criar Conta\n[E] Entrar''')
    Question_Into_Create = input('-->').upper()
    if Question_Into_Create == 'C':
        print(format_)
        print(colorRed +'   Criação de Conta Collapse'+ Reset)
        print(format_)
        name_Register = input(colorRed + 'Nome completo; \n-->' + Reset)
        while True:
            password = input(str('Senha; \n-->'))
            if len(password) < 8:
                print(colorRed + 'Senha muito curta' + Reset)
                continue
            else:
                break

        while True:
            birthday = input(colorRed + 'Data de Nacimento; \n-->' + Reset)
            if len(birthday) < 8:
                print('Data Errada')
                continue
            break

        while True:
            cpf_Register = input(colorRed +'CPF; \n-->' + Reset)
            if len(cpf_Register) < 11:
                continue
            break

        while True:
            address_register = input(colorRed + 'Estado; \n-->'+ Reset)
            if address_register in ApiEstado.keys():
               break
                
            else:
               print('Esse Estado não existe')
               continue

        Profisson = input('Profisão; \n-->')
        Value_Wage = input(float('Salario; \n-->'))
        Recomend = input(Fore.BLUE + 'Você recomendou alguem ? [S/N]; \n-->' + Reset)
        if Recomend == 'S':
            ...
        if Recomend == 'N':
            print(colorRed +':Conta Criada com sucesso:' + Reset)

    if Question_Into_Create == 'E':
        ...
    else:
        continue
 
