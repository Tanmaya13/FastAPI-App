import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from bson import ObjectId

from db import items_collection, clock_in_records_collection, create
from collection import Item, ClockInRecord
from validation import PayloadValidator, UserPayloadValidator, serialize_document

app = FastAPI()

ITEM_NOT_FOUND_CONST = "Item not found"
INVALID_ITEM_ID_PROVIDED = "Invalid item id provided."
CLOCK_IN_RECORD_NOT_FOUND_CONST = "Clock-in record not found"
INVALID_CLOCK_IN_RECORD_ID_PROVIDED = "Invalid clock-in record id provided."

@app.get("/", tags=["Root"])
async def root():
    return {"info": "Welcome to my FastAPI app! Please add /docs at the end of the above URL to access the APIs."}

@app.post("/items", tags=["Item"])
def create_item(item: Item):
    '''validating create item payload'''
    payload_keys = ["name", "email", "item_name", "quantity", "expiry_date"]
    validate_payload = PayloadValidator(
        name=item.name,
        email=item.email,
        item_name=item.item_name,
        quantity=item.quantity,
        expiry_date=item.expiry_date,
        payload_keys=payload_keys
    )
    validated_data = validate_payload.validate()
    for key in payload_keys:
        if validated_data[key]:
            raise HTTPException(status_code=400, detail=validated_data[key])

    data = {
        "name": item.name,
        "email": item.email,
        "item_name": item.item_name,
        "quantity": item.quantity,
        "expiry_date": item.expiry_date,
        "insert_date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    '''inserting item details into the DB'''
    item = create(data, items_collection)

    return {"created successfully": True, "item_id" : str(item.inserted_id)}


@app.get("/items/filter", tags=["Item"])
def filter_items(
    email: Optional[str] = None,
    expiry_date: Optional[str] = None,
    insert_date: Optional[str] = None,
    quantity: Optional[int] = None
):
    filters = {}
    if email:
        filters["email"] = email
    if expiry_date:
        filters["expiry_date"] = {"$gte": expiry_date}
    if insert_date:
        filters["insert_date"] = {"$gte": insert_date}
    if quantity:
        filters["quantity"] = {"$gte": quantity}

    items = items_collection.find(filters)
    res = []
    for item in items:
        res.append(serialize_document(item))

    if len(res) == 0:
        return {"records": "No matching records found."}
    
    return res


@app.get("/items/aggregate", tags=["Item"])
def aggregate_items():
    pipeline = [
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]
    results = items_collection.aggregate(pipeline)
    return list(results)


@app.get("/items/{item_id}", tags=["Item"])
def get_item(item_id: str):
    '''validating and converting item_id to ObjectId type'''
    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail=INVALID_ITEM_ID_PROVIDED)

    '''searching for the matching item record in the DB'''
    item = items_collection.find_one({"_id": object_id})

    '''raising error exception if no matching record is found'''
    if item is None:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND_CONST)
    
    return {"item_details": serialize_document(item)}


@app.delete("/items/{item_id}", tags=["Item"])
def delete_item(item_id: str):
    '''validating and converting item_id to ObjectId type'''
    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail=INVALID_ITEM_ID_PROVIDED)

    '''deleting record from D'''
    result = items_collection.delete_one({"_id": object_id})

    '''raising exception if no matching record is found'''
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND_CONST)

    return {"message": "Item deleted successfully"}


@app.put("/items/{item_id}", tags=["Item"])
def update_item(item_id: str, item: Item):
    payload_keys = ["name", "email", "item_name", "quantity", "expiry_date"]
    validate_payload = PayloadValidator(
        name=item.name,
        email=item.email,
        item_name=item.item_name,
        quantity=item.quantity,
        expiry_date=item.expiry_date,
        payload_keys=payload_keys
    )
    validated_data = validate_payload.validate()
    for key in payload_keys:
        if validated_data[key]:
            raise HTTPException(status_code=400, detail=validated_data[key])

    item_dict = item.dict(exclude={"insert_date"})
    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(status_code=400, detail=INVALID_ITEM_ID_PROVIDED)

    result = items_collection.update_one({"_id": object_id}, {"$set": item_dict})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND_CONST)

    return {"message": "Item updated successfully"}



@app.post("/clock-in", tags=["User"])
def create_clock_in_record(clock_in_record: ClockInRecord):
    '''clock in record payload validation'''
    payload_keys = ["email", "location"]
    validate_payload = UserPayloadValidator(
        email=clock_in_record.email,
        location=clock_in_record.location,
        payload_keys=payload_keys
    )
    validated_data = validate_payload.validate()
    for key in payload_keys:
        if validated_data[key]:
            raise HTTPException(status_code=400, detail=validated_data[key])

    clock_in_record_dict = {
        "email": clock_in_record.email,
        "location": clock_in_record.location,
        "insert_datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    '''creating clock in record'''
    resp = create(clock_in_record_dict, clock_in_records_collection)

    return {"ok": "clock-in successful", "clock-in id": str(resp.inserted_id)}



@app.get("/clock-in/filter", tags=["User"])
def filter_clock_in_records(
    email: Optional[str] = None,
    location: Optional[str] = None,
    insert_datetime: Optional[str] = None
):
    filters = {}
    if email:
        filters["email"] = email
    if location:
        filters["location"] = location
    if insert_datetime:
        filters["insert_datetime"] = {"$gte": insert_datetime}

    clock_in_records = clock_in_records_collection.find(filters)
    res = []
    for record in clock_in_records:
        res.append(serialize_document(record))

    if len(res) == 0:
        return {"records": "No matching records found."}

    return res


@app.get("/clock-in/{clock_in_record_id}", tags=["User"])
def get_clock_in_record(clock_in_record_id: str):
    '''validating and converting clock in id to objectId type'''
    try:
        object_id = ObjectId(clock_in_record_id)
    except Exception:
        raise HTTPException(status_code=400, detail=INVALID_CLOCK_IN_RECORD_ID_PROVIDED)

    '''finding record from DB'''
    clock_in_record = clock_in_records_collection.find_one({"_id": object_id})

    '''raising exceptionif no matching record is found'''
    if clock_in_record is None:
        raise HTTPException(status_code=404, detail=CLOCK_IN_RECORD_NOT_FOUND_CONST)

    return {"clock_in_record_details": serialize_document(clock_in_record)}


@app.delete("/clock-in/{clock_in_record_id}", tags=["User"])
def delete_clock_in_record(clock_in_record_id: str):
    '''validating and converting clock in id to objectId type'''
    try:
        object_id = ObjectId(clock_in_record_id)
    except Exception:
        raise HTTPException(status_code=400, detail=INVALID_CLOCK_IN_RECORD_ID_PROVIDED)

    '''deleting record from DB'''
    result = clock_in_records_collection.delete_one({"_id": object_id})

    '''raising exception if no matching record is found'''
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=CLOCK_IN_RECORD_NOT_FOUND_CONST)

    return {"message": "Clock-in record deleted successfully"}


@app.put("/clock-in/{clock_in_record_id}", tags=["User"])
def update_clock_in_record(clock_in_record_id: str, clock_in_record: ClockInRecord):
    '''validating and converting clock in id to objectId type'''
    try:
        object_id = ObjectId(clock_in_record_id)
    except Exception:
        raise HTTPException(status_code=400, detail=INVALID_CLOCK_IN_RECORD_ID_PROVIDED)
    
    '''payload validation'''
    payload_keys = ["email", "location"]
    validate_payload = UserPayloadValidator(
        email=clock_in_record.email,
        location=clock_in_record.location,
        payload_keys=payload_keys
    )
    validated_data = validate_payload.validate()
    for key in payload_keys:
        if validated_data[key]:
            raise HTTPException(status_code=400, detail=validated_data[key])

    clock_in_record_dict = {
        "email": clock_in_record.email,
        "location": clock_in_record.location
    }

    clock_in_record_dict = clock_in_record.dict(exclude={"insert_datetime"})

    '''updating record in DB'''
    result = clock_in_records_collection.update_one({"_id": object_id}, 
                                                    {"$set": clock_in_record_dict})
    
    '''if no record found raise exception'''
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail=CLOCK_IN_RECORD_NOT_FOUND_CONST)
    return {"message": "Clock-in record updated successfully"}
