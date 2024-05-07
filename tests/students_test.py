def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1
def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )
    assert response.status_code == 200
    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2
def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })
    assert response.status_code == 400
def test_post_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 'ABCD TESTPOST'
        }
    )

    assert response.status_code == 400
    assert 'data' not in response.json


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )

    assert response.status_code == 404
    assert 'data' not in response.json

def test_submit_assignment_student_2(client, h_student_2):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 4,
            'teacher_id': 2
        }
    )

    assert response.status_code == 404
    assert 'data' not in response.json


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )
    error_response = response.json
    assert response.status_code == 404
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == 'No assignment with this id was found'



def test_submit_assignment_id_5(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 5,
            'teacher_id': 2
        }
    )

    # Check if the response status code is 404 (Not Found)
    assert response.status_code == 404

    # Check if the response contains an error message indicating that no assignment was found
    response_json = response.json
    assert 'error' in response_json
    assert response_json['error'] == 'FyleError'
    assert 'message' in response_json
    assert 'No assignment with this id was found' in response_json['message']
