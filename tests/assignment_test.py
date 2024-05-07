import pytest
from unittest.mock import patch, MagicMock
from core import db

from core.models.assignments import Assignment, GradeEnum, AssignmentStateEnum
from core.models.teachers import Teacher
from core.models.students import Student
from core.apis.decorators import AuthPrincipal

@pytest.fixture
def sample_assignment():
    return Assignment(student_id=1, content="Sample content")

def test_upsert_existing_assignment(sample_assignment):
    with patch('core.models.assignments.db.session') as mock_session:
        mock_session.query().filter().first.return_value = sample_assignment

        Assignment.upsert(sample_assignment)

        # Update the content of the assignment
        sample_assignment.content = "Updated content"
        updated_assignment = Assignment.upsert(sample_assignment)

        assert updated_assignment.content == "Updated content"

def test_upsert_new_assignment(sample_assignment):
    with patch('core.models.assignments.db.session') as mock_session:
        mock_session.query().filter().first.return_value = None

        added_assignment = Assignment.upsert(sample_assignment)

        assert added_assignment.content == "Sample content"

def test_submit_draft_assignment(sample_assignment):
    sample_assignment.state = AssignmentStateEnum.DRAFT
    with patch('core.models.assignments.db.session') as mock_session:
        mock_session.query().filter().first.return_value = sample_assignment

        submitted_assignment = Assignment.submit(sample_assignment.id, 1, AuthPrincipal(student_id=1, user_id=123))

        assert submitted_assignment.state == AssignmentStateEnum.SUBMITTED

