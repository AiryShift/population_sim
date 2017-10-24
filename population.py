#!/usr/bin/env python

import argparse
import random
import sys
import time
from collections import Counter

import matplotlib.pyplot as plt


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


def plot(args, data):
    fig = plt.figure()
    graph = fig.add_subplot(111)
    graph.set_title('Number of surnames after n generations')
    graph.set_xlabel('Generations')
    graph.set_ylabel('Population count')
    if args.growth_factor > 1:
        graph.set_yscale('log')

    population_over_time = [[] for _ in range(args.people)]
    for count in data:
        for name in range(args.people):
            population_over_time[name].append(count.get(name, 0))

    for name, count in enumerate(population_over_time):
        graph.plot(range(1, args.generations + 1),
                   count,
                   label=str(name),
                   marker='.')

    font_properties = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    text = ('Initial unique surnames: {}\n'
            'Generations: {}\n'
            'Same name probability: {}\n'
            'Growth factor: {}'.format(args.people,
                                       args.generations,
                                       args.same_name_chance,
                                       args.growth_factor
                                       )
            )

    graph.text(0.05,
               0.95,
               text,
               transform=graph.transAxes,
               fontsize=13,
               verticalalignment='top',
               bbox=font_properties)
    plt.show()


def textdump(generation, counter):
    print('Generation:', generation)
    for last_name, freq in sorted(counter.items()):
        print('{}: {}'.format(last_name, freq))
    print('Total population:', sum(counter.values()))


def main(args):
    start_time = time.time()
    data = []
    people = list(range(args.people))
    for generation in range(args.generations):
        print('Current generation:', generation, file=sys.stderr)
        next_generation(people)

        counter = Counter(people)
        textdump(generation, counter)
        data.append(counter)

    print('Took {:.2f}s'.format(time.time() - start_time), file=sys.stderr)
    plot(args, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Does some population counting')
    parser.add_argument('-p',
                        '--people',
                        type=int,
                        default=100,
                        help='Size of initial population')
    parser.add_argument('-g',
                        '--generations',
                        type=int,
                        default=120,
                        help='Number of generations')
    parser.add_argument('-s',
                        '--same-name-chance',
                        type=float,
                        default=0.55,
                        help='Chance that the two children of a couple have the same last name')
    parser.add_argument('-f',
                        '--growth-factor',
                        type=float,
                        default=1.1,
                        help='Average growth factor of the population')
    args = parser.parse_args()
    assert(args.growth_factor >= 1)
    main(args)
