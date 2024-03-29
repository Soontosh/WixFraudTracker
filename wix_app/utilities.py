"""
Utilities that will be commonly used throughout the project.
"""
import requests, json, logging, os, sys
from dotenv import load_dotenv, dotenv_values, find_dotenv
import inspect
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Utilities:
    """Stores all commonly used Utilities\n
    Requires initialization"""
    def __init__(self, json_dir: str, refresh_token: str) -> None:
        """
        Initialize the Utilities class.

        ### Args:
            json_dir ```str```: The directory where JSON data is stored.
            refresh_token ```str```: The refresh token used for access token retrieval.
        """
        # Initialize the Utilities class with JSON directory and refresh token
        self.json_dir = json_dir
        self.refresh_token = refresh_token

        # Create a session and set Content-Type header
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        self.session = session

        # Create a logger instance
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)

        # Create a console handler for logging errors to the console
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        # Create a formatter for log messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(ch)

        # Store the logger instance
        self.logger = logger


    def log(self, log_type: str, message: str):
        """
        Log a message with the specified logging type. Saves event log

        ### Args:
            log_type ```str```: The type of log message (```DEBUG```, ```INFO```, ```WARNING```, ```ERROR```, ```CRITICAL```).\n
            message ```str```: The message to log.

        ### Raises:
            ValueError: If an invalid log_type is provided.
        """
        # Define a mapping of log types to logging levels
        log_level_mapping = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL,
        }

        if log_type not in log_level_mapping:
            # Raise a ValueError and log error if log_type is not valid
            self.log("ERROR", f"Invalid logging type {log_type}. Line number: {inspect.currentframe().f_back.f_lineno}")
            raise ValueError(f"Invalid loggingType: {log_type}. It should be one of DEBUG, INFO, WARNING, ERROR, or CRITICAL.")

        #Create EventLog row

        # Set the logging level for the logger
        self.logger.setLevel(log_level_mapping[log_type])

        # Log the message with the specified logging level
        self.logger.log(log_level_mapping[log_type], message)
    
    def save_event_log(self, save_log_bool: bool, event_type: str, error: bool, error_type: str, error_message: str, json_data: str, invoice_num: int, email_id: int, current_log: str = "") -> str:
        """
        Save event to a row in DB. Returns log string w/ Event ID information\n

        ### Args:
            save_log_bool ```bool```: Whether or not a log will be saved to DB
            event_type ```str```: The type of event that took place. (```INVOICE SENT```, ```INVOICE PAID```, ```INVOICE OVERDUE```, ```EMAIL SENT```, ```EMAIL OPENED```) \n
            error ```bool```: Whether or not an error took place during this event. Defaults to ```False```\n
            error_message ```str```: Error message associated with the log. Defaults to ```None``` if not present\n
            json_data ```str```: JSON Data associated with the log, useful when dealing with errors. Defaults to ```None``` if not available\n
            invoice_num ```int```: The associated invoice's number. Defaults to ```None``` if not available \n
            email_id ```int```: The ID of the associated email. Defaults to ```None``` if not available \n
            current_log ```str```: The current log information as a string

        ### Handles and Logs:
        """

        #Get the current time in UTC

        #Get this
        #Event type
        #Error
        #Error Type
        #Error Message
        #Associated JSON Data
        #Associated Invoice(take in invoice number)
        #Associated Email(opt)

        #Try and get the error

        #Try and save

        #If unable to, log error w/ "log_event" as false
        pass

#Load environment variables
load_dotenv(find_dotenv('.env'))

#Initializing utilities
utilites = Utilities(f"{os.path.dirname(os.path.realpath(__file__))}\\JSONTemplates\\refresh_access_token.json", os.getenv("REFRESH_TOKEN"))