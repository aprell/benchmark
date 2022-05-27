from src.utils import read_list


def test_read_list():
    assert read_list([]) == []
    assert read_list("") == [""]
    assert read_list("1") == ["1"]
    assert read_list("1 , 2 , 3") == ["1", "2", "3"]
    assert read_list("1 | 2 | 3", sep="|", elem=int) == [1, 2, 3]
