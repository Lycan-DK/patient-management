import unittest
import boto3
import os
from adapters.dynamodb.dyanmo_db_init import DynamoDBInit
from services.patient_management_service import add_patient, update_patient, delete_patient, search_patient, get_all_patient


class TestPatient(unittest.TestCase):
    def setUp(self):
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
        dynamodb = boto3.resource(
            'dynamodb', endpoint_url="http://localhost:8000")
        table = dynamodb.create_table(
            TableName='unittest_patient_table',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        self.table = DynamoDBInit(config={
                                  "table_name": "unittest_patient_table", "endpoint_url": "http://localhost:8000"}).table
    def tearDown(self):
        self.table.delete()

    def test_create_patient(self):
        payload = {
            "first_name": "Admin",
            "last_name": "Super",
            "age": "21",
            "gender": "Male",
            "state": "NA",
            "country": "NA",
            "email": "unittest_testing@nodomianavailable1231.com",
        }
        response = add_patient(table=self.table, source=payload)
        self.assertEqual(response.get("status"), 200)

    def test_update_patient(self):
        """
        test case is completed in 2 steps
        1. create a sample patient and get id
        2. update patient data with matching patient_id
        :return:
        """
        # create patient and get patient_id
        patient_id = self._create_patient_and_get_id()

        # update patient with fields in update_fields of patient_id
        update_fields = {
            "first_name": "Admin1",
            "last_name": "Super1",
            "id": patient_id
        }
        update_patient_response = update_patient(table=self.table, source=update_fields)
        self.assertEqual(update_patient_response.get("status"), 200)

    def test_delete_patient(self):
        """
        test case is completed in 2 steps
        1. create a sample patient and get id
        2. delete patient with matching patient_id
        :return:
        """
        # Create patient and get id
        patient_id = self._create_patient_and_get_id()

        # Delete patient with patient_id
        source = {
            "id": patient_id
        }
        deleted_patient_response = delete_patient(table=self.table, source=source)
        self.assertEqual(deleted_patient_response.get("status"), 200)

    def test_get_one_patient(self):
        """
        test case is completed in 2 steps
        1. create a sample patient and get id
        2. Get patient with matching patient_id
        :return:
        """
        # Create patient and get patient_id
        patient_id = self._create_patient_and_get_id()

        # Get patient with patient_id
        query_params = {
            "id": patient_id
        }
        search_result = search_patient(table=self.table, query_params=query_params)
        self.assertEqual(search_result.get("Item").get("id"), patient_id)

    def test_get_all_patients(self):
        """
        test case is completed in 2 steps
        1. create a sample patient and get id
        2. Get patient with matching patient_id
        :return:
        """
        # Create 2 patients
        self._create_patient_and_get_id()
        self._create_patient_and_get_id()

        # Get list of patient
        list_of_patients = get_all_patient(table=self.table)
        self.assertGreater(len(list_of_patients), 0)

    def _create_patient_and_get_id(self):
        # create patient
        payload = {
            "first_name": "Admin2",
            "last_name": "Super2",
            "age": "22",
            "gender": "Male",
            "state": "NA",
            "country": "NA",
            "email": "unittest_testing@nodomianavailable1231.com",
        }
        created_patient = add_patient(table=self.table, source=payload)

        # get patient id from message
        message = created_patient.get("message")
        split = message.split('id :')
        id = split[1]
        return id