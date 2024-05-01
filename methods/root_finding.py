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
        '''
        '''

        middle_vals = [0]
        error = self.tolerance + 10e-5

        while error > self.tolerance:
            
            middle_value = (self.interval[0] + self.interval[1])/2 # Compute the middle value
            f_middle_value = self.function(middle_value)
            
            # If middle value is equal to 0, the work is donde!
            if (f_middle_value == 0):
                self.root = middle_value # Setting as root value

            elif self.function(self.interval[0]) * f_middle_value > 0:
                self.interval[0] = middle_value
                
            else: 
                self.interval[1] = middle_value

            self.steps += 1
            
            middle_vals.append(middle_value)
            error = errors.absolute(middle_vals[-2], middle_vals[-1])

            # Adding to history as a new row
            self.add_summary(self.steps,
                             middle_value,
                             error,
                             errors.relative(middle_vals[-2], middle_vals[-1])
                             )

        self.root = middle_value
        self.make_summary() 

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
        '''
        '''

        # Setting the initial error
        error = self.tolerance + 10e-5
        
        # Computting initial points valued in self.function
        function_eval_p0 = self.function(self.points[0])
        function_eval_p1 = self.function(self.points[1])

        # Iterating until the error had been lower to tolerance
        while error > self.tolerance:

            # In case of the denominator be equal to zero
            if function_eval_p0==function_eval_p1:
                raise ZeroDivisionError('You can not divide by zero!')

            # Computing the fractional
            numerator = self.points[0]*function_eval_p1 - self.points[1]*function_eval_p0
            denominator = function_eval_p1 - function_eval_p0

            new_point = numerator / denominator # Compute new point (x_{i+1})
            new_point_evaluated = self.function(new_point)

            # Updating points
            self.points[0], self.points[1] = self.points[1], new_point
            function_eval_p0, function_eval_p1 = function_eval_p1, new_point_evaluated

            # Update references
            self.steps += 1
            self.root = new_point
            error = errors.absolute(self.points[0], self.points[1])

            # Adding to history as a new row
            self.add_summary(self.steps,
                             new_point,
                             error,
                             errors.relative(self.points[0], self.points[1])
                             )

        self.make_summary()


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
        
        aprox_ = [0, self.point] # Copy initial point for not mutate it
        error = errors.absolute(aprox_[-2], aprox_[-1])

        while error > self.tolerance:
            
            # Adding to history as a new row
            self.add_summary(self.steps,
                             self.root,
                             error,
                             errors.relative(aprox_[-2], aprox_[-1])
                             )


            frac = self.function(aprox_[-2])/self.derivative(aprox_[-2])
            aprox_.append(aprox_[-2] - frac)
            self.steps += 1

            error = errors.absolute(aprox_[-2], aprox_[-1])

            self.root = aprox_[-1] # Set last point as root
            
        self.make_summary()

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
        
        aprox_ = [0, self.point] # Copy initial point for not mutate it
        error = errors.absolute(aprox_[-2], aprox_[-1]) # initial error abs

        while error > self.tolerance:

            # Adding to history as a new row
            self.add_summary(self.steps,
                             self.root,
                             error,
                             errors.relative(aprox_[-2], aprox_[-1])
                            )


            value_x = self.function(aprox_[-1])
            aprox_.append(value_x)

            error = errors.absolute(aprox_[-2], aprox_[-1])
            self.steps += 1

            self.root = aprox_[-1]

        self.make_summary()

