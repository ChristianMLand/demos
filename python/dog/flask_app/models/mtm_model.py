from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

#TODO more error handling

class MtM:
    def __init__(self, left, right, middle):
        '''
        Create an instance of the MtM class.

        Example usages:
        --------
            ``self.favorites = MtM(left = self, right = User, middle = "favorites") -> creates a many-to-many relationship with User called favorites``

        Attributes:
        ----------
            left (Schema): Instance of class representing a given row in a table.
            
            right (Class): Class associated with the table to create the relationship with.
            
            middle (str): Table name of the middle table in the relationship.
        '''
        self.left = left
        self.right = right
        self.middle = middle

    def add(self, *items):
        """
        Creates a new relationship between the given instance and any instances passed in as arguments.

        Example usages:
        -------------
            ``my_user.favorites.add(my_book) -> adds relationship to given book``

            ``my_user.favorites.add(book1,book2,book3) -> adds relationship to all 3 given books``

        Parameters
        ----------
            items (Schema): Items passed as arguments to have a relationship with the given instance.

        Returns
        -------
            Id of the new relationship created in the database if successful or False if query failed.
        """
        query = f"INSERT INTO `{self.middle}` (`{self.left.table}_id`,`{self.right.table}_id`) "
        query += f"VALUES {', '.join(f'({self.left.id},{item.id})' for item in items)}"
        return connectToMySQL(db).query_db(query)

    def remove(self, *items):
        """
        Removes relationship from given instance and any instances passed in as arguments.

        Example usages:
        -------------
            ``my_user.favorites.remove(my_book) -> removes relationship to given book``

            ``my_user.favorites.remove(book1,book2,book3) -> removes relationship to all 3 given books``

        Parameters
        ----------
        items (Schema): Items to have relationship with the given instance removed.

        Returns
        -------
            None if successful or False if query failed
        """
        query = f"DELETE FROM `{self.middle}` WHERE "
        query += f"{'AND '.join(f'`{self.left.table}_id`={self.left.id} AND `{self.right.table}_id`={item.id} ' for item in items)}"
        return connectToMySQL(db).query_db(query)

    def retrieve(self):
        """
        Retrieves all instances with a relationship to the given instance.
        
        Does not take any parameters.

        Example usages:
        -------------
            ``User.favorites.retrieve() -> retrieves all instances with a relationship to the user table via the favorites table``

        Returns
        -------
            List of instances with a relationship to the given instance if successful or False if query failed
        """
        query = f"SELECT `{self.right.table}`.* FROM `{self.right.table}` "
        query += f"JOIN `{self.middle}` ON `{self.right.table}_id` = `{self.right.table}`.id "
        query += f"WHERE `{self.left.table}_id`={self.left.id}"
        return [self.right(**item) for item in connectToMySQL(db).query_db(query)]
    
    def __repr__(self):#more readable representation
        return f"<MtM obj: table={self.middle}>"