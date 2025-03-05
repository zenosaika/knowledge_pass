from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_with_query():
    response = client.get("/search?q=Full%20Stack%20JavaScript")
    assert response.status_code == 200
    data = response.json()
    assert "html" in data
    assert "sankey_data" in data
    assert len(data['sankey_data']) > 0
    return True # Test passed

def test_search_without_query():
    response = client.get("/search")
    assert response.status_code == 200
    assert response.json() == {"message": "No query provided"}
    return True # Test passed

def test_compile_graph():
    response = client.get("/compile_graph")
    assert response.status_code == 200
    return True # Test passed

def test_get_graph_info():
    response = client.get("/get_graph_info")
    assert response.status_code == 200
    obj = response.json()
    assert 'n_job' in obj
    assert 'n_course' in obj
    assert 'n_skill' in obj
    return True # Test passed

def test_get_all_job():
    response = client.get("/get_all_job")
    assert response.status_code == 200
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
    print(f"\n[INTEGRATION TEST]: {name.title()}")
    try:
        if test_func():
            print("✅ PASSED")
            passed_count += 1
    except AssertionError:
        print("❌ FAILED")

percentage_passed = (passed_count / total_count) * 100
print(f"\nTest Results: {passed_count}/{total_count} tests passed ({percentage_passed:.2f}%)")