from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

#TODO more error handling

class MtM:
    '''
    A class to that holds methods for querying many-to-many relationships

    ...

    Attributes
    ----------
    left : Schema
        instance of class representing a given row in a table
    right : Class
        Class of table to create the relationship with
    middle : str
        table name of the middle table in the relationship
    
    Methods:
    --------
    add(*items):
        creates a new relationship for the given row and any rows passed in as items
    
    remove(*items):
        removes a relationship for the given row and and rows passed in as items
    
    retrieve():
        returns a list of rows with a relationship to the given row
    '''
    def __init__(self, **data):
        """
        Constructs all the necessary attributes for the MtM object.

        Parameters
        ----------
            left : Schema
                instance of class representing a given row in a table
            right : Class
                Class of table to create the relationship with
            middle : str
                table name of the middle table in the relationship
        """
        self.left = data.get("left_table")
        self.right = data.get("right_table")
        self.middle = data.get("middle_table")

    def add(self, *items):#TODO properly sanitize
        """
        Creates a new relationship for the given row and any rows passed in as arguments

        Parameters
        ----------
        items : Obj | List[Obj]
            list of items to have a relationship with the given row

        Returns
        -------
            None
        """
        query = f"INSERT INTO `{self.middle}` (`{self.left.table}_id`,`{self.right.table}_id`) "
        query += f"VALUES {', '.join(f'({self.left.id},{item.id})' for item in items)}"
        return connectToMySQL(db).query_db(query)

    def remove(self, *items):#TODO properly sanitize
        """
        Removes relationship from given row and any rows passed in as arguments

        Parameters
        ----------
        items : Obj | List[Obj]
            list of items to have relationship with the given row removed

        Returns
        -------
            None
        """
        query = f"DELETE FROM `{self.middle}` WHERE "
        query += f"{'AND '.join(f'`{self.left.table}_id`={self.left.id} AND `{self.right.table}_id`={item.id} ' for item in items)}"
        return connectToMySQL(db).query_db(query)

    def retrieve(self):
        """
        Retrieves all rows with a relationship to the given row

        Returns
        -------
            List of rows with a relationship to the given row
        """
        query = f"SELECT `{self.right.table}`.* FROM `{self.right.table}` "
        query += f"JOIN `{self.middle}` ON `{self.right.table}_id` = `{self.right.table}`.id "
        query += f"WHERE `{self.left.table}_id`={self.left.id}"
        return [self.right(**item) for item in connectToMySQL(db).query_db(query)]
    
    def __repr__(self):#more readable representation
        return f"<MtM obj: table={self.middle}>"