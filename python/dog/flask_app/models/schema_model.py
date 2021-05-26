from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

#TODO more error handling

class Schema:
    validators = {}

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
        new_id = connectToMySQL(db).query_db(query,data)
        return cls(id=new_id,**data)
#-------------------Retrieve-------------------#
    @classmethod
    def retrieve(cls, **data):#if no data passed in, select all, otherwise filter by whatever keyword arguments are passed in
        cols,vals = cls.format_data(data.keys())
        query = f"SELECT * FROM `{cls.table}` {'WHERE'+' AND'.join(f' {col}={val}' for col,val in zip(cols,vals)) if data else ''}"
        return [cls(**item) for item in  connectToMySQL(db).query_db(query,data)]
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
#------------------Validate--------------------#
    @classmethod
    def validate(cls,**data):
        is_valid = True
        for field,valids in cls.validators.items():
            for valid,msg in valids:
                if not valid(data.get(field)):
                    flash(msg)
                    is_valid = False
                    break
        return is_valid

    @classmethod
    def validator(cls,msg):
        def register(func):
            if func.__name__ not in cls.validators:
                cls.validators[func.__name__] = [(func,msg)]
            else:
                cls.validators[func.__name__].append((func,msg))
        return register
#----------------------------------------------#
    def __repr__(self):#more readable representation
        return f"<{self.table} obj: id={self.id}>"

    def __lt__(self,other):#allows sorting
        return self.id < other.id