from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core import db
from core.libs import helpers, assertions
from .schema import AssignmentSchema, AssignmentGradeSchema
from flask import Blueprint  # Import Blueprint class


teacher_assignments_resources = Blueprint(
    'teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )


