
def native(f):
    """A function decorator to mock `micropython.native`. Does nothing."""
    return f


def viper(f):
    """A function decorator to mock `micropython.viper`. Does nothing."""
    return f


def const(val):
    """A function to declare a value as constant. Does nothing."""
    return val
