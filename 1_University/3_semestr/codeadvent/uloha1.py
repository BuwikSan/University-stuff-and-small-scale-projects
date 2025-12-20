import os

CUSTOM_NUMBER_OF_POSITIONS = 100
PRACTICE_DATASET = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]

def points_to_zero(rotations, starting_rotation=50, number_of_positions = 100):
    sum_to_zero = 0
    current_position = starting_rotation

    for rotation in rotations:
    
        rotation_direction, rotation_steps = parse_line(rotation)
        if rotation_direction == 'R':
            current_position = (current_position + rotation_steps) % number_of_positions
        else:
            current_position = (current_position - rotation_steps) % number_of_positions
        
        if current_position == 0:
            sum_to_zero += 1
        
    return sum_to_zero


def parse_line(line: str):
    direction = line[0]
    steps = int(line[1:])
    return direction, steps




def give_password(rotations, start_position=50, number_of_positions = 100):
    
    current_position = start_position
    previous_position = start_position
    sum_point_to_zero = 0
    
    for rotation in rotations:
        direction, steps = parse_line(rotation)

        if direction == 'R':
            current_position += steps
        else:
            current_position -= steps

        sum_point_to_zero += abs(current_position // number_of_positions)


        current_position = current_position % number_of_positions

        if current_position == 0 and direction == 'L':
            sum_point_to_zero += 1
        if previous_position == 0 and direction == 'L':
            sum_point_to_zero -= 1

        previous_position = current_position


    return sum_point_to_zero

if __name__ == '__main__':
    current_dir = os.path.dirname(__file__)
    os.chdir(current_dir)

    with open('resources/input1.txt', 'r', encoding='utf-8') as f:
        obsah = f.read()


    lines = obsah.splitlines()
    result1_practice = points_to_zero(PRACTICE_DATASET, starting_rotation=50, number_of_positions=CUSTOM_NUMBER_OF_POSITIONS)
    print(f'Practice result 1: {result1_practice}')
    result2_practice = give_password(PRACTICE_DATASET, start_position=50, number_of_positions=CUSTOM_NUMBER_OF_POSITIONS)
    print(f'Practice result 2: {result2_practice}')
    #result1 = give_password(lines, start_position=50, number_of_positions=CUSTOM_NUMBER_OF_POSITIONS)
    #print(f'Result: {result}')
    #result2 = give_password(lines, start_position=50, number_of_positions=CUSTOM_NUMBER_OF_POSITIONS)
    #print(f'Result 2: {result2}')