from unittest import TestCase
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from settings import settings
from routers.people import session_scope


MODULE = "routers.people"

API_PREFIX = settings.people_route

client = TestClient(app)


class MainTestCase(TestCase):

    @patch(f"{MODULE}.paginate_list")
    def test_list_people(self, paginate_list_mock):
        paginated_list_mock = {
            "total_count": 0,
            "count": 0,
            "limit": 10,
            "offset": 0,
            "results": []
        }
        paginate_list_mock.return_value = paginated_list_mock

        response = client.get(API_PREFIX)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), paginated_list_mock)

    @patch(f"{MODULE}.Person")
    @patch(f"{MODULE}.exists")
    def test_create_person_when_does_not_exist_already(self, exists_mock, orm_person_model_mock):
        session_mock = MainTestCase.mock_session_dependency()

        exists_mock.return_value = False

        person_id = 1
        person_name = "Someone"
        orm_person_model_instance_mock = MagicMock()
        orm_person_model_instance_mock.id = person_id
        orm_person_model_instance_mock.name = person_name
        orm_person_model_mock.return_value = orm_person_model_instance_mock

        person_data = {"name": person_name}

        response = client.post(f"{API_PREFIX}/", json=person_data)

        exists_mock.assert_called_once_with(session_mock, orm_person_model_mock, **person_data)

        orm_person_model_mock.assert_called_once_with(**person_data)

        session_mock.add.assert_called_once_with(orm_person_model_instance_mock)
        session_mock.flush.assert_called_once()

        self.assertEqual(response.status_code, 201)

        expected_response_json = {**person_data, **{"id": person_id}}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.Person")
    @patch(f"{MODULE}.exists")
    def test_create_person_when_already_exists(self, exists_mock, orm_person_model_mock):
        session_mock = MainTestCase.mock_session_dependency()

        exists_mock.return_value = True

        person_name = "Someone"
        person_data = {"name": person_name}

        response = client.post(f"{API_PREFIX}/", json=person_data)

        exists_mock.assert_called_once_with(session_mock, orm_person_model_mock, **person_data)

        self.assertEqual(response.status_code, 409)

        expected_response_json = {"detail": "The person already exists"}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.Person")
    @patch(f"{MODULE}.read")
    def test_read_person(self, read_mock, orm_person_model_mock):
        session_mock = MainTestCase.mock_session_dependency()

        person_id = 1
        person_name = "Someone"

        person_mock = MagicMock()
        person_mock.id = person_id
        person_mock.name = person_name

        read_mock.return_value = person_mock

        response = client.get(f"{API_PREFIX}/{person_id}")

        read_mock.assert_called_once_with(session_mock, orm_person_model_mock, person_id)

        self.assertEqual(response.status_code, 200)

        expected_response_json = {"id": person_id, "name": person_name}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.Person")
    def test_update_person_when_exists(self, orm_person_model_mock):
        session_mock = MainTestCase.mock_session_dependency()

        person_id = 1
        person_old_name = "Someone"
        person_new_name = "Someone else"

        orm_person_instance_mock = MagicMock()
        orm_person_instance_mock.id = person_id
        orm_person_instance_mock.name = person_old_name

        session_mock.query.return_value = session_mock
        session_mock.get.return_value = orm_person_instance_mock

        request_body = {"name": person_new_name}
        response = client.put(f"{API_PREFIX}/{person_id}", json=request_body)

        session_mock.query.assert_called_once_with(orm_person_model_mock)
        session_mock.get.assert_called_once_with(person_id)

        session_mock.add.assert_called_once_with(orm_person_instance_mock)

        self.assertEqual(response.status_code, 200)

        expected_response_json = {"id": person_id, "name": person_new_name}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.Person")
    def test_update_person_when_does_not_exist(self, orm_person_model_mock):
        session_mock = MainTestCase.mock_session_dependency()

        person_id = 1
        person_new_name = "Someone else"

        orm_person_instance_mock = None

        session_mock.query.return_value = session_mock
        session_mock.get.return_value = orm_person_instance_mock

        request_body = {"name": person_new_name}
        response = client.put(f"{API_PREFIX}/{person_id}", json=request_body)

        session_mock.query.assert_called_once_with(orm_person_model_mock)
        session_mock.get.assert_called_once_with(person_id)

        self.assertEqual(response.status_code, 404)

        expected_response_json = {"detail": "Not Found"}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.Person")
    def test_delete_person_when_exists_and_has_no_events(self, orm_person_model_mock):
        session_mock = MainTestCase.mock_session_dependency()

        person_id = 1

        orm_person_instance_mock = MagicMock()
        orm_person_instance_mock.events = []

        session_mock.query.return_value = session_mock
        session_mock.get.return_value = orm_person_instance_mock

        response = client.delete(f"{API_PREFIX}/{person_id}")

        session_mock.query.assert_called_once_with(orm_person_model_mock)
        session_mock.get.assert_called_once_with(person_id)

        session_mock.delete.assert_called_once_with(orm_person_instance_mock)

        self.assertEqual(response.status_code, 204)

    @patch(f"{MODULE}.Person")
    def test_delete_person_when_does_not_exist(self, orm_person_model_mock):
        session_mock = MainTestCase.mock_session_dependency()

        person_id = 1

        orm_person_instance_mock = None
        session_mock.query.return_value = session_mock
        session_mock.get.return_value = orm_person_instance_mock

        response = client.delete(f"{API_PREFIX}/{person_id}")

        session_mock.query.assert_called_once_with(orm_person_model_mock)
        session_mock.get.assert_called_once_with(person_id)

        self.assertEqual(response.status_code, 404)

        expected_response_json = {"detail": "Not Found"}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.Person")
    def test_delete_person_when_has_events(self, orm_person_model_mock):
        session_mock = MainTestCase.mock_session_dependency()

        person_id = 1

        orm_person_instance_mock = MagicMock()
        orm_person_instance_mock.events = [MagicMock()]

        session_mock.query.return_value = session_mock
        session_mock.get.return_value = orm_person_instance_mock

        response = client.delete(f"{API_PREFIX}/{person_id}")

        session_mock.query.assert_called_once_with(orm_person_model_mock)
        session_mock.get.assert_called_once_with(person_id)

        self.assertEqual(response.status_code, 409)

        expected_response_json = {"detail": "The person is related to events"}
        self.assertEqual(response.json(), expected_response_json)

    @staticmethod
    def mock_session_dependency():
        session_mock = MagicMock()

        def session_scope_mock():
            return session_mock

        app.dependency_overrides[session_scope] = session_scope_mock

        return session_mock
