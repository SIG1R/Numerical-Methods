# Root search
# Equations
import polars as pl
import numpy as np
from errors import errors

class Base_Method:
    
    def __init__(self):
        self.steps = 0
        self.root = 0
        self.summary = {
            'Iter': [],
            'Root': [],
            'Error ABS': [],
            'Error Relative':  []
            }

    def add_summary(self, iter_, root, errorabs, errorre):

        self.summary['Iter'].append(iter_)
        self.summary['Root'].append(root)
        self.summary['Error ABS'].append(errorabs)
        self.summary['Error Relative'].append(errorre)
            

    def make_summary(self):
        self.summary = pl.DataFrame(data = self.summary,
                                    schema = {
                                        'Iter': pl.Int64,
                                        'Root': pl.Float64,
                                        'Error ABS': pl.Float64,
                                        'Error Relative': pl.Float64,
                                    })
                                    


class Bisection(Base_Method):
    '''

    '''
    
    def set_parameters(self, interval, tolerance, function):
        '''
        Initializer of Bisection class where is given the next arguments:

        - interval: they are the inteval where the function is defined
          must be defined in a 2-index list, like this [value_left, value_right].

        - tolerance: it´s the error that you want assume, in simple words
          if there are more tolerance then you root would be most nearest
          to the real number.

        - function: amm your function, ¿not?
        '''

        assert type(interval) == list, 'The interval of the function must be into a list like this: [value_left, value_right]'

        self.interval = interval
        self.tolerance = tolerance
        self.function = function
    
    def check_interval(self):
        '''
        Do you wanna check if your interval have any root?, So this method do it!
        '''

        calc = self.function(self.interval[0]) * self.function(self.interval[1])
        if calc < 0: 
            print(f'Para el intervalo [{self.interval[0]},{self.interval[1]}] existe alguna raíz C')
            return True
        else: 
            print(f'Para el intervalo [{self.interval[0]},{self.interval[1]}] no existe alguna raíz C')
            return False

    def check_tolerance(self):
        return abs(self.interval[1]-self.interval[0]) < self.tolerance

    def fit(self):
        c = (self.interval[0] + self.interval[1])/2
        fa = self.function(self.interval[0])
        fc = self.function(c)
    
        if self.function(c) == 0 or self.check_interval():
            return f'El valor raíz es {c}'
        elif fa*fc > 0:
            return self.fit(c, self.interval[1], self.function, self.tolerance)
        else: 
            return self.fit(self.interval[0], c, self.function, self.tolerance)


class Secant(Base_Method):
    '''
    '''

    def set_parameters(self, points, tolerance, function):
        '''
        Initializer of Secant class where is given the next arguments:

        - points: the points indicate the x axes points, it must be defined in a 2-index list, like this [x_1, x_2].

        - tolerance: it´s the error that you want assume, in simple words
          if there are more tolerance then you root would be most nearest
          to the real number.

        - function: amm your function, ¿not?
        '''
        
        assert type(points) == list, 'The axes points x_1 and x_2 must be into a list like this: [x_1,x_2]'

        self.points = points
        self.tolerance = tolerance
        self.function = function


    def fit(self):
        
        function_eval_p0 = self.function(self.points[0])
        function_eval_p1 = self.function(self.points[1])

        # >>> Iterating until... <<<
        while True:

            # ... until 
            if function_eval_p0==function_eval_p1:
                raise ZeroDivisionError('You can not divide by zero!')

            iter_point = (self.points[0]*function_eval_p1-self.points[1]*function_eval_p0)/(function_eval_p1-function_eval_p0)
            iter_function = self.function(iter_point)
            
            # ... until the tolerance had been exceeded
            if abs(iter_function)<self.tolerance:
                self.root = iter_point
                print(f'Root found on coordinate x={self.root}')
                break
            
            else:
                self.points[0], self.points[1], function_eval_p0, function_eval_p1 = self.points[1], iter_point,function_eval_p1, iter_function

            self.steps += 1

        return self.steps



class Newton_Raphson(Base_Method):

    def set_parameters(self, point, tolerance, function, derivative):
        '''
        Initializer of Newton_Raphson class where is given the next arguments:

        - point: they are the initial point where the function is defined

        - tolerance: it´s the error that you want assume, in simple words
          if there are more tolerance then you root would be most nearest
          to the real number.

        - function: amm your function f(x)
        
        - derivative: the derivative of your function. :)
        '''
        
        assert isinstance(point, (float, int)), 'Check data type of the point'
        assert isinstance(tolerance, (float, int)), 'Check tolerance data type'

        self.point = point
        self.tolerance = tolerance
        self.function = function
        self.derivative = derivative

    def fit(self):
        '''
        
        '''
        
        aprox_ = [999999999999, self.point] # Copy initial point for not mutate it

        while abs(aprox_[-1] - aprox_[-2]) > self.tolerance:
            frac = self.function(aprox_[-2])/self.derivative(aprox_[-2])
            aprox_.append(aprox_[-2] - frac)
            self.steps += 1

        self.root = aprox_[-1]


class Fixed_Point(Base_Method):
 
    def set_parameters(self, point, tolerance, function):
        '''
        Initializer of  Fixed_Point class where is given the next arguments:

        - point: they are the initial point where the function is defined

        - tolerance: it´s the error that you want assume, in simple words
          if there are more tolerance then you root would be most nearest
          to the real number.

        - function: Very important! this argument is your function in the
        form x = g(x), obviously this parameter is g(x).
        '''
        
        assert isinstance(point, (float, int)), 'Check the point data type'
        assert isinstance(tolerance, (float, int)), 'Check tolerance data type'

        self.point = point
        self.tolerance = tolerance
        self.function = function

    def fit(self):
        '''
        
        '''
        
        aprox_ = [np.inf, self.point] # Copy initial point for not mutate it
        error = errors.absolute(aprox_[-2], aprox_[-1]) # initial error abs

        while error > self.tolerance:

            self.add_summary(self.steps, self.root, error, errors.relative(aprox_[-2], aprox_[-1])
)


            value_x = self.function(aprox_[-1])
            aprox_.append(value_x)

            error = errors.absolute(aprox_[-2], aprox_[-1])
            self.steps += 1

            self.root = aprox_[-1]

        self.make_summary()

