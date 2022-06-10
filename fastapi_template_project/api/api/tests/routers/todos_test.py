from unittest import TestCase
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from settings import settings
from routers.todos import session_scope


MODULE = "routers.todos"

API_PREFIX = settings.todos_route

client = TestClient(app)


class MainTestCase(TestCase):

    @patch(f"{MODULE}.paginate_list")
    def list_todos(self, paginate_list_mock):
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

    @patch(f"{MODULE}.Todo")
    def test_create_todo(self, model_class_mock):
        session_mock = MainTestCase.mock_session_dependency()

        todo_id = 1
        todo_name = "Feed the cat"
        model_instance_mock = MagicMock()
        model_instance_mock.id = todo_id
        model_instance_mock.name = todo_name
        model_class_mock.return_value = model_instance_mock

        todo_data = {"name": todo_name}

        response = client.post(f"{API_PREFIX}/", json=todo_data)

        model_class_mock.assert_called_once_with(**todo_data)

        session_mock.add.assert_called_once_with(model_instance_mock)
        session_mock.flush.assert_called_once()

        self.assertEqual(response.status_code, 201)

        expected_response_json = {**todo_data, **{"id": todo_id}}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.Todo")
    @patch(f"{MODULE}.read")
    def test_read_todo(self, read_mock, model_class_mock):
        session_mock = MainTestCase.mock_session_dependency()

        todo_id = 1
        todo_name = "Feed the cat"

        model_mock = MagicMock()
        model_mock.id = todo_id
        model_mock.name = todo_name

        read_mock.return_value = model_mock

        response = client.get(f"{API_PREFIX}/{todo_id}")

        read_mock.assert_called_once_with(session_mock, model_class_mock, todo_id)

        self.assertEqual(response.status_code, 200)

        expected_response_json = {"id": todo_id, "name": todo_name}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.get_or_raise")
    @patch(f"{MODULE}.Todo")
    def test_update_todo_when_exists(self, model_class_mock, get_or_raise_mock):
        session_mock = MainTestCase.mock_session_dependency()

        todo_id = 1
        old_name = "Feed the cat"
        new_name = "Feed the fish"

        model_mock = MagicMock()
        model_mock.id = todo_id
        model_mock.name = old_name

        get_or_raise_mock.return_value = model_mock

        request_body = {"name": new_name}
        response = client.put(f"{API_PREFIX}/{todo_id}", json=request_body)

        get_or_raise_mock.assert_called_once_with(session_mock, model_class_mock, id=todo_id)

        session_mock.add.assert_called_once_with(model_mock)

        self.assertEqual(response.status_code, 200)

        expected_response_json = {"id": todo_id, "name": new_name}
        self.assertEqual(response.json(), expected_response_json)

    @patch(f"{MODULE}.get_or_raise")
    @patch(f"{MODULE}.Todo")
    def test_delete_todo(self, model_class_mock, get_or_raise_mock):
        session_mock = MainTestCase.mock_session_dependency()

        todo_id = 1

        model_mock = MagicMock()
        model_mock.events = []

        get_or_raise_mock.return_value = model_mock

        response = client.delete(f"{API_PREFIX}/{todo_id}")

        get_or_raise_mock.assert_called_once_with(session_mock, model_class_mock, id=todo_id)

        session_mock.delete.assert_called_once_with(model_mock)

        self.assertEqual(response.status_code, 204)

    @staticmethod
    def mock_session_dependency():
        session_mock = MagicMock()

        def session_scope_mock():
            return session_mock

        app.dependency_overrides[session_scope] = session_scope_mock

        return session_mock
