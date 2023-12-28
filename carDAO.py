# Code reference: https://github.com/andrewbeattycourseware/datarepresentation/blob/main/code/Topic10-server1linktoDB.py/bookDAO.py

import mysql.connector
import dbconfig as cfg

# Define a class for handling database operations.
class carDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''


# Constructor to initialise database connection parameters.    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

# Method to establish a database connection and get a cursor.
    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()

 # Method to create a new car entry.         
    def create(self, values):
        cursor = self.getcursor()
        sql="insert into car (name,model, price) values (%s,%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

# Method to retrieve all car entries.
    def getAll(self):
        cursor = self.getcursor()
        sql="select * from car"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

# Method to find a car by its ID.
    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from car where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

 # Method to update car entry.
    def update(self, values):
        cursor = self.getcursor()
        sql="update car set name= %s,model=%s, price=%s  where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

# Method to delete a car entry.        
    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from car where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','name','model', "price"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
carDAO = carDAO()