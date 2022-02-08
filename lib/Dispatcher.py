import json
import logging
import copy
from .Request import *


class Dispatcher(object):
    """
    Requests dispatcher class
    """

    
    def __init__(self, config_params):
        self.logger = logging.getLogger(__name__)


    def request_switcher(self, json_message, session_id, config_params):
        """
        Getting request from JSON message. Selecting by request and execute function.  
        """
        
        RequestObj = Request()
        
        try:
            json_dict = json.loads(json_message)
            if not json_dict:
                self.logger.info("Session ID: %s, error: string could not be converted to json" %session_id)
                return {"error": "string could not be converted to json"}
            self.logging_local("Received request" , json_dict, session_id, config_params)
            request =  json_dict['request']
            switcher = {
                'getdata_1': RequestObj.getdata_1,
                'getdata_2': RequestObj.getdata_2,
            }
            # Get the function from switcher dictionary
            cmd_execute = switcher.get(request, lambda null_arg0,null_arg1,null_arg2: {"error": "invalid request"})
            # Execute the function
            json_reply = cmd_execute(json_dict, config_params)
            self.logging_local("Sended reply" , json_reply, session_id, config_params)
            return json_reply
        except ValueError:
            self.logging_local("Sended reply" , {"error": "string could not be converted to json"}, session_id, config_params)
            return {"error": "string could not be converted to json"}


    def logging_local(self, sendreceive, in_message, session_id, config_params):
        """
        Logging messages
        """

        out_message = copy.copy(in_message)
        if 'error' in out_message:
            self.logger.error("Session ID: %s, %s: %s" % (session_id, sendreceive, out_message))
        else:
            for key_hidden_value in config_params['hidden_keys']:
                if key_hidden_value in out_message:
                    out_message[key_hidden_value] = u'*******'
            self.logger.info("Session ID: %s, %s: %s" % (session_id, sendreceive, out_message))
