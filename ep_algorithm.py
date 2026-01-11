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
            # Filter menu items by category
            items = self.df[self.df['Category'] == cat]
            # Ensure the index is within range
            idx = individual[i] % len(items)
            meal = items.iloc[idx]
            
            total_price += meal['Price_RM']
            total_cal += meal['Calories']
        
        # PENALTY: If calories are not near target, score gets worse (higher)
        # This is how we handle constraints in EP
        penalty = abs(total_cal - self.target_cal) * 10
        return total_price + penalty

    def run(self, generations=100, pop_size=50, mut_rate=0.3):
        """
        generations: from Streamlit slider
        pop_size: from Streamlit slider
        mut_rate: how likely a meal is to change
        """
        # 1. INITIALIZATION: Start with random meal plan indices
        pop = []
        for _ in range(pop_size):
            # Create a random list of 4 numbers (one for each meal category)
            ind = [np.random.randint(0, 100) for _ in range(4)]
            pop.append(ind)
        
        history = []
        
        # 2. EVOLUTION LOOP
        for g in range(generations):
            # MUTATION: Create offspring by copying parents and mutating
            offspring = []
            for parent in pop:
                child = parent.copy()
                # EP Mutation: Every child is a slightly changed version of the parent
                for i in range(4):
                    if np.random.rand() < mut_rate:
                        # Change to a new random meal index
                        child[i] = np.random.randint(0, 100)
                offspring.append(child)
            
            # 3. SELECTION: Combine Parents + Offspring and pick the best (Tournament/Elite)
            combined = pop + offspring
            # Sort by fitness (lowest score is best)
            combined.sort(key=lambda x: self.fitness(x))
            
            # Keep the top 'pop_size' individuals for the next generation
            pop = combined[:pop_size]
            
            # Record the best fitness score to show in the Streamlit graph
            history.append(self.fitness(pop[0]))
            
        # Return the best individual found and the progress history
        return pop[0], history
