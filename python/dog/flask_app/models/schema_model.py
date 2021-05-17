from flask_app.config.mysqlconnection import connectToMySQL

class Schema:
    def __init__(self,row_id):
        self.id = row_id

    @staticmethod
    def format_data(columns):
        cols = [f'`{col}`' for col in columns]
        vals = [f'%({col})s' for col in columns]
        return cols,vals
#C
    @classmethod
    def create(cls, **data):
        cols,vals = cls.format_data(data.keys())
        query = f"INSERT INTO `{cls.table}` ({', '.join(cols)}) VALUES ({', '.join(vals)})"
        return connectToMySQL(cls.db).query_db(query,data)
#R
    @classmethod
    def retrieve(cls, **data):#if nothing is passed in select all, otherwise filters by whatever keyword arguments are passed in
        cols,vals = cls.format_data(data.keys())
        query = f"SELECT * FROM `{cls.table}` {'WHERE '+' AND'.join(f' {col}={val}' for col,val in zip(cols,vals)) if data else ''}"
        return connectToMySQL(cls.db).query_db(query,data)
#U
    @classmethod
    def update(cls, **data):
        cols,vals = cls.format_data(data.keys())
        query = f"UPDATE `{cls.table}` SET {', '.join(f'{col}={val}' for col,val in zip(cols,vals))} WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)
#D
    @classmethod
    def delete(cls, **data):
        cols,vals = cls.format_data(data.keys())
        query = f"DELETE FROM `{cls.table}` WHERE {' AND '.join(f'{col}={val}' for col,val in zip(cols,vals))}"
        return connectToMySQL(cls.db).query_db(query,data)