import pytest

from container import Container


def test_container():
    """Test that calling abstract methods of the abstract class Container raise NotImplementedError.
    """
    c = Container()
    with pytest.raises(NotImplementedError):
        c.add('foo')
    with pytest.raises(NotImplementedError):
        c.remove()
    with pytest.raises(NotImplementedError):
        c.is_empty()
