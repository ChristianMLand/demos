from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

class Schema:
    def __init__(self,row_id):
        self.id = row_id

    @staticmethod#can be called either by the class directly or an instance of the class
    def format_data(columns):
        cols = [f'`{col}`' for col in columns]
        vals = [f'%({col})s' for col in columns]
        return cols,vals
#-------------------Create---------------------#
    @classmethod
    def create(cls, **data):
        cols,vals = cls.format_data(data.keys())
        query = f"INSERT INTO `{cls.table}` ({', '.join(cols)}) VALUES ({', '.join(vals)})"
        return connectToMySQL(db).query_db(query,data)
#-------------------Retrieve-------------------#
    @classmethod
    def retrieve(cls, **data):#if nothing is passed in select all, otherwise filters by whatever keyword arguments are passed in
        cols,vals = cls.format_data(data.keys())
        query = f"SELECT * FROM `{cls.table}` {'WHERE '+' AND'.join(f' {col}={val}' for col,val in zip(cols,vals)) if data else ''}"
        return connectToMySQL(db).query_db(query,data)
#-------------------Update---------------------#
    @classmethod
    def update(cls, **data):
        cols,vals = cls.format_data(data.keys())
        query = f"UPDATE `{cls.table}` SET {', '.join(f'{col}={val}' for col,val in zip(cols,vals))} WHERE id=%(id)s"
        return connectToMySQL(db).query_db(query,data)
#-------------------Delete---------------------#
    @classmethod
    def delete(cls, **data):
        cols,vals = cls.format_data(data.keys())
        query = f"DELETE FROM `{cls.table}` WHERE {' AND '.join(f'{col}={val}' for col,val in zip(cols,vals))}"
        return connectToMySQL(db).query_db(query,data)
#----------------------------------------------#