import argparse
import random
import sys
import time
from collections import Counter


def decision(probability):
    return random.random() < probability


def next_generation(people):
    random.shuffle(people)
    new = []
    for i in range(0, len(people) // 2 * 2, 2):
        first, second = people[i], people[i + 1]
        # probability for same named children
        if decision(args.same_name_chance):
            new_surname = random.choice([first, second])
            people[i] = people[i + 1] = new_surname

        # probability for new child
        # multiplies by 2 because only couples produce extra children
        if decision((args.growth_factor - 1) * 2):
            new.append(random.choice([first, second]))
    people.extend(new)


def main(args):
    start_time = time.time()

    people = list(range(args.people))
    for generation in range(args.generations):
        print('Current generation:', generation, file=sys.stderr)
        next_generation(people)

    people_frequency = Counter(people)
    print('Occurences')
    for last_name, freq in sorted(people_frequency.items()):
        print('{}: {}'.format(last_name, freq))
    print('Total population:', sum(people_frequency.values()))

    print('Took {:.2f}s'.format(time.time() - start_time), file=sys.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Does some population counting')
    parser.add_argument('-p', '--people', type=int, default=100, help='Number of people')
    parser.add_argument('-g', '--generations', type=int, default=120, help='Number of generations')
    parser.add_argument('-s', '--same-name-chance', type=float, default=0.55, help='Chance that the two children of a couple have the same last name')
    parser.add_argument('-f', '--growth-factor', type=float, default=1.1, help='Average growth factor of the population')
    args = parser.parse_args()
    main(args)
