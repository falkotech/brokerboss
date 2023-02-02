from log_config import logging
import subprocess
import psutil

class InvalidAccessException(Exception):
    pass

class BrokerManager():
    """Broker manager class."""
    config_changed = False
    DEFAULT_CONFIG_LOGGING = """log_dest stderr\nlog_dest file /mosquitto/log/mosquitto.log\nlog_timestamp_format %Y-%m-%dT%H:%M:%S\n"""
    @staticmethod
    def start_broker() -> bool:
        try:
            # Start the Mosquitto process detached (-d) with config file (-c /file/path)
            psutil.Popen(['mosquitto','-d', '-c', '/mosquitto/config/mosquitto.conf'], start_new_session=True)
            # Reset the config_changed flag
            BrokerManager.config_changed = False
            return True 
            # You need to use BrokerManager.is_running() to check if the broker is running. 
            # This just returns True if there were no errors starting the broker.
        except Exception as e:
            logging.error(f"start_broker: {e}, type: {type(e)}")
            return False


    @staticmethod
    def stop_broker()-> bool:
        try:
            # Find the Mosquitto process
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'mosquitto':
                    # Stop the Mosquitto process
                    proc.terminate()
                    # proc.kill()
                    return True
        except Exception as e:
            logging.error(f"stop_broker: {e}, type: {type(e)}")
            return False


    
    @staticmethod
    def is_running()-> bool:
        try:
            # Check if the Mosquitto broker is running
            for process in psutil.process_iter(['name']):
                if process.info['name'] == 'mosquitto' and process.status() in ['running', 'sleeping']:
                    return True
            return False
        except Exception as e:
            logging.error(f"is_running: {e}, type: {type(e)}")
            return False

        

    @staticmethod
    def list_users() -> list:
        """List the users from the Mosquitto MQTT broker"""
        users = []
        try:
            # Open the pw.txt file
            with open('/mosquitto/config/pw.txt', 'r') as f:
                # Read each line of the file
                for line in f:
                    #skip empty lines
                    if  len(line.strip()) == 0:
                        continue
                    # Split the line into username and password
                    username, _password = line.strip().split(':')
                    # Add the username to the list
                    users.append({'username': username})
        except Exception as e:
            logging.error(f"Error opening pw.txt: {e}")
        return users

    @staticmethod
    def user_exists(username: str) -> bool:
        """Check if a user exists in the Mosquitto MQTT broker"""
        # Get the list of users
        users = BrokerManager.list_users()
        # Check if the username is in the list
        return username in users
    
    @staticmethod
    def get_ports() -> list:
        """Get the ports from the Mosquitto MQTT broker"""
        ports = []
        config_dict = BrokerManager.config_to_dict()
        if config_dict:
            listeners = config_dict.get('listener', [])
            for listener in listeners:
                port = listener.get('port', None)
                if port:
                    ports.append(port)
        else:
            logging.error("Error getting ports from config file")
            ports.append("Error getting ports from config file")
        return ports

    @staticmethod
    def get_version() -> str:
        """Get the version of the Mosquitto MQTT broker"""
        try:
            result = subprocess.run(['mosquitto', '-h'], stdout=subprocess.PIPE)
            return str(result.stdout).replace("\\n", " ").split(" ")[2]
        except Exception as e:
            logging.error(f"Error getting version: {e}, type: {type(e)}")
            return "Error getting version"



    @staticmethod
    def add_user(username: str, password: str, pw_file='/mosquitto/config/pw.txt') -> bool:
        """
        Add a user to the mosquitto MQTT broker
        - This will add the user to the password file

        :param username: The username of the user to add
        :param password: The password of the user to add
        :return: A boolean indicating if the user was added successfully
        """
        # Check if the user already exists and exit if so
        if BrokerManager.user_exists(username):
            logging.error(f"User {username} already exists")
            return False
        #TODO prevent injection attacks, check username and password are valid
        try:
            result = subprocess.run(['mosquitto_passwd', '-b', pw_file, username, password])
            # Check the result of the command
            if result.returncode == 0:
                # Change flag to indicate that the config file has changed
                BrokerManager.config_changed = True
                # Return a response to the client
                return True # Success
            else:
                return False # Error
        except Exception as e:
            logging.error(f"Error adding user {username}: {e}")
            return False
    

    @staticmethod
    def delete_user(username: str) -> bool:
        """
        Delete a user from the mosquitto MQTT broker
        - This will delete the user from the password file
        - This will delete the user from the ACL file
        
        :param username: The username of the user to delete
        :return: A boolean indicating if the user was deleted successfully
        """
        #TODO prevent injection attacks, check username is valid
        try:
            # Delete the user from the ACL file
            acl_dict = BrokerManager.acl_to_dict(acl_file='/mosquitto/config/acl.acl')
            del acl_dict ["user_acl"][username]
            BrokerManager.dict_to_acl(acl_dict, acl_file='/mosquitto/config/acl.acl')
            
            # Delete the user from the password file
            result = subprocess.run(['mosquitto_passwd', '-D', '/mosquitto/config/pw.txt', username])
            # Check the result of the command
            if result.returncode == 0:
                # Change flag to indicate that the config file has changed
                BrokerManager.config_changed = True
                # Return a response to the client
                return True # Success
            else:
                return False # Error
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            return False
    
    

    @staticmethod
    def edit_user(username: str, password: str) -> bool:
        """
        Edit a user in the mosquitto MQTT broker

        :param username: The username of the user to edit
        :param password: The password of the user to edit
        :return: A boolean indicating if the user was edited successfully
        """
        # Check if the user already exists and exit if not
        if not BrokerManager.user_exists(username):
            logging.error(f"Error editing password for user {username}: User does not exist")
            return False
        #TODO prevent injection attacks, check username and password are valid
        #TODO right now this method is very similar to add_user, maybe refactor to use a common method? Or, as program grows, methods will diverge.
        try:
            result = subprocess.run(['mosquitto_passwd', '-b', '/mosquitto/config/pw.txt', username, password])
            # Check the result of the command
            if result.returncode == 0:
                # Return a response to the client
                return True # Success
            else:
                return False # Error
        except Exception as e:
            logging.error(f"Error editing password for user {username}: {e}")
            return False


    @staticmethod
    def config_to_dict(config_file="/mosquitto/config/mosquitto.conf") -> dict:
        config_dict = {}
        listeners = []
        content = ""
        try:
            #TODO add default configuration lines for BrokerBoss?
            with open(config_file, "r") as file:
                content = file.read()
            lines = content.split("\n")
            if BrokerManager.DEFAULT_CONFIG_LOGGING in content:
                config_dict['enable_logging'] = True 
            for line in lines:
                # clear trailing and leading whitespace
                line = line.strip()
                # Skip empty and commented lines
                if line.startswith("#") or line == "":
                    continue
                if line.startswith("log_"):
                    continue
                # Split the line into key and value(s)
                key, *value = line.split()
                # *value creates a list of values, so if there is only one value, 
                # we need to get the first element of that list
                if len(value) == 1:
                    value = value[0]
                # Convert string values to boolean otherwise "False" returns True 
                if type(value) == str and value.lower() == "false":
                    value = False
                # Iterate over the listeners 
                # and transform them into a list of dicts like this: 
                # listener.[{'port': 1883, 'protocol': 'mqtt'},{'port': 8883, 'protocol': 'mqtt'}]
                # because the form expects a list of dicts
                if key == "listener":
                    listeners.append({"port": value, "protocol": "mqtt"})
                # protocol is a subkey of listener, and should always be defined after a listener. 
                # So we need to add it to the last listener
                elif key == "protocol":
                    listeners[-1]["protocol"] = value
                else:
                    config_dict[key] = value
            config_dict["listener"] = listeners
            return config_dict
        except FileNotFoundError as e:
            logging.error(f"Error loading config file into dict: {e}, Config file not found, Type: {type(e)}")
            return False
        except PermissionError as e:
            logging.error(f"Error loading config file into dict: {e}, Permission denied, Type: {type(e)}")
            return False
        except Exception as e:
            logging.error(f"Error loading config file into dict: {e}, Type: {type(e)}")
            return False

    @staticmethod
    def dict_to_config(config_dict) -> bool:
        """Update the Mosquitto MQTT broker config file"""
        # update config file with data from form
        try:
            with open("/mosquitto/config/mosquitto.conf", "w") as config_file:
                for key, value in config_dict.items():
                    if key == "enable_logging":
                        if value:
                            config_file.write(BrokerManager.DEFAULT_CONFIG_LOGGING)
                        continue
                    # Convert boolean values to string otherwise "False" returns an error because of the capital F
                    if type(value) == bool:
                        value = str(value).lower()

                    config_file.write(f"{key} {value}\n")

                BrokerManager.config_changed = True
                return True
        except Exception as e:
            logging.error(f"Error updating config file: {e}, Type: {type(e)}")
            return False




    @staticmethod
    def dict_to_acl(acl_dict: dict, acl_file: str) -> bool:
        """
        Convert the Mosquitto MQTT broker ACL file to a dictionary
        The dictionary will have the following format:
        {
            "user_acl": {
                "username1": {
                    "topic": "access",
                    ...
                },
                "username2": {
                    "other_topic": "access",
                    ...
                }
            },
            "pattern_acl": {
                "pattern": "access",
                ...
            },
        }
        Keys in the "user_acl" dictionary are usernames
        Keys in the "pattern_acl" dictionary are topic patterns
        Values are access levels (read, write, readwrite)
        :return: bool indicating success
        """
        try:
            # Open the ACL file
            with open(acl_file, 'w') as f:
                # Iterate over the patterns
                for pattern, access in acl_dict["pattern_acl"].items():
                    # Write the pattern
                    f.write(f'pattern {pattern} {access}\n')
                # Write a blank line after the patterns
                f.write('\n')
                # Iterate over the users
                for username, rules in acl_dict["user_acl"].items():
                    # Write the username
                    f.write(f'user {username}\n')
                    # Iterate over the rules
                    for topic, access in rules.items():
                        # Write the rule
                        f.write(f'topic {topic} {access}\n')
                    # Write a blank line after each user
                    f.write('\n')
            # Set the config_changed flag
            BrokerManager.config_changed = True
            return True
        except FileNotFoundError:
            logging.error("Error when updating ACL file: File not found")
            return False
        except PermissionError:
            logging.error("Error when updating ACL file: Permission Error")
            return False
        except Exception as e:
            logging.error(f"Error when updating ACL file: {e}")
            return False


    @staticmethod
    def acl_to_dict(acl_file: str) -> dict:
        """
        Convert the Mosquitto MQTT broker ACL file to a dictionary
        :return: dictionary representation of the ACL file
        """
        acl_dict = {
            "user_acl": {},
            "pattern_acl": {}
        }
        try:
            with open(acl_file, 'r') as f:
                current_user = None
                for line in f:
                    line = line.strip()
                    # ignore blank lines
                    if len(line) == 0:
                        continue
                    # check if the line starts with 'user'
                    if line.startswith("user"):
                        current_user = line.split()[1]
                        acl_dict["user_acl"][current_user] = {}
                    # check if the line starts with 'pattern'
                    elif line.startswith("pattern"):
                        pattern, access = line.split()[1:]
                        acl_dict["pattern_acl"][pattern] = access
                    # if none of the above, it must be a rule
                    elif line.startswith("topic"):
                        topic, access = line.split()[1:]
                        acl_dict["user_acl"][current_user][topic] = access
        except FileNotFoundError:
            logging.error("Error when reading ACL file: File not found")
        except PermissionError:
            logging.error("Error when reading ACL file: Permission Error")
        except Exception as e:
            logging.error(f"Error when reading ACL file: {e}")
        return acl_dict



    @staticmethod
    def add_acl_pattern_rule(pattern: str, read, write) -> bool:
        acl_dict = BrokerManager.acl_to_dict('/mosquitto/config/acl.acl')
        try:
            acl_dict["pattern_acl"][pattern] = BrokerManager._access_to_string(read, write)
            return True if BrokerManager.dict_to_acl(acl_dict, '/mosquitto/config/acl.acl') else False
        except InvalidAccessException as e:
            logging.error(e)
            return False
        except Exception as e:
            logging.error(f"Error adding ACL pattern rule: {e}")
            return False

    @staticmethod
    def delete_acl_pattern_rule(pattern) -> bool:
        acl_dict = BrokerManager.acl_to_dict('/mosquitto/config/acl.acl')
        try:
            del acl_dict["pattern_acl"][pattern]
            return True if BrokerManager.dict_to_acl(acl_dict, '/mosquitto/config/acl.acl') else False
        except KeyError:
            logging.error(f"Error deleting ACL pattern rule: {pattern} not found")
            return False
        except Exception as e:
            logging.error(f"Error deleting ACL pattern rule: {e}")
            return False


    @staticmethod
    def add_acl_user_rule(usr, topic, read, write):
        #TODO dont hardcode path to acl file
        acl_dict = BrokerManager.acl_to_dict('/mosquitto/config/acl.acl')
        try:
            if usr not in acl_dict["user_acl"]:
                acl_dict["user_acl"][usr] = {}
            usr_dict = acl_dict["user_acl"][usr]
            usr_dict[topic] = BrokerManager._access_to_string(read, write)
            return True if BrokerManager.dict_to_acl(acl_dict, '/mosquitto/config/acl.acl') else False
        except InvalidAccessException as e:
            logging.error(f"Error adding ACL user rule: {e}")
            return False
        except Exception as e:
            logging.error(f"Error adding ACL user rule: {e}")
            return False

    @staticmethod
    def delete_acl_user_rule(usr, topic):
        acl_dict = BrokerManager.acl_to_dict('/mosquitto/config/acl.acl')
        try:
            del acl_dict["user_acl"][usr][topic]
            return True if BrokerManager.dict_to_acl(acl_dict, '/mosquitto/config/acl.acl') else False
        except KeyError:
            logging.error(f"Error deleting ACL user rule: {topic} not found")
            return False
        except Exception as e:
            logging.error(f"Error deleting ACL user rule: {e}, Type: {type(e)}")
            return False

    @staticmethod
    def _access_to_string(read, write):
        def is_true(value):
            true_values = {"true", "t", "yes", "1"}
            if type(value) == str:
                return value.lower() in true_values
            elif type(value) in [int, bool]:
                return value == 1
            else:
                return False

        can_read, can_write = is_true(read), is_true(write)

        if can_read and can_write:
            return "readwrite"
        elif can_read:
            return "read"
        elif can_write:
            return "write"
        else:
            # Raise error if read and write are both false. 
            # Because the mosquitto default is to allow readwrite access if read and write are not specified
            # However, this is not the desired behaviour for this application as it would be confusing in the frontend
            raise InvalidAccessException("Invalid access specified: expected read, write or readwrite")