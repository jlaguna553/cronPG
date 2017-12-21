import psycopg2
import psycopg2.extras
import threading
import time


class conection(object):
    def __init__(self, dbHost, dbName, dbUser, dbPassword):
        self.conn_string = "host='" + dbHost + "' dbname='" + dbName + "' user='" + dbUser + "' password='" + dbPassword + "'"
        try:
            self.conn = psycopg2.connect(self.conn_string)
            self.cursor = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        except Exception as e:
            print ("Se produjo un error al conectarse:\n" + str(e))
            raise
        
    def getData(self, dbFields, dbFrom, dbWhere):
        resultado =None
        try:                                   
            #print "Connected!\n"
            dbQuery = 'Select' + dbFields + 'From' + dbFrom
            if dbWhere != '':
                 dbQuery = dbQuery + 'where' + dbWhere
            self.cursor.execute(dbQuery)
            resultado = self.cursor.fetchall()
        except Exception as e:
            print ("Se produjo un error al consultar la BD:\n" + str(e))
            raise
        finally:
            return resultado

    def doUpdate(self, dbFrom, dbFields, dbWhere):
        updated_rows = 0
        try:
            dbQuery = 'Update' + dbFrom + 'Set' + dbFields 
            if dbWhere != '':
                dbQuery = dbQuery + 'where' + dbWhere  
            self.cursor.execute(dbQuery)
            updated_rows = self.cursor.rowcount
            self.conn.commit()
        except Exception as e:
            print ("Se produjo un error al realizar el UPDATE la BD:\n" + str(e))
            updated_rows = str(e)
            #raise
        finally:
            return updated_rows
        
    def doInsert(self, dbQuery):
        inserted_rows = 0
        try:
            self.cursor.execute(dbQuery)
            inserted_rows = self.cursor.rowcount
        except Exception as e:
            print ("Se produjo un error al realizar el INSERT la BD:\n" + str(e))
            raise
        finally:
            return inserted_rows
    
    def committ(self):
        self.conn.commit()
    
    def closeConection(self):
        self.cursor.close()
        self.conn.close()
