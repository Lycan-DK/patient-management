import boto3


class DynamoDBInit:
    """
    This class is sued for creating dynamo DB instace that can be used at multiple places.
    """

    def __init__(self, config):
        self.config = config
        self.table_name = self.config.get("table_name", None)
        self.endpoint_url = self.config.get("endpoint_url", None)
        client = boto3.resource("dynamodb")
        if self.endpoint_url:
            client = boto3.resource("dynamodb", endpoint_url=self.endpoint_url)
        self.table = client.Table(self.table_name)
