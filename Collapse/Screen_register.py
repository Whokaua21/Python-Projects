from ast import Try
from colorama import Fore
from colorama import Style
import requests
from time import time
import json
import sqlite3
import os
import pandas as pd
import datetime
sql_Adm = sqlite3.connect('Python-Projects/Collapse/Bank_Collapse.db')
cursor_sql = sql_Adm.cursor()
cursor_sql.execute('''
Create table if not exists CollapseRegister(
Cpf integer primary key,
Name varchar,
PassWortd varchar,
Nacimento varchar,
YearsUser int, 
StadeUser varchar,
Profisson varchar,
Wage float
)
''')

# Extract from account user

cursor_sql.execute("""
Create table if not exists Extrato_Usuario(
    CPF integer,
    Name varchar,
    MoneyLose float,
    Date varchar               
    )
""")
# cursor_sql.execute('Drop table Pix_CLLP')
# cursor_sql.execute('Drop table CollapseRegister')
# cursor_sql.execute('Drop table Extrato_Usuario')
def ApiEstados() -> dict:
    # Api what i'm have use
    # Api_request = requests.get('https://brasilapi.com.br/api/ibge/uf/v1') 
    with open('Python-Projects/Collapse/ApiRegioes.json','r') as ApiFile:
        apiReceive = json.load(ApiFile)
    index_Contriy = 0
    dictApiEstados = {}
    for i in range(27):
        estado = apiReceive[index_Contriy]['nome']
        sigla = apiReceive[index_Contriy]['sigla']
        dictApiEstados[estado] = sigla
        index_Contriy = index_Contriy + 1
    return dictApiEstados

def Verify_Register_Into(cpf,password) -> bool:
    """
    Verify Register from user 
    User Need(CPF and Password) from user

    if Password or CPF wrong return False else True
    """
    AllRegisters = cursor_sql.execute('Select Cpf,PassWortd from CollapseRegister').fetchall()
    for Cpf_and_Password in AllRegisters:
        if Cpf_and_Password[0] == cpf and Cpf_and_Password[1] == password:
            return True
    return False

def Verify_Key_Pix(key):
    verify_key = cursor_sql.execute('Select Key_user from Pix_CLLP').fetchall()
    for V in verify_key:
        if key == V[0]:
            print('Ok')
            return False



ApiEstado = ApiEstados()
format_ = '-'*30
colorRed = Fore.RED
colorMagenta = Fore.MAGENTA
colortBlue = Fore.BLUE
colorGreen = Fore.GREEN
Reset = Style.RESET_ALL

        
class Into_Collapse_Config():
    """
    This object is all configs from register using SQLite

    You need: name,Birthday,cpf,address,profission,weger
    to you can use the function  
    """
    def __init__(self,name:str,PassWord:str,Birthday:str,Cpf:str,Stade:str,profission:str,Wage:float,YersUser:int) -> None:
        self.allname = name
        self.birthday = Birthday
        self.cpf = Cpf
        self.stade = Stade
        self.profission = profission
        self.wage = Wage
        self.years = YersUser
        self.password = PassWord
        format_ = '-'*20
    def Put_sql_register_user(self) -> None:
        """
        Put informat important from register in SQLite
        of table CollapseRegister 
        """
        cursor_sql.execute(f'''
        insert into CollapseRegister values ('{self.cpf}','{self.allname}',
        '{self.password}','{self.birthday}',{self.years},'{self.stade}','{self.profission}',{self.wage})''')
        sql_Adm.commit()


class Screen_Config_Functions(Into_Collapse_Config):
    def __init__(self,name:str,PassWord:str,Birthday:str,Cpf:str,Stade:str,profission:str,Wage:float,YersUser:int) -> None:
        self.allname = name
        self.password = PassWord
        self.birthday = Birthday
        self.cpf = Cpf
        self.stade = Stade
        self.profission = profission
        self.wage = Wage
        self.years = YersUser
    def Screen_Collapse_Options(self):
        print(colorMagenta + f'{format_}\nCollapse Bank\n{format_}' + Reset)
        print(f'Nome:{self.allname}\nWage:{self.wage}\n')
        print(f"[P]Pix\n[E]Extrato\n[V]Voltar\n{format_}")
        Question_to_which_function_use = input().upper()
        match Question_to_which_function_use:
            case 'P':
                os.system('cls')
                self.Pix_Config_Load()
            case 'E':
                os.system('cls')
                self.Extrato_Cont()
            case 'V':
                os.system('cls')
                return


    def Extrato_Cont(self):
        format_Extrato = '|----------------------------------------|'
        print(colorGreen + f'{format_Extrato}\n     Extrato da Conta\n{format_Extrato} ')
        print(f'Nome:{self.allname}\nCPF:{self.cpf}' + Reset)
        print('Okkk')
        TakeExtrato = cursor_sql.execute(f'Select * from Extrato_Usuario where CPF = "{self.cpf}"  ').fetchall()
        Dict_Extrato = {
            'CPF': [],
            'Name': [],
            'MoneyLose': [],
            'Date': [],
        }

        for i in TakeExtrato:
            Dict_Extrato['CPF'].append(i[0])
            Dict_Extrato['Name'].append(i[1])
            Dict_Extrato['MoneyLose'].append(i[2])
            Dict_Extrato['Date'].append(i[3])
        if Dict_Extrato['CPF'] == []:
            print('Nao possui extrato')
            self.Screen_Collapse_Options()
            
        Table_xml = pd.DataFrame(Dict_Extrato)
        print(Table_xml)
        print('Deseja Salvar a Tabela?'.upper())
        if input('[S/N]->').upper() == 'S':
            Table_xml.to_csv('D:\\program_vs\Python-Projects\Collapse\AquivoCSV.csv',index=False)
        os.system('cls')
        self.Screen_Collapse_Options()



    def Pix_Config_Load(self):
        # Local Pix configuration

        cursor_sql.execute('PRAGMA foreign_keys = ON;')
        cursor_sql.execute('''
         Create table if not exists Pix_CLLP(
            Key_user varchar primary key,
            CPF int,
            Foreign Key(CPF) References CollapseRegister(Cpf)                    
            );''')
        Response_Tranfer_Key = ['T','C']
        while True:
            # Creating key pix from user
            print(colorMagenta + f'{format_}\n      Collapse PIX\n{format_}' + Reset)
            print('[T] Transferencia\n[C] Criar Chave')
            Ask_Transfer_or_Key = input('-->').upper()

            if not isinstance(Ask_Transfer_or_Key,str) or Ask_Transfer_or_Key not in Response_Tranfer_Key:
                continue 
            if Ask_Transfer_or_Key == 'T':
                # Tranfer monney to other person
                while True:
                    Transfer_Complete = False
                    # Select All Keys Pix in Table Pix_CLLP
                    All_keys_pix = cursor_sql.execute('Select Key_user from Pix_CLLP ').fetchall()
                    print(All_keys_pix)
                    # Tranfer money by pix
                    print(colorMagenta + f'{format_}\n       Transferencia\n{format_}' + Reset)
                    Input_key_pix = str(input('Chave Pix:\n-->')) 
                    print(All_keys_pix)
                    Cont_accont = 0
                    # Verify if the key pix is correct
                    for verify_key_pix in All_keys_pix:
                        print(verify_key_pix)
                        for verifyin in  verify_key_pix:
                            if verifyin == Input_key_pix:
                                print(verifyin)

                                # Select the accont from user what gosed received the monney 
                                select_accont_pix_user = cursor_sql.execute(f'''Select CPF from Pix_CLLP where Key_user = '{Input_key_pix}' ''').fetchall()
                                print(select_accont_pix_user[0][0])


                                # Update Saldo of user what received the money
                                data_user_pix = cursor_sql.execute(f'select Name,Wage,StadeUser from CollapseRegister where Cpf = {select_accont_pix_user[0][0]}').fetchall() 

                                print(f'Nome: {data_user_pix[0][0]}\nSaldo: R${data_user_pix[0][1]}\nEstado: {data_user_pix[0][2]}')

                                value_pix = float(input('Valor do R$:'))
                                Saldo = round(float(data_user_pix[0][1]),2)
                                Saldo += round(value_pix,2)
                                print(Saldo)
                                cursor_sql.execute(f'UPDATE CollapseRegister SET Wage = {Saldo} WHERE Cpf = {select_accont_pix_user[0][0]}')
                                sql_Adm.commit()
                                #Update Wege from trasnfer 

                                UserDropSaldo = cursor_sql.execute(f'SELECT Wage from CollapseRegister where Cpf = {self.cpf} ').fetchall()

                                cursor_sql.execute(f'UPDATE CollapseRegister SET Wage = {UserDropSaldo[0][0] - value_pix} WHERE Cpf = {self.cpf}')

                                cursor_sql.execute(f'Insert into Extrato_Usuario (CPF,Name,MoneyLose,Date) values ("{self.cpf}", "{self.allname}", "{value_pix}","{datetime.datetime.now()}")')
                            
                                sql_Adm.commit()

                                print(colortBlue + f'{format_}\n  Transferência Concluída\n{format_}' + Reset)
                                os.system("cls")
                                os.system('cls')
                                self.Screen_Collapse_Options()
                            else:
                                print('.')
            else:
                # Creating new key pix from user
                while True:
                    print(colorMagenta + f'{format_}\n       Criação de Chave\n{format_}' + Reset)
                    print('Obs: É Recomendado usar o seu CPF ou Telefone:')
                    Create_key_pix = input('Digite sua chave:')
                    c = 0
                    if len(Create_key_pix) > 15:
                        print(':Chave muito longa:')
                        continue
                    verify_key = Verify_Key_Pix(Create_key_pix)
                    if verify_key == False:
                        print(':Chave já existente:')
                        continue
                    else:
                        cursor_sql.execute(f'INSERT INTO Pix_CLLP (Key_user, CPF) VALUES("{Create_key_pix}","{self.cpf}")')
                        sql_Adm.commit()
                        os.system('cls')
                        print(colortBlue + f'{format_}\n      Chave Criada\n{format_}' + Reset)
                        self.Screen_Collapse_Options()
                        
# l = Screen_Config_Functions('Kaua','123456','10102007','86545695112','Bahia','Desenvolvedor','1000','2007')
# l.Screen_Collapse_Options()

Screen_Register = True
try:
    print('ok')
    while Screen_Register: 
        print(format_)
        print(colorMagenta + '        Collapse Bank' + Reset)
        print(format_)
        print('''[C] Criar Conta\n[E] Entrar''')
        Question_Into_Create = input('-->').upper()
        if Question_Into_Create == 'C':
            print(format_)
            print(colorRed +'   Criação de Conta Collapse'+ Reset)
            print(format_)
            name_Register = input(colortBlue + 'Nome completo; \n-->' + Reset)
            while True:
                password = input(str(colortBlue + 'Senha max(6); \n-->' + Reset))
                if len(password) > 6:
                    os.system('cls')
                    print(colortBlue + 'Senha muito longa' + Reset)
                    continue
                else:
                    break

            while True:
                birthday = input(colortBlue + 'Data de Nacimento; \n-->' + Reset)
                if len(birthday) < 8:
                    os.system('cls')
                    print('Data Errada')
                    continue
                year_day =  int(birthday[4:].strip())
                print(type(year_day))
                break

            while True:
                cpf_Register = input(colortBlue +'CPF; \n-->' + Reset)
                if len(cpf_Register) < 11:
                    os.system('cls')
                    print('CPF invalido')
                    continue
                break

            while True:
                address_register = input(colortBlue + 'Estado; \n-->'+ Reset)
                if address_register in ApiEstado.keys():
                    break
                else:
                    os.system('cls')
                print('Esse Estado não existe')
                continue

            Profisson = input('Profisão; \n-->')
            while True:
                Value_Wage = round(float(input('Slario;\n-->')),2)
                if not isinstance(Value_Wage,float):
                    print('Erro:Não e um numero ou falta de .')
                    continue
                break

            Recomend = input(Fore.BLUE + 'Você foi recomendado por alguem? [S/N]; \n-->' + Reset).upper()
            if Recomend == 'S':
                # Recomen give 10R$ the more
                # Not Recomend give nothing
                Value_Wage += 10
            print(colortBlue +':Conta Criada com sucesso:' + Reset)
            receive_informat = Into_Collapse_Config(name_Register.upper(),password,birthday,cpf_Register,address_register,Profisson,Value_Wage,year_day)
            receive_informat.Put_sql_register_user()


        elif Question_Into_Create == 'E':
            AllRegisters = cursor_sql.execute('Select Cpf,PassWortd from CollapseRegister').fetchall()
            confirm_cpf = int(input('CPF;\n-->'))
            confirm_password = input('Senha;\n-->') 
            Verify_Accont = Verify_Register_Into(confirm_cpf,confirm_password)
            if Verify_Accont == False:
                os.system('cls')
                print(colorRed + 'Login Invalido' + Reset)
                print(colorRed + ':CPF ou Senha Invalidos:' + Reset)
                continue

            else:
                print(colortBlue + 'LOGIN FEITO' + Reset)
                # Insert Data to Into_Collapse_Config

                list_register_user =  cursor_sql.execute(f'Select * from CollapseRegister where cpf = {confirm_cpf}').fetchall()
                Screnn_collapse = Screen_Config_Functions(list_register_user[0][1],list_register_user[0][2],list_register_user[0][3],list_register_user[0][0],
                list_register_user[0][5],list_register_user[0][6],list_register_user[0][7],list_register_user[0][4])
                os.system('cls')
                Screnn_collapse.Screen_Collapse_Options()
        else:
            continue
except:
    sql_Adm.rollback()
    sql_Adm.close()
    cursor_sql.close()
    print('Erro ao conectar ao banco de dados')
    