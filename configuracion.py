import os
import easygui as eg
from AESCipher import *

class AppConfig(eg.EgStore):
    def __init__(self, filename):
        self.host = ""
        self.dbname = ""
        self.user = ""
        self.password = ""
        self.key = ""
        self.iv = ""
        self.filename = filename
        
def LoadConfig():
    car = os.getcwd()
    ArchivoConfig = os.path.join(car,"","config.txt")
    MiConfig = AppConfig(ArchivoConfig)
    MiConfig.restore()
    host = MiConfig.host
    dbname = MiConfig.dbname
    user = MiConfig.user
    password = MiConfig.password
    key = MiConfig.key
    iv = MiConfig.iv

    if MiConfig.host == "" or MiConfig.dbname == "" or MiConfig.user == ""  or MiConfig.password == ""  or MiConfig.key == ""  or MiConfig.iv == "" :
        campos = ['Host', 'Nombre DB', 'Usuario','Password','Key para Cript','IV']
        datos = [host, dbname, user, password, key, iv]
        datos = eg.multenterbox(msg='Modifique los datos',
                                title='EgStore: Guardar datos',
                                fields=campos, values=datos)

        MiConfig.host = encrypt(datos[0],datos[4],datos[5])
        MiConfig.dbname = encrypt(datos[1],datos[4],datos[5])
        MiConfig.user = encrypt(datos[2],datos[4],datos[5])
        MiConfig.password = encrypt(datos[3],datos[4],datos[5])
        MiConfig.key = datos[4]
        MiConfig.iv = datos[5]
        MiConfig.store()

    MiConfig.restore()
    MiConfig.password = decrypt(MiConfig.password,MiConfig.key,MiConfig.iv)
    MiConfig.host = decrypt(MiConfig.host,MiConfig.key,MiConfig.iv)
    MiConfig.dbname = decrypt(MiConfig.dbname,MiConfig.key,MiConfig.iv)
    MiConfig.user = decrypt(MiConfig.user,MiConfig.key,MiConfig.iv)

    return MiConfig