import numpy as np

class EP_Optimizer:
    def __init__(self, menu_df, target_cal, target_prot, target_fat):
        # We now pass protein and fat targets from the Streamlit sliders
        self.df = menu_df
        self.target_cal = target_cal
        self.target_prot = target_prot
        self.target_fat = target_fat
        self.cats = ['Breakfast', 'Lunch', 'Dinner', 'Snack']

    def fitness(self, individual):
        total_price = 0
        total_cal = 0
        total_prot = 0
        total_fat = 0
        
        for i, cat in enumerate(self.cats):
            items = self.df[self.df['Category'] == cat]
            idx = individual[i] % len(items)
            meal = items.iloc[idx]
            
            total_price += meal['Price_RM']
            total_cal += meal['Calories']
            total_prot += meal['Protein']
            total_fat += meal['Fat']
        
        # --- PENALTIES (The "Rules" of the optimization) ---
        
        # 1. Calorie Penalty (Stay close to target)
        cal_penalty = abs(total_cal - self.target_cal) * 5
        
        # 2. Protein Penalty (Bad if total protein is LOWER than target)
        # If total_prot is 100 and target is 100, penalty is 0.
        prot_penalty = max(0, self.target_prot - total_prot) * 10
        
        # 3. Fat Penalty (Bad if total fat is HIGHER than target)
        fat_penalty = max(0, total_fat - self.target_fat) * 10
        
        # The goal is to minimize this final score
        return total_price + cal_penalty + prot_penalty + fat_penalty

    def run(self, generations=100, pop_size=50, mut_rate=0.3):
        # 1. INITIALIZATION
        pop = []
        for _ in range(pop_size):
            # Start with 4 random numbers representing the 4 meals
            ind = [np.random.randint(0, 100) for _ in range(4)]
            pop.append(ind)
        
        history = []
        
        # 2. EVOLUTION LOOP
        for g in range(generations):
            # MUTATION: This is the core of Evolutionary Programming
            offspring = []
            for parent in pop:
                child = parent.copy()
                for i in range(4):
                    if np.random.rand() < mut_rate:
                        # Change the meal index to a new random one
                        child[i] = np.random.randint(0, 100)
                offspring.append(child)
            
            # 3. SELECTION (Survival of the fittest)
            combined = pop + offspring
            # Sort by fitness score (lowest is the "best")
            combined.sort(key=lambda x: self.fitness(x))
            
            # Keep the top half (pop_size) to be parents for next time
            pop = combined[:pop_size]
            
            # Save the best score so we can graph it in Streamlit
            history.append(self.fitness(pop[0]))
            
        return pop[0], history
