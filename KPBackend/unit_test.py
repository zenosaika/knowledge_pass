from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_with_query():
    # Mock SibylSystem.inference to return a known result
    class MockSibylSystem:
        def inference(q):
            return {
                "data": [["skill1", "course1"], ["skill2", "course2"]],
                "required_skills": ["skill1", "skill2"],
            }
        def compile_graph():
            return None
        def get_graph_info():
            return 1,1,1
        def get_all_job():
            return ["job1","job2"]

    import main
    main.SibylSystem = MockSibylSystem

    response = client.get("/search?q=test_job")
    assert response.status_code == 200
    data = response.json()
    assert "html" in data
    assert "sankey_data" in data
    assert len(data['sankey_data']) > 0
    assert "course1" in data['html'][0]
    assert "course2" in data['html'][0]
    return True # Test passed

def test_search_without_query():
    response = client.get("/search")
    assert response.status_code == 200
    assert response.json() == {"message": "No query provided"}
    return True # Test passed

def test_compile_graph():
    class MockSibylSystem:
        def inference(q):
            return {
                "data": [["skill1", "course1"], ["skill2", "course2"]],
                "required_skills": ["skill1", "skill2"],
            }
        def compile_graph():
            return None
        def get_graph_info():
            return 1,1,1
        def get_all_job():
            return ["job1","job2"]

    import main
    main.SibylSystem = MockSibylSystem

    response = client.get("/compile_graph")
    assert response.status_code == 200
    assert response.json() == {"status": 200}
    return True # Test passed

def test_get_graph_info():
    class MockSibylSystem:
        def inference(q):
            return {
                "data": [["skill1", "course1"], ["skill2", "course2"]],
                "required_skills": ["skill1", "skill2"],
            }
        def compile_graph():
            return None
        def get_graph_info():
            return 1, 2, 3
        def get_all_job():
            return ["job1","job2"]

    import main
    main.SibylSystem = MockSibylSystem

    response = client.get("/get_graph_info")
    assert response.status_code == 200
    assert response.json() == {"n_job": 1, "n_course": 2, "n_skill": 3}
    return True # Test passed

def test_get_all_job():
    class MockSibylSystem:
        def inference(q):
            return {
                "data": [["skill1", "course1"], ["skill2", "course2"]],
                "required_skills": ["skill1", "skill2"],
            }
        def compile_graph():
            return None
        def get_graph_info():
            return 1, 2, 3
        def get_all_job():
            return ["job1", "job2", "job3"]

    import main
    main.SibylSystem = MockSibylSystem
    response = client.get("/get_all_job")
    assert response.status_code == 200
    assert response.json() == ["job1", "job2", "job3"]
    return True # Test passed

tests = [
    ("search with query", test_search_with_query),
    ("search without query", test_search_without_query),
    ("compile graph", test_compile_graph),
    ("get graph info", test_get_graph_info),
    ("get all job", test_get_all_job),
]

passed_count = 0
total_count = len(tests)

for name, test_func in tests:
    print(f"\n[UNIT TEST]: {name.title()}")
    try:
        if test_func():
            print("✅ PASSED")
            passed_count += 1
    except AssertionError:
        print("❌ FAILED")

percentage_passed = (passed_count / total_count) * 100
print(f"\nTest Results: {passed_count}/{total_count} tests passed ({percentage_passed:.2f}%)")