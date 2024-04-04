# Direct methods
# Matrix
import numpy as np

class Base:
    
    def set_parameters(self, matrix, b):
        '''
        Given the matrix equation Ax = b, where:

        - A is a square matrix of shape NxN, denoted with matrix argument.
        - b is the solution vector, denoted with b argument.
        '''

        assert type(matrix) == np.matrix, 'matrix argument must be numpy.matrix'
        assert type(b) == np.ndarray, 'solution vector (b) argument must be numpy.ndarray'

        self.matrix = matrix    # Saving matrix (A)
        self.b = b              # Saving solution vector (b)
        
        # Pre-setting the solution vector
        len_x_vector = self.matrix.shape[0]     # Saving length of x vector
        self.solution = np.zeros(len_x_vector)  # Create void x vector



class Diagonal(Base):

    
    def fit(self):
        '''
        Remeber the matrix equation Ax = b, we previously declare A and b,
        this method compute the variables vector (x).
        '''


        # Mutating over solution vector (fitting)
        for index in range(len_x_vector):
            self.solution[index] = self.b[index] /  self.matrix[index,index]

class Lower_Triangular(Base):

    def fit(self):
        '''
        '''
        
        # Fitting the initial element
        self.solution[0] = self.b[0] / self.matrix[0,0]

        # Iterating for fitting the rest of terms for each row
        for index in range(1, self.b.shape[0]):
            
            # Iterating over the each element of a row
            summation = 0
            for r in range(0, index):
                term = self.matrix[index, r] * self.solution[r]
                summation += term
            
    
            self.solution[index] = (self.b[index] - summation) / self.matrix[index, index]
 

class Upper_Triangular(Base):
 
    def fit(self):
        '''
        ¡Important!

        Remember these notations:
        - [::-1] -> Invert the orden of a iterable.
        '''
        
        # Fitting the initial element
        self.solution[-1] = self.b[-1] / self.matrix[-1,-1]

        # Iterating for fitting the rest of terms for each row
        # [0,1,2,3][::-1] -> [3,2,1,0]
        for index in range(0, self.b.shape[0]-1)[::-1]:
            
            # Iterating over the each element of a row
            summation = 0
            for r in range(index, self.b.shape[0])[::-1]:
                term = self.matrix[index, r] * self.solution[r]
                summation += term
            
    
            self.solution[index] = (self.b[index] - summation) / self.matrix[index, index]

class Gauss(Base):

    def fit(self):
        '''
        Compute the gauss descomposition
        '''

        # Copy elements for no mutating
        matrix = self.matrix.copy()
        b = self.b.copy()

        # Fitting
        for row in matrix:

            factor


