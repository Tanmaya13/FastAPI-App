import re
import datetime

def serialize_document(doc):
    if doc is None:
        return None
    doc['_id'] = str(doc['_id'])
    return doc

class PayloadValidator():
    def __init__(self, name=None, email=None, item_name=None, quantity=None, expiry_date=None, insert_date=None, payload_keys=None):
        self.name = name
        self.email = email
        self.item_name = item_name
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.insert_date = insert_date
        self.payload_keys = payload_keys

    def validate_name(self):
        err_msg = None
        if self.name is None:
            err_msg = "name key is missing in the payload."
        elif not isinstance(self.name, str):
            err_msg = "User name should be in string."
        elif len(self.name) == 0:
            err_msg = "name field cannot be empty."
        return err_msg

    def validate_email(self):
        err_msg = None
        if self.email is None:
            err_msg = "email key is missing in the payload."
        elif not isinstance(self.email, str):
            err_msg = "email should be in string."
        elif len(self.email) == 0:
            err_msg = "email field cannot be empty."
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid_email = re.match(pattern, self.email) is not None
        if not valid_email:
            err_msg = "please provide a valid email."
        return err_msg

    def validate_item_name(self):
        err_msg = None
        if self.name is None:
            err_msg = "item_name key is missing in the payload."
        elif not isinstance(self.name, str):
            err_msg = "Item name should be in string."
        elif len(self.name) == 0:
            err_msg = "Item name field cannot be empty."
        return err_msg

    def validate_quantity(self):
        err_msg = None
        if self.quantity is None:
            err_msg = "quantity key is missing in the payload."
        elif not isinstance(self.quantity, int):
            err_msg = "Item's quantity should be in integers."
        elif self.quantity < 0:
            err_msg = "Please provide valid item quantity count."
        return err_msg

    def validate_expiry_date(self):
        err_msg = None
        if self.expiry_date is None:
            err_msg = "expiry_date key is missing in the payload."
        elif not isinstance(self.expiry_date, str):
            err_msg = "Item expiry_date should be in string."
        elif len(self.expiry_date) == 0:
            err_msg = "Please provide an item expiry_date."
        try:
            datetime.datetime.strptime(self.expiry_date, "%Y-%m-%d")
        except ValueError:
            err_msg = "Please provide expiry date in yyyy-mm-dd format"
        return err_msg
    
    def validate_insert_date(self):
        err_msg = None
        if self.insert_date is None:
            err_msg = "insert_date key is missing in the payload."
        elif not isinstance(self.insert_date, str):
            err_msg = "Item insert_date should be in string."
        elif len(self.insert_date) == 0:
            err_msg = "Please provide an item insert_date."
        try:
            datetime.datetime.strptime(self.insert_date, "%Y-%m-%d")
        except ValueError:
            err_msg = "Please provide insert date in yyyy-mm-dd format."
        return err_msg


    def validate(self):
        validated_payload = {}
        for key in self.payload_keys:
            validate_method = f"validate_{key}"
            method = getattr(self, validate_method)
            response = method()
            validated_payload[key] = response
        return validated_payload
    


class UserPayloadValidator():
    def __init__(self, email=None, location=None, payload_keys=None):
        self.email = email
        self.location = location
        self.payload_keys = payload_keys

    def validate_email(self):
        err_msg = None
        if self.email is None:
            err_msg = "email key is missing in the payload."
        elif not isinstance(self.email, str):
            err_msg = "email should be in string."
        elif len(self.email) == 0:
            err_msg = "email field cannot be empty."
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid_email = re.match(pattern, self.email) is not None
        if not valid_email:
            err_msg = "please provide a valid email."
        return err_msg
    
    def validate_location(self):
        err_msg = None
        if self.location is None:
            err_msg = "location key is missing in the payload."
        elif not isinstance(self.location, str):
            err_msg = "User location should be in string."
        elif len(self.location) == 0:
            err_msg = "location field cannot be empty."
        return err_msg

    def validate(self):
        validated_payload = {}
        for key in self.payload_keys:
            validate_method = f"validate_{key}"
            method = getattr(self, validate_method)
            response = method()
            validated_payload[key] = response
        return validated_payload
    

