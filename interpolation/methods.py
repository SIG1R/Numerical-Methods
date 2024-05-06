
class Lagrange:
    def compute(coordinates: list, eval_point):
        '''
        Compute the Lagrange polynomial and returns the value of the fuction
        evaluated in eval_point.

        Arguments:
        - coordinates: this are the coordinates in R², this structure is
                    a list with the coordinates in tuples, for example
                    [(-2,-2),(-1,-1),(0,0),(1,1),(2,2)]

        - eval_point: is the point of eval in the equation of Lagrange
                    polynomial, this can be a point (float) or a
                    array of points to eval, correspond to axis X
                    in the plane R².
        '''


        summation = 0 # Initial term of the summatory


        for i in range(len(coordinates)): # 

            productory = 1 # Initial term of the productory
            
            for j in range(len(coordinates)):
                if i!=j:
                    productory *= (eval_point-coordinates[j][0])/(coordinates[i][0]-coordinates[j][0])

            summation += productory*coordinates[i][1] # Adding term i to the summation
        
        return summation

class Newton:
    
    def slope(initial_point: tuple, final_point: tuple):
        '''
        This fucntion assume that each point have the structure (x,f(x))
        and return the slope.
        '''
        
        print(f'\t({final_point[1]} - {initial_point[1]})/({final_point[0]} - {initial_point[0]})')

        return (final_point[1] - initial_point[1])/(final_point[0] - initial_point[0])

    def compute(coordinates: list, eval_point):
        '''
        Compute the Newton polynomial and returns the value of the fuction
        evaluated in eval_point.

        Arguments:
        - coordinates: this are the coordinates in R², this structure is
                    a list with the coordinates in tuples, for example
                    [(-2,-2),(-1,-1),(0,0),(1,1),(2,2)]

        - eval_point: is the point of eval in the equation of Lagrange
                    polynomial, this can be a point (float or int)
                    or a array of points to eval, correspond to axis
                    X in the plane R².
        '''

        # Suppose the next coordinates: [(0,0), (1,1), (2,4), (3,6)]
        # for EVERY line constructed (take this to a example guie)

        summation = 0 # Initial term of the summatory

        #po = coordinates[0][1] # Initial term of the polynomial

        #p0 + (eval_point - coordinates[0][0])

        # The first coefficient (when is grade one) is every the
        # basic slope of a first degree equation.
        init_coef = slope(coordinates[0], coordinates[1])

        x0 = coordinates[0][0]
        last_coef = init_coef
        y_aux = 0

        print(f'Initial coeficiente = {init_coef}')
        
        # this bucle begin to 
        for i in range(2, len(coordinates)):
            print('Iretation ', i)

            
            last_coef = slope(coordinates[i-1], coordinates[i]) -  y_aux
            print(f'\tlast_coef = {last_coef/(coordinates[i][0]-x0)}')
            y_aux = last_coef
            last_coef /= (coordinates[i][0]-x0)



