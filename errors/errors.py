def absolute(approximate, real):
    '''
    Compute the relative error associated to
    an approximated error.
    '''

    error = abs(approximate - real)

    return round(error, 3)

def relative(approximate, real):
    '''
    Compute the relative error associated to
    an approximated error.
    '''

    error = absolute(approximate, real) / abs(real) * 100

    return round(error, 3)

