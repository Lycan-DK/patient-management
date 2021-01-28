import json
from services.main_service_mapper import map_services


def lambda_handler(event, context):
    if not isinstance(event, dict):
        event = event.to_dict()
    payload = {
        "context": event.get("context"),
        "source": event.get("source")
    }
    type_of_entrypoint = "event"
    name_of_service = "patient_management_service"
    return map_services(type_of_entrypoint=type_of_entrypoint,
                        name_of_service=name_of_service, payload=payload)
