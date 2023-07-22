import os
import sqlite3

class DatabaseModel:
    """This class is a wrapper around the sqlite3 database. It provides a simple interface that maps methods
    to database queries. The only required parameter is the database file."""

    def __init__(self, database_file):
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    # Using the built-in sqlite3 system table, return a list of all tables in the database
    def get_table_list(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        return tables

    # Return the rows and column names
    def get_questions_content(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vragen.vraag, auteurs.voornaam FROM vragen, leerdoelen, auteurs WHERE leerdoelen.id == vragen.leerdoel AND vragen.auteur == auteurs.id AND vragen.leerdoel <= 7 LIMIT 10")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Convert int to string for each question
        for content in table_content:
            for tulpe in content:
                tulpe = str(tulpe)

        # Note that this method returns 2 variables!
        return table_content, table_headers

    # Return the rows and column names
    def get_learningobject_content(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM leerdoelen")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

    # Return the rows and column names
    def get_authors_content(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM auteurs")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers