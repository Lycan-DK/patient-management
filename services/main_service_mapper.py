from services.patient_management_service import patient_service


def map_services(type_of_entrypoint, name_of_service, payload):
    if name_of_service == "patient_management_service":
        return patient_service(type_of_entrypoint=type_of_entrypoint, name_of_service=name_of_service, payload=payload)
    else:
        return None
