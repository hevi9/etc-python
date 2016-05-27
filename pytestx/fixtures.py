"""

"""

import  pytest

@pytest.fixture(scope="session")
def fix_session(request):
    print("fixture","session","make")
    def fin():
        print("fixture", "session", "fin")
    request.addfinalizer(fin)
    return "session"

@pytest.fixture(scope="module")
def fix_module(request):
    print("fixture","module","make")
    def fin():
        print("fixture", "module", "fin")
    request.addfinalizer(fin)
    return "module"

@pytest.fixture
def fix_function(request):
    print("fixture","function","make")
    def fin():
        print("fixture", "function", "fin")
    request.addfinalizer(fin)
    return "function"


def test_case_a(fix_session, fix_module, fix_function):
    print("test_case_a")

def test_case_b(fix_session, fix_function):
    print("test_case_b")


def test_case_c(fix_function):
    print("test_case_c")