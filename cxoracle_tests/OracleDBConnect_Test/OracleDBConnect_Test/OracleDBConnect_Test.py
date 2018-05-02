import cx_Oracle
import sys

oracle_conn = "" # This is a global variable that holds the oracle connection
class DBManagement(object):
    __oracleConnectionString=""

    def __init__(self,user,password,sid,port,host):
        self.oracleHost = host
        self.oraclePort = port
        self.oracleUser = user
        self.oraclePassword = password
        self.oracleSID = sid
        self.__oracleConnectString = user+"/"+password+"@"+host+":"+port+"/"+sid
        self.dsn = cx_Oracle.makedsn(self.oracleHost,self.oraclePort,service_name=sid)
        print(self.__oracleConnectString)
        global oracle_conn
        oracle_conn=cx_Oracle.connect(user,password,self.dsn)




myObj = DBManagement("stock_user","stock_user","orcl122","1521","RMT-FS")

myCursor = oracle_conn.cursor()
myCursor.execute("select * from stock_info")
for result in myCursor:
    print(result)