import json
from core.models.assignments import Assignment, GradeEnum, AssignmentStateEnum
from unittest.mock import patch  # Import patch from unittest.mock module
from unittest.mock import Mock




def test_grade_assignment_draft_assignment_principal(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 404

def test_grade_assignment_principal(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 404

    # Check if 'data' key is present in the response
    assert 'data' not in response.json

    # Check the error message and type
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == 'No assignment with this id was found'




def test_regrade_assignment_principal(client, h_principal):
    response = client.post(
        '/principal/assignments/regrade',
        headers=h_principal,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 404

    # Update assertions based on the actual response structure
    assert 'data' not in response.json
    assert 'error' in response.json
    assert 'message' in response.json



def test_grade_nonexistent_assignment_principal(client, h_principal):
    """
    Test attempting to grade a nonexistent assignment.
    """
    non_existent_assignment_id = 999999  # Assume this ID does not exist
    grade_response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            'id': non_existent_assignment_id,
            'grade': 'B'
        }
    )
    assert grade_response.status_code == 404
    data = grade_response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_invalid_grade_principal(client, h_principal):
    """
    Test grading an assignment with an invalid grade.
    """

    # Attempt to grade the assignment with an invalid grade
    invalid_grade_response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            'id': 4,
            'grade': 'Z'  # Assume 'Z' is an invalid grade
        }
    )
    assert invalid_grade_response.status_code == 400
    error_response = invalid_grade_response.json

    assert error_response['error'] == 'ValidationError'


# Add teacher grading tests


def test_grade_assignment_cross_teacher(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "B"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'



def test_grade_assignment_bad_grade_teacher(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "CD"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment_teacher(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "B"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment_teacher(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1, json={
            "id": 2,
            "grade": "B"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_by_teacher(monkeypatch):
    assignment_id = 1  # Provide a valid assignment ID
    grade = GradeEnum.A  # Provide a valid grade
    teacher_id = 1  # Provide a valid teacher ID

    # Mock the query method and return value using monkeypatch.setattr
    def mock_query(*args, **kwargs):
        return Mock(filter=Mock(return_value=Mock(first=Mock(return_value=Assignment(id=assignment_id, content="Sample content", state=AssignmentStateEnum.SUBMITTED)))))
    monkeypatch.setattr('core.models.assignments.db.session', Mock(query=mock_query))
