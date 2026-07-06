from datetime import date

from flask_restx import Namespace
from flask_restx import Resource
from flask_restx import fields
from flask_restx import marshal

from app.database import SessionLocal

from app.repositories.user_repository import UserRepository
from app.repositories.task_repository import TaskRepository

from app.services.task_service import TaskService

tasks_ns = Namespace(
    "tasks",
    description="Task operations"
)

# =========================
# REQUEST MODELS
# =========================

task_create_model = tasks_ns.model(
    "TaskCreateRequest",
    {
        "user_id": fields.Integer(
            required=True,
            description="User identifier"
        ),
        "task": fields.String(
            required=True,
            description="Task description"
        ),
        "datum": fields.String(
            required=True,
            description="Due date (YYYY-MM-DD)"
        )
    }
)

task_update_model = tasks_ns.model(
    "TaskUpdateRequest",
    {
        "task": fields.String(
            required=True
        ),
        "datum": fields.String(
            required=True
        ),
        "done": fields.Boolean(
            required=True
        )
    }
)

# =========================
# RESPONSE MODELS
# =========================

task_response_model = tasks_ns.model(
    "TaskResponse",
    {
        "id": fields.Integer(),
        "datum": fields.String(),
        "task": fields.String(),
        "done": fields.Boolean()
    }
)

task_created_response_model = tasks_ns.model(
    "TaskCreatedResponse",
    {
        "id": fields.Integer()
    }
)

task_deleted_response_model = tasks_ns.model(
    "TaskDeletedResponse",
    {
        "message": fields.String()
    }
)

error_response_model = tasks_ns.model(
    "ErrorResponse",
    {
        "error": fields.String()
    }
)

# =========================
# CREATE TASK
# =========================

@tasks_ns.route("")
class TaskCollection(Resource):

    @tasks_ns.expect(task_create_model)

    @tasks_ns.response(
        201,
        "Task created"
    )

    @tasks_ns.response(
        400,
        "Invalid request",
        error_response_model
    )
    def post(self):

        session = SessionLocal()

        try:

            data = tasks_ns.payload

            service = TaskService(
                TaskRepository(session),
                UserRepository(session)
            )

            task = service.create_task(
                data["user_id"],
                data["task"],
                date.fromisoformat(
                    data["datum"]
                )
            )

            return marshal({
                "id": task.id
            }, task_created_response_model), 201

        except ValueError as ex:

            return {
                "error": str(ex)
            }, 400

        finally:
            session.close()

# =========================
# GET USER TASKS
# =========================

@tasks_ns.route("/user/<int:user_id>")
class UserTasksResource(Resource):

    @tasks_ns.marshal_list_with(
        task_response_model
    )
    def get(self, user_id):

        session = SessionLocal()

        try:

            service = TaskService(
                TaskRepository(session),
                UserRepository(session)
            )

            tasks = service.get_tasks_by_user(
                user_id
            )

            result = []

            for task in tasks:

                result.append({
                    "id": task.id,
                    "datum": str(task.datum),
                    "task": task.task,
                    "done": task.done
                })

            return result

        finally:
            session.close()

# =========================
# GET USER TASKS BY DATE
# =========================

@tasks_ns.route("/user/<int:user_id>/<string:task_date>")
class UserTasksByDateResource(Resource):

    @tasks_ns.marshal_list_with(
        task_response_model
    )
    def get(self, user_id, task_date):

        session = SessionLocal()

        try:

            service = TaskService(
                TaskRepository(session),
                UserRepository(session)
            )

            tasks = service.get_tasks_by_date(
                user_id,
                date.fromisoformat(task_date)
            )

            result = []

            for task in tasks:

                result.append({
                    "id": task.id,
                    "datum": str(task.datum),
                    "task": task.task,
                    "done": task.done
                })

            return result

        finally:
            session.close()

# =========================
# UPDATE / DELETE TASK
# =========================

@tasks_ns.route("/<int:task_id>")
class TaskResource(Resource):

    @tasks_ns.expect(task_update_model)

    @tasks_ns.response(
        400,
        "Task not found",
        error_response_model
    )
    def put(self, task_id):

        session = SessionLocal()

        try:

            data = tasks_ns.payload

            service = TaskService(
                TaskRepository(session),
                UserRepository(session)
            )

            task = service.update_task(
                task_id,
                data["task"],
                date.fromisoformat(
                    data["datum"]
                ),
                data["done"]
            )

            return marshal({
                "id": task.id
            }, task_created_response_model)

        except ValueError as ex:

            return {
                "error": str(ex)
            }, 400

        finally:
            session.close()

    @tasks_ns.response(
        404,
        "Task not found",
        error_response_model
    )
    def delete(self, task_id):

        session = SessionLocal()

        try:

            service = TaskService(
                TaskRepository(session),
                UserRepository(session)
            )

            service.delete_task(task_id)

            return marshal({
                "message": "Task deleted."
            }, task_deleted_response_model)

        except ValueError as ex:

            return {
                "error": str(ex)
            }, 404

        finally:
            session.close()