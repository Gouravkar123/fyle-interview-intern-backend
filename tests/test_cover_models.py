import pytest
from core.models.students import Student
from core.models.teachers import Teacher
from core.models.assignments import Assignment, AssignmentStateEnum, assertions


def test_student_repr():
    # Create a student instance for testing
    student = Student(id=1)

    # Check the representation string
    repr_string = repr(student)

    # Assert that the representation string contains the expected format
    assert repr_string.startswith('<Student 1')

def test_teacher_repr():
    # Create a teacher instance for testing
    teacher = Teacher(id=1)

    # Check the representation string
    repr_string = repr(teacher)

    # Assert that the representation string contains the expected format
    assert repr_string.startswith('<Teacher 1')

@pytest.fixture
def sample_assignment():
    # Create a sample assignment for testing
    return Assignment(student_id=1, content='Sample Content')

def test_assignment_repr(sample_assignment):
    # Check the __repr__ method of the Assignment class
    repr_string = repr(sample_assignment)
    assert repr_string.startswith('<Assignment ')

def test_upsert_existing_assignment_with_id_check(monkeypatch):
    # Mocked function that raises AssertionError
    def mock_assert_valid(condition, error_message):
        raise AssertionError(error_message)

    # Replace the actual assert_valid function with the mocked one
    monkeypatch.setattr(assertions, 'assert_valid', mock_assert_valid)

# Assuming you have a function to fetch an assignment by ID from the database
def get_assignment_by_id(assignment_id):
    return Assignment.query.filter_by(id=assignment_id).first()

# Get the existing assignment with ID 1 from the database
existing_assignment = get_assignment_by_id(1)

# If the assignment doesn't exist, you can create a new one
if not existing_assignment:
    existing_assignment = Assignment(student_id=3, content='Existing Assignment Content', id=1)
