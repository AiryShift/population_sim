import random
import sys
import time
from collections import Counter

NUM_PEOPLE = 100
NUM_GENERATIONS = 100


def decision(probability):
    return random.random() < probability


def next_generation(people):
    random.shuffle(people)
    new = []
    for i in range(0, len(people) // 2 * 2, 2):
        first, second = people[i], people[i + 1]
        # probability for same named children
        if decision(0.55):
            new_surname = random.choice([first, second])
            people[i] = people[i + 1] = new_surname

        # probability for new child
        if decision(0.2):
            new.append(random.choice([first, second]))
    people.extend(new)


if __name__ == '__main__':
    start_time = time.time()

    people = list(range(NUM_PEOPLE))
    for generation in range(NUM_GENERATIONS):
        print('Current generation: {}'.format(generation), file=sys.stderr)
        next_generation(people)

    people_frequency = Counter(people)
    print('Occurences')
    for last_name, freq in sorted(people_frequency.items()):
        print('{}: {}'.format(last_name, freq))
    print('Total population:', sum(people_frequency.values()))

    print('Took {:.2f}s'.format(time.time() - start_time), file=sys.stderr)
