from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

#TODO more error handling

class MtM:
    def __init__(self, **data):
        self.left = data.get("left_table")
        self.right = data.get("right_table")
        self.middle = data.get("middle_table")

    def add(self, *items):#TODO properly sanitize
        query = f"INSERT INTO `{self.middle}` (`{self.left.table}_id`,`{self.right.table}_id`) "
        query += f"VALUES {', '.join(f'({self.left.id},{item.id})' for item in items)}"
        return connectToMySQL(db).query_db(query)

    def remove(self, *items):#TODO properly sanitize
        query = f"DELETE FROM `{self.middle}` WHERE "
        query += f"{'AND '.join(f'`{self.left.table}_id`={self.left.id} AND `{self.right.table}_id`={item.id} ' for item in items)}"
        return connectToMySQL(db).query_db(query)

    def retrieve(self):
        query = f"SELECT `{self.right.table}`.* FROM `{self.right.table}` "
        query += f"JOIN `{self.middle}` ON `{self.right.table}_id` = `{self.right.table}`.id "
        query += f"WHERE `{self.left.table}_id`={self.left.id}"
        return [self.right(**item) for item in connectToMySQL(db).query_db(query)]
    
    def __repr__(self):#more readable representation
        return f"<MtM obj: table={self.middle}>"