import json
import jwt
from functools import wraps
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, Unauthorized

# We will need these use cases for our handlers
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.login_user import LoginUserUseCase, JWT_SECRET
from src.application.use_cases.get_user_profile import GetUserProfileUseCase
from src.application.use_cases.update_password import UpdatePasswordUseCase
from src.application.use_cases.delete_user import DeleteUserUseCase

def login_required(f):
    """Decorator to protect endpoints that require authentication."""
    @wraps(f)
    def decorated_function(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise Unauthorized()

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user_id = payload['sub']
        except jwt.ExpiredSignatureError:
            return Response(json.dumps({'error': 'Token has expired'}), status=401, mimetype='application/json')
        except jwt.InvalidTokenError:
            return Response(json.dumps({'error': 'Invalid token'}), status=401, mimetype='application/json')

        return f(self, request, *args, **kwargs)
    return decorated_function

class Application:
    def __init__(self, use_case_factory):
        self.use_case_factory = use_case_factory
        self.url_map = Map([
            Rule('/register', endpoint='register', methods=['POST']),
            Rule('/login', endpoint='login', methods=['POST']),
            Rule('/profile', endpoint='profile_get', methods=['GET']),
            Rule('/profile/password', endpoint='profile_password', methods=['PUT']),
            Rule('/profile', endpoint='profile_delete', methods=['DELETE']),
        ])

    @login_required
    def on_profile_get(self, request: Request) -> Response:
        try:
            get_profile_case = self.use_case_factory(GetUserProfileUseCase)
            user = get_profile_case.execute(request.user_id)
            response_data = {"id": user.id, "username": user.username, "email": user.email}
            return Response(json.dumps(response_data), status=200, mimetype='application/json')
        except ValueError as e:
            return Response(json.dumps({"error": str(e)}), status=404, mimetype='application/json')

    def on_register(self, request: Request) -> Response:
        try:
            data = request.get_json()
            username = data['username']
            email = data['email']
            password = data['password']
        except Exception:
            return Response(json.dumps({"error": "Invalid JSON or missing fields"}), status=400, mimetype='application/json')

        try:
            register_use_case = self.use_case_factory(RegisterUserUseCase)
            user = register_use_case.execute(username, email, password)
            response_data = {"id": user.id, "username": user.username, "email": user.email}
            return Response(json.dumps(response_data), status=201, mimetype='application/json')
        except ValueError as e:
            return Response(json.dumps({"error": str(e)}), status=400, mimetype='application/json')

    @login_required
    def on_profile_password(self, request: Request) -> Response:
        try:
            data = request.get_json()
            new_password = data['new_password']
        except Exception:
            return Response(json.dumps({"error": "Invalid JSON or missing 'new_password' field"}), status=400, mimetype='application/json')

        try:
            update_password_case = self.use_case_factory(UpdatePasswordUseCase)
            update_password_case.execute(request.user_id, new_password)
            return Response(json.dumps({"message": "Password updated successfully"}), status=200, mimetype='application/json')
        except ValueError as e:
            return Response(json.dumps({"error": str(e)}), status=404, mimetype='application/json')

    @login_required
    def on_profile_delete(self, request: Request) -> Response:
        try:
            delete_user_case = self.use_case_factory(DeleteUserUseCase)
            delete_user_case.execute(request.user_id)
            return Response(status=204) # No Content
        except ValueError as e:
            return Response(json.dumps({"error": str(e)}), status=404, mimetype='application/json')

    def on_login(self, request: Request) -> Response:
        try:
            data = request.get_json()
            email = data['email']
            password = data['password']
        except Exception:
            return Response(json.dumps({"error": "Invalid JSON or missing fields"}), status=400, mimetype='application/json')

        try:
            login_use_case = self.use_case_factory(LoginUserUseCase)
            token = login_use_case.execute(email, password)
            return Response(json.dumps({"token": token}), status=200, mimetype='application/json')
        except ValueError as e:
            return Response(json.dumps({"error": str(e)}), status=401, mimetype='application/json')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(self, f'on_{endpoint}')
            return handler(request, **values)
        except NotFound:
            return Response("Not Found", status=404)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

# The main factory for creating use cases will be passed here in main.py
def create_app(use_case_factory):
    return Application(use_case_factory)
