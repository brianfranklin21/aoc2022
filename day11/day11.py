""" https://adventofcode.com/2022/day/11
"""


class Monkey:

    def __init__(self, id, items, op, test) -> None:
        self.id = id
        self.items = items
        self.op = op
        self.test = test
        self.insp_cnt = 0

    def __repr__(self) -> str:
        return f"{self.items}"


class MonkeyBusiness:

    def __init__(self) -> None:
        self.monkeys = {}
        self.divisors_prod = 1  # unreduced LCM

    def enlist_monkey(self, d) -> None:
        m = int(d[0][-1])
        items = [int(i) for i in d[1][2:]]
        operand1, operator, operand2 = d[2][3:]
        test_value, if_true, if_false = int(d[3][-1]), int(d[4][-1]), int(d[5][-1])
        op = eval(f"lambda old: {operand1} {operator} {operand2}")
        test = eval(f"lambda i: {if_true} if i % {test_value} == 0 else {if_false}")
        self.monkeys[m] = Monkey(m, items, op, test)
        self.divisors_prod *= test_value
        # print(f"LCM = {self.divisors_prod}")
        # print(f"d = {d}")
        # print(m, items)
        # print(m, operand1, operator, operand2)
        # print(m, test_value, if_true, if_false)
        # print(f"Enlisted Monkey {m}")

    def play(self, part1=True) -> None:
        # print("Starting a round", self.monkeys)
        for m, monkey in self.monkeys.items():
            # print(f"Monkey {m} starts playing")
            # print(self.monkeys)
            while self.monkeys[m].items:
                self.monkeys[m].insp_cnt += 1
                # print(f"Monkey {m} inspects {item}")
                self.monkeys[m].items[0] = monkey.op(self.monkeys[m].items[0])
                # print(self.monkeys)
                if part1:
                    self.monkeys[m].items[0] //= 3
                else:
                    self.monkeys[m].items[0] %= self.divisors_prod
                # print("You relax")
                # print(self.monkeys)
                next_m = monkey.test(self.monkeys[m].items[0])
                # print(m, self.monkeys[m].items[i], next_m)
                # print(f"Monkey {m} tossed {self.monkeys[m].items[0]} to Monkey {next_m}")
                self.monkeys[next_m].items.append(self.monkeys[m].items.pop(0))
                # print(next_m, self.monkeys[next_m].items)
                # print(self.monkeys)


class DayEleven:

    def __init__(self, input_fname):
        with open(input_fname, 'r') as _file:
            self.data = [[i.strip(",:") for i in line.split()] for line in _file]

    def part1(self):
        """ Figure out which monkeys to chase by counting how many items they inspect
            over 20 rounds. What is the level of monkey business after 20 rounds of
            stuff-slinging simian shenanigans?
        """
        print("Part1")
        mb = MonkeyBusiness()
        for i in range(0, len(self.data), 7):
            mb.enlist_monkey(self.data[i:7 + i])
        print(mb.monkeys)

        for _ in range(20):
            mb.play()
        print(mb.monkeys)

        insp_cnts = [m.insp_cnt for m in mb.monkeys.values()]
        print(insp_cnts)
        print(sorted(insp_cnts)[-1] * sorted(insp_cnts)[-2])

    def part2(self):
        """ Worry levels are no longer divided by three after each item is inspected;
            you'll need to find another way to keep your worry levels manageable.
            Starting again from the initial state in your puzzle input,
            what is the level of monkey business after 10000 rounds?
        """
        print("Part2")
        mb = MonkeyBusiness()
        for i in range(0, len(self.data), 7):
            mb.enlist_monkey(self.data[i:7 + i])
        print(mb.monkeys)

        for _ in range(10000):
            mb.play(part1=False)
        print(mb.monkeys)

        insp_cnts = [m.insp_cnt for m in mb.monkeys.values()]
        print(insp_cnts)
        print(sorted(insp_cnts)[-1] * sorted(insp_cnts)[-2])


# day11 = DayEleven("sample.txt")
day11 = DayEleven("input.txt")
day11.part1()
day11.part2()
