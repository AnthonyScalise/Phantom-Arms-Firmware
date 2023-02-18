
# This file contains custom libraries for working with gears and gear trains
# Created by: Anthony Scalise (2/18/2023)



# Class that represents a gear
class Gear:
    def __init__(self, num_teeth, gear_id=None):
        self.num_teeth = num_teeth
        self.gear_id = gear_id
        self.gear_ratios = {}
        
    # Class method that returns the number of teeth
    def get_num_teeth(self):
        return(self.num_teeth)
    
    # Class method that returns the gear id
    def get_gear_id(self):
        return(self.gear_id)
    
    # Class method that takes an output gear of the Gear class and returns the gear ratio between itself and the output gear
    def get_gear_ratio(self, output_gear):
        if output_gear.get_gear_id() in self.gear_ratios.keys():
            return(self.gear_ratios[output_gear.get_gear_id()])
        else: 
            self.gear_ratios[output_gear.get_gear_id()] = (output_gear.get_num_teeth() / self.get_num_teeth())
            return(self.gear_ratios[self.gear_ratios[output_gear.get_gear_id()]])

    # Class method that takes an input angle delta and an output gear of the Gear class and returns the output angle delta
    def get_output_delta(self, input_delta, output_gear):
        return(input_delta / self.get_gear_ratio(output_gear))
    
    # Class method that takes a desired output angle delta and an output gear of the Gear class and returns the input angle delta required
    def get_input_delta(self, output_delta, output_gear):
        return(output_delta * self.get_gear_ratio(output_gear))
    
    
    
# Class that represents a gear train of three or more gears
class GearTrain:
    def __init__(self, first_gear, gear_train_id=None):
        self.gear_train_id = gear_train_id
        self.gear_list = [[first_gear]]
        self.gear_train_ratio = 1
        self.output_magnitude_is_flipped = False
        self.coaxial_pairs_indexes = []
        
    # Class method that returns the gear train id
    def get_gear_train_id(self):
        return(self.gear_train_id)
        
    # Class method that returns the gear list
    def get_gear_list(self):
        return(self.gear_list)
    
    # Class method that returns the gear train ratio
    def get_gear_train_ratio(self):
        return(self.gear_train_ratio)
    
    # Class method that returns whether or not the output magnitude is flipped
    def get_output_magnitude_is_flipped(self):
        return(self.output_magnitude_is_flipped)
    
    # Class method that adds a gear to the gear train meshed with the last gear in the gear list
    def add_gear(self, gear):
        self.gear_list.append([gear])
        self.output_magnitude_is_flipped = not self.output_magnitude_is_flipped
        self.update_gear_train_ratio()
    
    # Class method that adds a gear to the gear train coaxial with the last gear in the gear list
    def add_coaxial_gear(self, gear):
        if(len(self.gear_list[-1]) < 2):
            self.gear_list[-1].append(gear)
            self.coaxial_pairs_indexes.append(len(self.gear_list) - 1)
            self.update_gear_train_ratio()
        else:
            raise("GearTrain.add_coaxial_gear: Does not support multiple coaxial gears")
        
    # Class method that takes an input angle delta and returns the output angle delta
    def get_output_delta(self, input_delta):
        return(input_delta / self.get_gear_train_ratio())

    # Class method that takes a desired output angle delta and returns the input angle delta required
    def get_input_delta(self, output_delta):
        return(output_delta * self.get_gear_train_ratio())

    # Function that updates the gear train ratio
    def update_gear_train_ratio(self):
        compounding_gear_ratios = []
        net_ratio = 1
        current_input_gear = self.get_gear_list()[0][0]
        for i in range(1, len(self.get_gear_list())):
            if i in self.coaxial_pairs_indexes:
                compounding_gear_ratios.append(current_input_gear.get_gear_ratio(self.get_gear_list()[i][0]))
                current_input_gear = self.get_gear_list()[i][1]
            if i < (len(self.get_gear_list()) - 3):
                if len(self.get_gear_list()[i + 1]) == 1 and (i + 2) in self.coaxial_pairs_indexes:
                    compounding_gear_ratios.append(current_input_gear.get_gear_ratio(self.get_gear_list()[i + 1][0]))
                    current_input_gear = self.get_gear_list()[i + 1][0]
            elif i == (len(self.get_gear_list()) - 1) and i not in self.coaxial_pairs_indexes:
                compounding_gear_ratios.append(current_input_gear.get_gear_ratio(self.get_gear_list()[i][0]))
        for i in range(len(compounding_gear_ratios)):
            net_ratio *= compounding_gear_ratios[i]
        self.gear_train_ratio = net_ratio
        print(compounding_gear_ratios)

