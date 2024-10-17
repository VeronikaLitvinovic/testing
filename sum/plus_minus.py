import random

def simulate_money_changes():
    num_people = 50
    initial_amount = 1000
    iterations = 100

    people = [initial_amount] * num_people

    for iteration in range(iterations):
        for i in range(num_people):
            change_factor = 1.1 if random.choice([True, False]) else 0.9
            people[i] *= change_factor

        total_after_iteration = sum(people)
        print(f"Total money after iteration {iteration + 1}: {total_after_iteration:.2f} rubles")

    # for index, amount in enumerate(people, start=1):
    #     print(f"Person {index}: {amount:.2f} rubles")

    final_total = sum(people)
    print(f"\nFinal total money of all people: {final_total:.2f} rubles")

simulate_money_changes()
