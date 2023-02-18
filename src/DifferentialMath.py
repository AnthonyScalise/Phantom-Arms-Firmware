
# This file contains custom libraries for working with the Phantom Arm 4 input 3 output differential
# Created by: Anthony Scalise (2/18/2023)

# Imports
import numpy as np



# Class that handles the Phantom Arm 4 input 3 output differential with the new matrix multiplication method
class PhantomArmDifferential:
    def __init__(self):
        self.inverse_transformation_matrix = np.array([
                                                [1, -1, -1],
                                                [1,  1, -1],
                                                [1,  1,  1],
                                                [1, -1,  1]
                                            ])
    
    # Class method that takes in three output deltas and returns the corresponding 4 input deltas
    def compute_inverse_differential(self, output_1, output_2, output_3):
        output_vector = np.array([[output_1, output_2, output_3]]).T
        return((self.inverse_transformation_matrix @ output_vector).T[0].tolist())
    
    

# Class that handles the Phantom Arm 4 input 3 output differential with the old input output modality table method
class PhantomArmDifferential_old:
    def __init__(self):
        self.base_output_modalities = [
                                    [0, 0, 0],
                                    [1, 0, 0], [-1, 0, 0],
                                    [0, 1, 0], [0, -1, 0],
                                    [0, 0, 1], [0, 0, -1]
                                ]
        self.base_input_modalities = [
                                    [0, 0, 0, 0],
                                    [1, 1, 1, 1], [-1, -1, -1, -1],
                                    [-1, 1, 1, -1], [1, -1, -1, 1],
                                    [-1, -1, 1, 1], [1, 1, -1, -1]
                                ]

        # Class method that handles division by zero errors
        def weird_division(self, x, y):
            try:
                return(x/y)
            except ZeroDivisionError:
                return 0
                
        # Class method that returns the base input modality component given an output delta component and the output index
        def get_input_modality_from_base_modalities(self, output_delta, output_index):
            normalized_magnitude = weird_division(output_delta, abs(output_delta))
            for i, modality in enumerate(self.base_output_modalities):
                if normalized_magnitude == modality[output_index]:
                    return(self.base_input_modalities[i][:])
            return -1

        # Class method that computes the required input deltas given the desired output deltas using the base component method                      
        def arm_algorithm_backwards_from_base_modalities(self, output_1, output_2, output_3):
            outputs = [output_1, output_2, output_3]
            input_solution = [0, 0, 0, 0]
            input_modality_components = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
            for i, output in enumerate(outputs):
                input_modality_components[i] = get_input_modality_from_base_modalities(output, i)
                for input_index in range(4):
                    input_modality_components[i][input_index] *= abs(output)
            for input_component in input_modality_components:
                for input_index in range(4):
                    input_solution[input_index] += input_component[input_index]
            return(input_solution)       

