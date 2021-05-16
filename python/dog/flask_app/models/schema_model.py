from flask_app.config.mysqlconnection import connectToMySQL

class Schema:
    def __init__(self,row_id):
        self.id = row_id

    @staticmethod
    def format_data(**data):
        cols = [f'`{col}`' for col in data.keys()]
        vals = [f'%({col})s' for col in data.keys()]
        return cols,vals
    
    @classmethod
    def create(cls, **data):
        cols,vals = cls.format_data(**data)
        query = f'INSERT INTO `{cls.table}` ({", ".join(cols)}) VALUES ({", ".join(vals)})'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update(cls, **data):
        cols,vals = cls.format_data(**data)
        query = f"UPDATE `{cls.table}` SET {', '.join(f'{col}={val}' for col,val in zip(cols,vals))} WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM `{cls.table}`"
        res =  connectToMySQL(cls.db).query_db(query)
        print(query,res)
        return res

    @classmethod
    def get_one(cls,**data):
        cols,vals = cls.format_data(**data)
        query = f"SELECT * FROM `{cls.table}` WHERE {' AND '.join(f'{col}={val}' for col,val in zip(cols,vals))}"
        return connectToMySQL(cls.db).query_db(query,data)[0]
    
    @classmethod
    def delete(cls,**data):
        cols,vals = cls.format_data(**data)
        query = f"DELETE FROM `{cls.table}` WHERE {' AND '.join(f'{col}={val}' for col,val in zip(cols,vals))}"
        return connectToMySQL(cls.db).query_db(query,data)