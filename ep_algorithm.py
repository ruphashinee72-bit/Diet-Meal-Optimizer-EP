import numpy as np

class EP_Optimizer:
    def __init__(self, menu_df, target_cal):
        self.df = menu_df
        self.target_cal = target_cal
        self.cats = ['Breakfast', 'Lunch', 'Dinner', 'Snack']

    def fitness(self, individual):
        total_price = 0
        total_cal = 0
        for i, cat in enumerate(self.cats):
            # Pick the meal using the index from the 'individual' list
            items = self.df[self.df['Category'] == cat]
            meal = items.iloc[individual[i] % len(items)]
            total_price += meal['Price_RM']
            total_cal += meal['Calories']
        
        # If calories are far from target, we add a "penalty" (bad score)
        penalty = abs(total_cal - self.target_cal) * 10
        return total_price + penalty

    def run(self, generations=50, pop_size=20):
        # 1. Start with random meal plans
        pop = []
        for _ in range(pop_size):
            ind = [np.random.randint(0, 50) for _ in range(4)]
            pop.append(ind)
        
        history = []
        for g in range(generations):
            # 2. Mutation: Copy parents and change one meal randomly
            offspring = [ind.copy() for ind in pop]
            for child in offspring:
                child[np.random.randint(0, 4)] = np.random.randint(0, 50)
            
            # 3. Selection: Keep the best ones
            combined = pop + offspring
            combined.sort(key=lambda x: self.fitness(x))
            pop = combined[:pop_size]
            history.append(self.fitness(pop[0]))
            
        return pop[0], history
