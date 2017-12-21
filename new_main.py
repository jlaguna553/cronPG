from configuracion import *
from AESCipher import *
from model import *
import os
from multiprocessing import Process


def worker(base,path,config):
    try:
        print ("{0} Start Process and stablish conection to {1}".format(os.getpid(),base))
        status(base,2,path,config)
        cx = conection(config.host,base['NombreBase'].replace('PG-',""),
                       base['UserAdmin'],decrypt(base['PasswordAdmin_SinCripto'],config.key,config.iv))
        cx.getData('*',base['Funcion'],'')
        status(base, 1,path,config)
        print ("{} Finish thread".format(os.getpid()))
    except Exception as e:
        os.path.join(path, "", "Errorlog.txt")
        archi = open('Errorlog.txt', 'a')
        archi.write('Error con el Proceso {}'.format(os.getpid()) + ' tiempo de error: ' + str(
        time.strftime("%c")) + ' Nombre de la base de datos: ' + str(base['NombreBase']) +
                    ' Nombre de la funcion: ' + str(base['Funcion']) + ' Tipo de error :' + str(e) + '\n')
        archi.close()


def status (base, status,path,config):
    cx2 = conection(config.host,config.dbname,config.user,config.password)
    update = cx2.doUpdate('"HQ"."Cron"',
                          '"UltimaActualizacion" = now(),"FuncionProcesadaPy" = {}'.format(status),
                          '"idCron" = {}'.format(base['idCron']))
    try:
        int(update)
        print 'successUpdate'
        cx2.committ()
        cx2.closeConection()
    except:
        os.path.join(path, "", "Errorlog.txt")
        archi = open('Errorlog.txt', 'a')
        archi.write(
            'Error!...  tiempo de error: ' + str(time.strftime("%c")) + ' Nombre de la base de datos: ' + str(
                base['NombreBase']) + ' Nombre de la funcion: ' + str(
                base['Funcion']) + ' Tipo de error :' + str(update) + '\n')
        archi.close()



if __name__=="__main__":
    procs = []
    config = LoadConfig()
    cnn = conection(config.host,config.dbname,config.user,config.password)
    cronPendientes = cnn.getData('*','"HQ"."vw_hq_CronPendiente"','')
    cnn.closeConection()
    #ruta absoluta ;)
    path = os.path.abspath(os.getcwd())

    for cronPendiente in cronPendientes:
        proc = Process(target=worker, args=(cronPendiente,path,config,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()