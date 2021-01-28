from services.patient_management_service import patient_service


def map_services(type_of_entrypoint, name_of_service, payload):
    """
    Function maps services based on name_of_service
    `type_of_entry_point`:
        type: String
        options: event, rest_api
    `name_of_service`:
        type: String
        options: currently supported `patient_management_service`
    `payload`:
        type: Dict
    """
    if name_of_service == "patient_management_service":
        return patient_service(type_of_entrypoint=type_of_entrypoint, name_of_service=name_of_service, payload=payload)
    else:
        return None
