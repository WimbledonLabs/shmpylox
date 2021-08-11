import lox

def test_global_error():
    lox1 = lox.Lox()
    lox2 = lox.Lox()

    # Check we can set the value, and that it's shared between instances
    lox1.had_error = True
    assert lox1.had_error == lox2.had_error == True

    # Check that we can set it back with the other instance
    lox2.had_error = False
    assert lox1.had_error == lox2.had_error == False

    # Check that we can set the value through the class directory
    lox.Lox.had_error = True
    assert lox1.had_error == lox2.had_error == True


def test_class_error():
    # Check that we can produce an error through the class
    lox.Lox.error(14, "test")

    # Check that it set the global error flag
    assert lox.Lox.had_error == True


