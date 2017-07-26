from configuracion import *
from AESCipher import *
from model import *
import os
import threading

class worker(threading.Thread):
    def __init__ (self, base, config,cnn):
        threading.Thread.__init__(self)
        self.b = base
        self.c = config
        self.connect = cnn
    def run(self):
        try:
            print ("{} Start thread".format(self.getName()))
            status(self.b,self.connect,2)
            cx = conection(self.c.host,self.b['NombreBase'].replace('PG-',""),self.b['UserAdmin'],decrypt(self.b['PasswordAdmin_SinCripto'],self.c.key,self.c.iv))
            qry = cx.getData('*',self.b['Funcion'],'')
            #print qry
            status(self.b,self.connect,1)
            print ("{} Finish thread".format(self.getName()))
        except Exception as e:
            car = os.getcwd()
            os.path.join(car,"","Errorlog.txt")
            archi=open('Errorlog.txt','a')
            archi.write('Error con el hilo {}'.format(self.getName()) + ' tiempo de error: ' + str(time.strftime("%c")) + ' Nombre de la base de datos: ' + str(self.b['NombreBase']) + ' Nombre de la funcion: '+ str(self.b['Funcion'])+    ' Tipo de error :'+ str(e) +'\n')
            archi.close()
            raise

        
def status(base,cnn,status):
    update = cnn.doUpdate('"HQ"."Cron"','"UltimaActualizacion" = now(),"FuncionProcesadaPy" = {}'.format(status),'"idCron" = {}'.format(base['idCron']))
    if update >= 0:
        print 'successUpdate'
    else:
        car = os.getcwd()
        os.path.join(car,"","Errorlog.txt")
        archi=open('Errorlog.txt','a')
        archi.write('Error!...  tiempo de error: ' + str(time.strftime("%c")) + ' Nombre de la base de datos: ' + str(base['NombreBase']) + ' Nombre de la funcion: '+ str(base['Funcion'])+    ' Tipo de error :'+ str(update) +'\n')
        archi.close()
        
        
        
class pinger(threading.Thread):
    def __init__ (self,config):
        threading.Thread.__init__(self)
        self.p = config.host
    def run(self):
        while True:
            print ("Doing pint to ... {}".format(self.p))
            try:                                   
                response = os.system("ping -c 1 " + self.p)
                if response == 0:
                    print self.p, 'is up!'
                time.sleep(5)
            except Exception as e:
                print ("Error during ping:\n" + str(e))
                raise
        

        
        
if __name__=="__main__":
    response = -1
    times = 0
    threads = []
    #print con
    con = LoadConfig()
    while response != 0 or times == 10:
        print ("Doing pint to ... {}".format(con.host))
        response = os.system("ping -c 1 " + con.host)
        time.sleep(2)
        if response == 0:
            print con.host, 'is up!'
        else:
            times = times + 1
    if response == 0:
        cnn = conection(con.host,con.dbname,con.user,con.password)
        qry = cnn.getData('*','"HQ"."vw_hq_CronPendiente"','')
        #print qry
        daemonPing = pinger(con)
        daemonPing.daemon = True
        #daemonPing.start()

        for num in qry:
            thread = worker(num,con,cnn)
            thread.start()
            threads.append(thread)
            #time.sleep(.5)
        for thread in threads:
            thread.join()
    else:
        car = os.getcwd()
        os.path.join(car,"","Errorlog.txt")
        archi=open('Errorlog.txt','a')
        archi.write('Error No se ha podido establecer conexion,  tiempo de error: ' + str(time.strftime("%c")) + '\n')
        archi.close()
    
    
    

    


#msj = encrypt('hola',con.key,con.iv)
#msj2 = decrypt(msj,con.key,con.iv)
