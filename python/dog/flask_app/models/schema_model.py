from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

#TODO more error handling

class Schema:
    '''
    A class to that holds methods for basic sql queries.

    Classes that represent tables in your database should
    extend this class.

    Should only ever be extended and not instantiated on its own.
    '''
    @staticmethod
    def format_data(columns):
        """
        Formats given data in a way that is safe to pass into a sql query without risk of sql injection.

        Parameters
        ----------
            columns (list[str]): List of column/variable names.

        Returns
        -------
            Tuple containing a list of escaped column names and a list of formatted variable names.
        """
        cols = [f'`{col}`' for col in columns]
        vals = [f'%({col})s' for col in columns]
        return cols,vals
#-------------------Create---------------------#
    @classmethod
    def create(cls, **data):
        '''
        Creates a new row in the database built from the given data.

        Example usages:
        --------------
            ``User.create(name="John",age=35) -> creates a new user with name "John" and age of 35``

            ``User.create(**request.form) -> creates a new user based on the data recieved from the form``

        Parameters
        ----------
            data (str): Key word arguments for each of the columns and the values to create.

        Returns
        -------
            New instance of the given class.
        '''
        cols,vals = cls.format_data(data.keys())
        query = f"INSERT INTO `{cls.table}` ({', '.join(cols)}) VALUES ({', '.join(vals)})"
        new_id = connectToMySQL(db).query_db(query,data)
        return cls(id=new_id,**data)
#-------------------Retrieve-------------------#
    @classmethod
    def retrieve(cls, **data):
        '''
        Retrieves everything from the database that matches the given data in the form of a list.

        If no parameters are given, everything from that table will be returned.

        Example usages:
        --------------
            ``User.retrieve() -> returns a list of all users``

            ``User.retrieve(id=1) -> returns a single user matching the id``

            ``User.retrieve(name="John") -> returns a list of all users with the name "John"``

        Parameters
        ----------
            data (**str) : Key word arguments for each of the column names and the values to try and match.

        Returns
        -------
            List of class instances created from the matching rows in the database.
        '''
        cols,vals = cls.format_data(data.keys())
        query = f"SELECT * FROM `{cls.table}` {'WHERE'+' AND'.join(f' {col}={val}' for col,val in zip(cols,vals)) if data else ''}"
        return [cls(**item) for item in  connectToMySQL(db).query_db(query,data)]
#-------------------Update---------------------#
    def update(self, **data):
        '''
        Updates the target instance in the database with the given data.

        Example usages:
        --------------
            ``my_user.update(name="Joe",age=24) -> updates my_user to now have the name of "Joe" and age of 24``

            ``my_user.update(**request.form) -> updates my_user based on the data recieved from the form``

        Parameters
        ----------
            data (**str) : Key word arguments for each of the column names and the new values to update with.

        Returns
        -------
            None if successful or False if query failed.
        '''
        cols,vals = self.format_data(data.keys())
        query = f"UPDATE `{self.table}` SET {', '.join(f'{col}={val}' for col,val in zip(cols,vals))} WHERE id={self.id}"
        return connectToMySQL(db).query_db(query,data)
#-------------------Delete---------------------#
    @classmethod
    def delete(cls, **data):
        '''
        Deletes all rows from the database that match the given data.

        Example usages:
        --------------
            ``User.delete(id=1) -> deletes user with the id of 1``

            ``User.delete(name="John") -> deletes all users with the name "John"``

        Parameters
        ----------
            data (**str) : Key word arguments for each of the column names and the values to try and match.

        Returns
        -------
            None if successful or False if query failed.
        '''
        cols,vals = cls.format_data(data.keys())
        query = f"DELETE FROM `{cls.table}` WHERE {' AND '.join(f'{col}={val}' for col,val in zip(cols,vals))}"
        return connectToMySQL(db).query_db(query,data)
#------------------Validate--------------------#
    @classmethod
    def validate(cls,**data):
        '''
        Validates the given data by applying any validators registered to the class via the validator decorator.

        If no validators are registered, then the data will always be considered valid.

        Example usages:
        --------------
            ``User.validate(**request.form) -> validates data from form``

            ``User.validate(name="abc",age="24") -> validates the given attributes``

        Parameters
        ----------
            data (**str) : Key word arguments for each of the field names and the values to be validated.

        Returns
        -------
            Boolean determining whether all of the data is valid or not
        '''
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
        '''
        Decorator used to register validators to a given class.

        The method below the decorator should be named the exact same
        as the field you are trying to validate and should return a boolean
        which will be used to determine if the field is valid or not.

        Parameters
        ----------
            msg (str): Error message for the specific validation
        '''
        def register(func):
            cls.validators = getattr(cls,"validators",{})
            cls.validators[func.__name__] = cls.validators.get(func.__name__,[])
            cls.validators[func.__name__].append((func,msg))
        return register
#----------------------------------------------#
    def __repr__(self):#more readable representation
        return f"<{self.table} obj: id={self.id}>"

    def __lt__(self,other):#allows sorting by id
        return self.id < other.id

    def __eq__(self,other):#allows checking equality
        return self.id == other.id