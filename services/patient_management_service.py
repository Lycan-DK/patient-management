import json
import uuid
from adapters.dynamodb.dyanmo_db_init import DynamoDBInit
from adapters.dynamodb.dynamo_db_functionalities import get_all, search, add_one, update_one, delete_one
from datetime import datetime, timezone


def patient_service(type_of_entrypoint, name_of_service, payload):
    """
    Supported context:
        - `get_all`
        - `get_one_patient`
        - `delete_one_patient`
        - `update_one_patient`
        - `add_one_patient`
    NOTE: type_of_entrypoint can be used later on providing custom response based on entrypoint.
    """
    source = payload.get("source")
    context = payload.get("context")
    table = DynamoDBInit(config={"table_name": "testPatientData1"}).table
    if context == "get_all":
        return get_all_patient(table=table)
    if context == "get_one_patient":
        return search_patient(table=table, query_params=source)
    if context == "add_one_patient":
        return add_patient(table=table, source=source)
    if context == "update_one_patient":
        return update_patient(table=table, source=source)
    if context == "delete_one_patient":
        return delete_patient(table=table, source=source)
    return None


def get_all_patient(table):
    response = get_all(table=table)
    return response


def search_patient(table, query_params):
    """
    query_params structure:
        {
        id: id of patient record
        }
    """
    if not isinstance(query_params, dict):
        query_params = query_params.to_dict()
    response = search(table=table, query_params=query_params)
    return response


def add_patient(table, source):
    """
    source structure: 
        -first_name: String
                    Required
        -last_name: String
                    Required
        -age: Int
            Required
        -gender: String
                Required
        -state: String
                Required
        -country: String
                Required
        -email: String
                Required
    """
    if not isinstance(source, dict):
        source = source.to_dict()
    id = '{}'.format(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    patient_object = {
        "id": id,
        "first_name": source.get("first_name"),
        "last_name": source.get("last_name"),
        "age": source.get("age"),
        "gender": source.get("gender"),
        "state": source.get("state"),
        "country": source.get("country"),
        "email": source.get("email"),
        "created_at": created_at
    }
    response = add_one(table=table, data=patient_object)
    if 200 <= response.get("ResponseMetadata").get("HTTPStatusCode") < 400:
        return {
            "status": 200,
            "message": "added patient first_name : {} , last_name: {}  with id :{}".format(source.get("first_name"), source.get("last_name"), id)
        }
    else:
        return{
            "status": response.get("ResponseMetadata").get("HTTPStatusCode"),
            "message": response
        }


def update_patient(table, source):
    """
    source structure: 
        -first_name: String
                    Required
        -last_name: String
                    Required
        -age: Int
            Required
        -id : String
            Required
    """
    if not isinstance(source, dict):
        source = source.to_dict()
    id = source.pop("id")
    response = update_one(table=table, id=id, data=source)
    if 200 <= response.get("ResponseMetadata").get("HTTPStatusCode") < 400:
        return {
            "status": 200,
            "message": "updated patient info  with id :{}".format(id)
        }
    else:
        return{
            "status": response.get("ResponseMetadata").get("HTTPStatusCode"),
            "message": response
        }


def delete_patient(table, source):
    """
    source structure:
        {
            id: id of patient record to be deleted
        }
    """
    id = source.get("id")
    if id is None:
        return {
            "status": 400,
            "message": "Need ID to delete the patient record"
        }
    response = delete_one(table=table, id=id)
    if 200 <= response.get("ResponseMetadata").get("HTTPStatusCode") < 400:
        return {
            "status": 200,
            "message": "deleted patient with id :{}".format(id)
        }
    else:
        return{
            "status": response.get("ResponseMetadata").get("HTTPStatusCode"),
            "message": response
        }
