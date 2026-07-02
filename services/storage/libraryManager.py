from .dataBaseHandler import dataBaseHandler
import logging
import uuid



logger = logging.getLogger(__name__)

class LibraryManager:
    def __init__(self):
        self.db = dataBaseHandler()

    def ensure_default_user(self):
        """Checks for existing users and creates a default 'user' if none exist."""
        # Querying the database to see if any user exists
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT user_id FROM USERS LIMIT 1")
            existing_user = cursor.fetchone()

        if not existing_user:
            default_user = {
                'user_id': 'user',
                'user_name': 'User',
                'light_mode': 1
            }
            self.db.create_entity('USERS', default_user)
            logger.info("No users in the DB, creating a default user - user_id: user")
        else:
            logger.info("Database has users in it")


    def addLibrary(self, user, library, type):
        '''
        Adds a library to a user. Users can have many libraries

        Args:
        user_name (str): The name of the user.
        server_name (str): The server identifier to store.
        '''
        new_library = {
                'library_id': self.generateUUID,
                'name': library,
                'type': type
            }
        self.db.create_record(library,)

    
    def addServer(self, user_name, server_name):
        """
        Updates the selected server for a user.
        
        Args:
            user_name (str): The name of the user.
            server_name (str): The server identifier to store.
        """
        self.db.change_field_by_xLookup(
            table='USERS',
            target_column='servers',
            new_value=server_name,
            search_column='user_name',
            search_value=user_name
        )
        logger.info(f"Updated server for {user_name} to {server_name}")


    def generateUUID():
        my_uuid = uuid.uuid4()
        return str(my_uuid)