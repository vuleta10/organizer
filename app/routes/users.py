from flask_restx import Namespace
from flask_restx import Resource
from flask_restx import fields
from flask_restx import marshal

from app.database import SessionLocal
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

users_ns = Namespace(
    "users",
    description="User operations"
)

# =========================
# REQUEST MODELS
# =========================

register_model = users_ns.model(
    "RegisterRequest",
    {
        "username": fields.String(
            required=True,
            description="Username"
        ),
        "password": fields.String(
            required=True,
            description="Password"
        )
    }
)

login_model = users_ns.model(
    "LoginRequest",
    {
        "username": fields.String(
            required=True,
            description="Username"
        ),
        "password": fields.String(
            required=True,
            description="Password"
        )
    }
)

change_password_model = users_ns.model(
    "ChangePasswordRequest",
    {
        "username": fields.String(
            required=True,
            description="Username"
        ),
        "old_password": fields.String(
            required=True,
            description="Current password"
        ),
        "new_password": fields.String(
            required=True,
            description="New password"
        )
    }
)

# =========================
# RESPONSE MODELS
# =========================

user_response_model = users_ns.model(
    "UserResponse",
    {
        "id": fields.Integer(),
        "username": fields.String()
    }
)

change_password_response_model = users_ns.model(
    "ChangePasswordResponse",
    {
        "message": fields.String(),
        "id": fields.Integer()
    }
)

error_response_model = users_ns.model(
    "ErrorResponse",
    {
        "error": fields.String()
    }
)

# =========================
# REGISTER
# =========================

@users_ns.route("/register")
class RegisterResource(Resource):

    @users_ns.expect(register_model)

    @users_ns.response(
        201,
        "User created"
    )

    @users_ns.response(
        400,
        "Username already exists",
        error_response_model
    )
    def post(self):

        session = SessionLocal()

        try:

            data = users_ns.payload

            service = UserService(
                UserRepository(session)
            )

            user = service.register(
                data["username"],
                data["password"]
            )

            return marshal({
                "id": user.id,
                "username": user.username
            }, user_response_model), 201

        except ValueError as ex:

            return {
                "error": str(ex)
            }, 400

        finally:
            session.close()

# =========================
# LOGIN
# =========================

@users_ns.route("/login")
class LoginResource(Resource):

    @users_ns.expect(login_model)

    @users_ns.response(
        200,
        "Login successful"
    )

    @users_ns.response(
        401,
        "Invalid credentials",
        error_response_model
    )
    def post(self):

        session = SessionLocal()

        try:

            data = users_ns.payload

            service = UserService(
                UserRepository(session)
            )

            user = service.login(
                data["username"],
                data["password"]
            )

            return marshal({
                "id": user.id,
                "username": user.username
            }, user_response_model)

        except ValueError as ex:

            return {
                "error": str(ex)
            }, 401

        finally:
            session.close()

# =========================
# CHANGE PASSWORD
# =========================

@users_ns.route("/change-password")
class ChangePasswordResource(Resource):

    @users_ns.expect(change_password_model)

    @users_ns.response(
        200,
        "Password changed"
    )

    @users_ns.response(
        400,
        "Invalid request",
        error_response_model
    )
    def put(self):

        session = SessionLocal()

        try:

            data = users_ns.payload

            service = UserService(
                UserRepository(session)
            )

            user = service.change_password(
                data["username"],
                data["old_password"],
                data["new_password"]
            )

            return marshal({
                "message": "Password changed.",
                "id": user.id
            }, change_password_response_model)

        except ValueError as ex:

            return {
                "error": str(ex)
            }, 400

        finally:
            session.close()