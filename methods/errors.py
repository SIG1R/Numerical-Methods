class Errors:

    def relative(approximate, real):
        '''
        Compute the relative error associated to
        an approximated value.
        '''

        return abs(approximate - real) / abs(real) * 100

