'''this file contains the database collections structure'''

from pydantic import BaseModel, Field

class Item(BaseModel):
    '''Item collection has 6 fields
        name stores the user name (string type)
        email stores the user email address (string type)
        item_name stores the name of the item (string type)
        quantity stores the number of items (interger type)
        expiry_date stores the expiry date of the item (string type in format yyyy-mm-dd)
        insert_date store the date of insertion of the item (string type with default value as system date)
    '''
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: str = Field(format="YYYY-MM-DD")


class ClockInRecord(BaseModel):
    '''this cellection has 3 fields
        email stores the email address of the clock-in user (string type)
        location stores the location of the clock-in user (string type)
        insert_datetime field is autopopulated when user clocks in (string type with default value as system datetime)
    '''
    email: str
    location: str