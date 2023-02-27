def filter_input(input, target):
    input_upper = input.upper()
    input_lower = input.lower()

    target_list = [target.upper(), target.lower()]

    for i in target_list:
        if input_lower == i:
            return input_lower
        
        elif input_upper == i: 
            return input_upper
        
    else: 
        return False

use = input('Welcome! \n Are you locking or unlocking your bicycle? \n Please type your answer and press enter.')

print(filter_input(use, 'Locking'))
print(filter_input(use, 'Unlocking'))
