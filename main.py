import random


"""
1. Problem Data
"""

courses = [
    {"name": "CISC101", "instructor": "Prof.A"},
    {"name": "CISC102", "instructor": "Prof.B"},
    {"name": "CISC201", "instructor": "Prof.A"},
    {"name": "CISC202", "instructor": "Prof.C"},
    {"name": "CISC301", "instructor": "Prof.D"},
    {"name": "CISC302", "instructor": "Prof.B"},
    {"name": "CISC303", "instructor": "Prof.E"},
    {"name": "CISC304", "instructor": "Prof.C"},
]

NUM_SLOTS = 5
NUM_ROOMS = 2

POP_SIZE = 60
MAX_GENERATIONS = 500
CROSSOVER_RATE = 0.80
MUTATION_RATE = 0.12
TOURNAMENT_SIZE = 3
ELITE_COUNT = 2
CGM_PROBABILITY = 0.60

random.seed(42)

"""
# 2. Basic Functions
"""

def random_chromosome(num_courses, num_slots):
    chromosome = []
    i = 0
    while i < num_courses:
        chromosome.append(random.randint(0, num_slots - 1))
        i = i + 1
    return chromosome


def initialize_population(pop_size, num_courses, num_slots):
    population = []
    i = 0
    while i < pop_size:
        chromosome = random_chromosome(num_courses, num_slots)
        population.append(chromosome)
        i = i + 1
    return population


def decode_schedule(chromosome, courses, num_slots, num_rooms):
    slot_courses = []
    slot_room_assignment = []

    slot_index = 0
    while slot_index < num_slots:
        slot_courses.append([])
        slot_room_assignment.append([])
        slot_index = slot_index + 1

    course_index = 0
    while course_index < len(chromosome):
        slot = chromosome[course_index]
        slot_courses[slot].append(course_index)
        course_index = course_index + 1

    slot_index = 0
    while slot_index < num_slots:
        room_number = 0
        course_position = 0

        while course_position < len(slot_courses[slot_index]):
            course_index = slot_courses[slot_index][course_position]

            if room_number < num_rooms:
                slot_room_assignment[slot_index].append((course_index, room_number))
                room_number = room_number + 1
            else:
                slot_room_assignment[slot_index].append((course_index, -1))

            course_position = course_position + 1

        slot_index = slot_index + 1

    return slot_courses, slot_room_assignment


"""
# 3. Fitness and Conflict Counting
"""

def count_conflicts(chromosome, courses, num_slots, num_rooms):
    slot_courses, slot_room_assignment = decode_schedule(chromosome, courses, num_slots, num_rooms)

    room_conflicts = 0
    instructor_conflicts = 0
    conflicted_courses = []

    slot_index = 0
    while slot_index < num_slots:
        used_instructors = []

        assignment_index = 0
        while assignment_index < len(slot_room_assignment[slot_index]):
            course_index, room_number = slot_room_assignment[slot_index][assignment_index]

            if room_number == -1:
                room_conflicts = room_conflicts + 1
                if course_index not in conflicted_courses:
                    conflicted_courses.append(course_index)

            assignment_index = assignment_index + 1

        course_position = 0
        while course_position < len(slot_courses[slot_index]):
            course_index = slot_courses[slot_index][course_position]
            instructor_name = courses[course_index]["instructor"]

            if instructor_name in used_instructors:
                instructor_conflicts = instructor_conflicts + 1

                if course_index not in conflicted_courses:
                    conflicted_courses.append(course_index)

                other_position = 0
                while other_position < len(slot_courses[slot_index]):
                    other_course_index = slot_courses[slot_index][other_position]
                    other_instructor_name = courses[other_course_index]["instructor"]

                    if other_instructor_name == instructor_name:
                        if other_course_index not in conflicted_courses:
                            conflicted_courses.append(other_course_index)

                    other_position = other_position + 1
            else:
                used_instructors.append(instructor_name)

            course_position = course_position + 1

        slot_index = slot_index + 1

    total_conflicts = room_conflicts + instructor_conflicts
    return total_conflicts, room_conflicts, instructor_conflicts, conflicted_courses


def fitness(chromosome, courses, num_slots, num_rooms):
    total_conflicts, room_conflicts, instructor_conflicts, conflicted_courses = count_conflicts(
        chromosome, courses, num_slots, num_rooms
    )
    return -total_conflicts


"""
# 4. Selection
"""

def tournament_selection(population, fitnesses, tournament_size):
    chosen_index = random.randint(0, len(population) - 1)
    best_index = chosen_index

    count = 1
    while count < tournament_size:
        chosen_index = random.randint(0, len(population) - 1)

        if fitnesses[chosen_index] > fitnesses[best_index]:
            best_index = chosen_index

        count = count + 1

    copied = []
    i = 0
    while i < len(population[best_index]):
        copied.append(population[best_index][i])
        i = i + 1

    return copied


"""
# 5. Variation Operators
"""

def single_point_crossover(parent1, parent2, crossover_rate):
    if random.random() > crossover_rate:
        child1 = []
        child2 = []

        i = 0
        while i < len(parent1):
            child1.append(parent1[i])
            child2.append(parent2[i])
            i = i + 1

        return child1, child2

    if len(parent1) <= 1:
        child1 = []
        child2 = []

        i = 0
        while i < len(parent1):
            child1.append(parent1[i])
            child2.append(parent2[i])
            i = i + 1

        return child1, child2

    point = random.randint(1, len(parent1) - 1)

    child1 = []
    child2 = []

    i = 0
    while i < point:
        child1.append(parent1[i])
        child2.append(parent2[i])
        i = i + 1

    while i < len(parent1):
        child1.append(parent2[i])
        child2.append(parent1[i])
        i = i + 1

    return child1, child2


def random_mutation(chromosome, num_slots, mutation_rate):
    mutated = []
    i = 0
    while i < len(chromosome):
        mutated.append(chromosome[i])
        i = i + 1

    i = 0
    while i < len(mutated):
        if random.random() < mutation_rate:
            mutated[i] = random.randint(0, num_slots - 1)
        i = i + 1

    return mutated


def conflict_guided_mutation(chromosome, courses, num_slots, num_rooms):
    mutated = []
    i = 0
    while i < len(chromosome):
        mutated.append(chromosome[i])
        i = i + 1

    total_conflicts, room_conflicts, instructor_conflicts, conflicted_courses = count_conflicts(
        mutated, courses, num_slots, num_rooms
    )

    if len(conflicted_courses) == 0:
        return mutated

    i = 0
    while i < len(conflicted_courses):
        course_index = conflicted_courses[i]
        mutated[course_index] = random.randint(0, num_slots - 1)
        i = i + 1

    return mutated


def mutate(chromosome, courses, num_slots, num_rooms, mutation_rate, cgm_probability):
    if random.random() < cgm_probability:
        return conflict_guided_mutation(chromosome, courses, num_slots, num_rooms)
    else:
        return random_mutation(chromosome, num_slots, mutation_rate)


"""
# 6. Population Management
"""

def get_best_index(fitnesses):
    best_index = 0
    i = 1
    while i < len(fitnesses):
        if fitnesses[i] > fitnesses[best_index]:
            best_index = i
        i = i + 1
    return best_index


def get_elites(population, fitnesses, elite_count):
    elite_population = []
    used_indices = []

    count = 0
    while count < elite_count:
        best_index = -1
        i = 0

        while i < len(population):
            if i not in used_indices:
                if best_index == -1 or fitnesses[i] > fitnesses[best_index]:
                    best_index = i
            i = i + 1

        copied = []
        j = 0
        while j < len(population[best_index]):
            copied.append(population[best_index][j])
            j = j + 1

        elite_population.append(copied)
        used_indices.append(best_index)
        count = count + 1

    return elite_population


"""
# 7. Main EA Loop
"""

def run_ea(courses, num_slots, num_rooms,
           pop_size, max_generations,
           crossover_rate, mutation_rate,
           tournament_size, elite_count,
           cgm_probability):

    num_courses = len(courses)
    population = initialize_population(pop_size, num_courses, num_slots)

    best_solution = None
    best_fitness = -999999
    history = []

    generation = 0
    while generation < max_generations:
        fitnesses = []
        i = 0
        while i < len(population):
            one_fitness = fitness(population[i], courses, num_slots, num_rooms)
            fitnesses.append(one_fitness)
            i = i + 1

        current_best_index = get_best_index(fitnesses)
        current_best_fitness = fitnesses[current_best_index]

        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_solution = []

            i = 0
            while i < len(population[current_best_index]):
                best_solution.append(population[current_best_index][i])
                i = i + 1

        history.append(best_fitness)

        if best_fitness == 0:
            print("Stopped early at generation", generation)
            print("A conflict-free schedule was found.")
            break

        new_population = get_elites(population, fitnesses, elite_count)

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses, tournament_size)
            parent2 = tournament_selection(population, fitnesses, tournament_size)

            child1, child2 = single_point_crossover(parent1, parent2, crossover_rate)

            child1 = mutate(child1, courses, num_slots, num_rooms, mutation_rate, cgm_probability)
            child2 = mutate(child2, courses, num_slots, num_rooms, mutation_rate, cgm_probability)

            new_population.append(child1)

            if len(new_population) < pop_size:
                new_population.append(child2)

        population = new_population
        generation = generation + 1

    return best_solution, best_fitness, history


"""
# 8. Print Output
"""

def print_schedule(chromosome, courses, num_slots, num_rooms):
    slot_courses, slot_room_assignment = decode_schedule(chromosome, courses, num_slots, num_rooms)

    print("\nFinal Schedule:")
    slot_index = 0
    while slot_index < num_slots:
        print("Time Slot", slot_index, ":")

        if len(slot_room_assignment[slot_index]) == 0:
            print("  (empty)")
        else:
            assignment_index = 0
            while assignment_index < len(slot_room_assignment[slot_index]):
                course_index, room_number = slot_room_assignment[slot_index][assignment_index]
                course_name = courses[course_index]["name"]
                instructor_name = courses[course_index]["instructor"]

                if room_number == -1:
                    print(" ", course_name, "-", instructor_name, "- no room assigned")
                else:
                    print(" ", course_name, "-", instructor_name, "- Room", room_number)

                assignment_index = assignment_index + 1

        slot_index = slot_index + 1

    total_conflicts, room_conflicts, instructor_conflicts, conflicted_courses = count_conflicts(
        chromosome, courses, num_slots, num_rooms
    )

    print("\nConflict Summary:")
    print("Total conflicts =", total_conflicts)
    print("Room conflicts =", room_conflicts)
    print("Instructor conflicts =", instructor_conflicts)


"""
# 9. Run Program
"""

best_solution, best_fitness, history = run_ea(
    courses,
    NUM_SLOTS,
    NUM_ROOMS,
    POP_SIZE,
    MAX_GENERATIONS,
    CROSSOVER_RATE,
    MUTATION_RATE,
    TOURNAMENT_SIZE,
    ELITE_COUNT,
    CGM_PROBABILITY
)

print("Best fitness =", best_fitness)
print("Best chromosome =", best_solution)

print_schedule(best_solution, courses, NUM_SLOTS, NUM_ROOMS)

print("\nBest fitness over generations:")
print(history)