from flask_restx import Api

api = Api(
    title="Organizer API",
    version="1.0",
    description="Task Organizer REST API",
    doc="/swagger.html"
)