from pycommerce.infra.providers.crypto import Hasher


def test_if_hashes_value():
    value = "testing"
    assert value != Hasher.hash(value)


def test_if_returns_true_when_checking_hashed_value():
    value = "testing"
    hashed = Hasher.hash(value)
    assert Hasher.check(value, hashed)


def test_if_returns_false_when_hashed_value_is_different():
    value = "testing"
    hashed = Hasher.hash("different")
    assert not Hasher.check(value, hashed)
