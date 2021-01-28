import uuid
from datetime import datetime, timezone


def get_all(table):
    records = table.scan()
    return records


def search(table, query_params):
    if not isinstance(query_params, dict):
        query_params = query_params.to_dict()
    response = table.get_item(Key=query_params)
    return response


def add_one(table, data):
    if not isinstance(data, dict):
        data = data.to_dict()
    response = table.put_item(
        Item=data
    )
    return response


def update_one(table, id, data):
    if not isinstance(data, dict):
        data = data.to_dict()
    update_expression, expression_attribute_values = _get_update_params(
        source=data)
    response = table.update_item(
        Key={
            "id": id,
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=dict(expression_attribute_values),
        ConditionExpression='attribute_exists(id)',
        ReturnValues="UPDATED_NEW"
    )
    return response


def delete_one(table, id):
    response = table.delete_item(
        Key={
            "id": id
        },
        ConditionExpression='attribute_exists(id)'
    )
    return response

# private functions


def _get_update_params(source):
    """Given a dictionary we generate an update expression and a dict of values
    to update a dynamodb table.

    Params:
        body (dict): Parameters to use for formatting.

    Returns:
        update expression, dict of values.
    """
    update_expression = ["set "]
    update_values = dict()

    for key, val in source.items():
        update_expression.append(f" {key} = :{key},")
        update_values[f":{key}"] = val

    return "".join(update_expression)[:-1], update_values
