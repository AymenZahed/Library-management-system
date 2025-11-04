# test_basic.py - TESTS TRÈS SIMPLES
def test_always_passes():
    """Test qui passe toujours"""
    assert True

def test_basic_math():
    """Test mathématique basique"""
    assert 2 + 2 == 4

def test_string_operations():
    """Test sur les strings"""
    assert "hello".upper() == "HELLO"
    assert " world".strip() == "world"

def test_list_operations():
    """Test sur les listes"""
    numbers = [1, 2, 3]
    assert len(numbers) == 3
    assert sum(numbers) == 100