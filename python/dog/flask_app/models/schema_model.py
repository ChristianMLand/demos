from typing import List,Tuple
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db

#TODO more error handling

class Schema:
    '''
    A class to that holds methods for basic sql queries.

    Classes that represent tables in your database should
    extend this class.

    ...

    Methods:
    --------
    create(cls,**data):
        Creates a new row in the database with the given data
    
    retrieve(cls,**data):
        Returns a list of rows from the database that match the given data
    
    update(cls,**data):
        Updates a row in the database with the given data

    delete(cls,**data):
        Deletes a row from the database that matches the given data

    validate(cls, **data):
        Runs any registered validators against given data and returns if valid or not
    '''
    @staticmethod#can be called either by the class directly or an instance of the class
    def format_data(columns:List[str]) -> Tuple[List[str],List[str]]:
        """
        Formats given data in a way that is safe to pass into a sql query without risk of sql injection

        Parameters
        ----------
        columns : list[str]
            list of column names

        Returns
        -------
            cols : list[str]
                list of escaped column names
            vals : list[str]
                list of formatted variable names 
        """
        cols = [f'`{col}`' for col in columns]
        vals = [f'%({col})s' for col in columns]
        return cols,vals
#-------------------Create---------------------#
    @classmethod
    def create(cls, **data):
        '''
        Creates a new row in the database based on the given data

        Parameters
        ----------
        data : dict[str,str]
            key word arguments for each of the columns and the values to create

        Returns
        -------
            new instance of the given class
        '''
        cols,vals = cls.format_data(data.keys())
        query = f"INSERT INTO `{cls.table}` ({', '.join(cols)}) VALUES ({', '.join(vals)})"
        new_id = connectToMySQL(db).query_db(query,data)
        return cls(id=new_id,**data)
#-------------------Retrieve-------------------#
    @classmethod
    def retrieve(cls, **data):#if no data passed in, select all, otherwise filter by whatever keyword arguments are passed in
        '''
        Retrieves everything from the database that matches the given data in the form of a list.

        If no parameters are given, everything from that table will be returned.

        If only one match was found, returns just the single element.

        Parameters
        ----------
        data : dict[str,str]
            key word arguments for each of the columns and their values to try and match against

        Returns
        -------
            list of class instances created from the matching rows in the database
        '''
        cols,vals = cls.format_data(data.keys())
        query = f"SELECT * FROM `{cls.table}` {'WHERE'+' AND'.join(f' {col}={val}' for col,val in zip(cols,vals)) if data else ''}"
        results = [cls(**item) for item in  connectToMySQL(db).query_db(query,data)]
        return results[0] if len(results) == 1 else results
#-------------------Update---------------------#
    @classmethod
    def update(cls, **data):#TODO update instance as well
        '''
        Updates the target row in the database with the given data

        Parameters
        ----------
        data : dict[str,str]
            key word arguments for each of the columns and their values to update to

        Returns
        -------
            None
        '''
        cols,vals = cls.format_data(data.keys())
        query = f"UPDATE `{cls.table}` SET {', '.join(f'{col}={val}' for col,val in zip(cols,vals))} WHERE id=%(id)s"
        return connectToMySQL(db).query_db(query,data)
#-------------------Delete---------------------#
    @classmethod
    def delete(cls, **data):
        '''
        Deletes a row from the database that matches the given data

        Parameters
        ----------
        data : dict[str,str]
            key word arguments for each of the columns and their values to try and match against

        Returns
        -------
            None
        '''
        cols,vals = cls.format_data(data.keys())
        query = f"DELETE FROM `{cls.table}` WHERE {' AND '.join(f'{col}={val}' for col,val in zip(cols,vals))}"
        return connectToMySQL(db).query_db(query,data)
#------------------Validate--------------------#
    @classmethod
    def validate(cls,**data):
        '''
        Validates the given data by passing it into any validators registered to the class
        with the validator decorator.

        If no validators are registered, then the data will always be considered valid.

        Parameters
        ----------
        data : dict[str,str]
            key word arguments for each of the fields and their values to be validated

        Returns
        -------
            Bool : whether all of the data is valid or not
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
        determining whether the field is valid or not.

        Parameters
        ----------
        msg : dict[str,str]
            Error message for the specific validation
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