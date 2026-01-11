import pandas as pd

def get_clean_data(file_path):
    df = pd.read_csv(file_path)
    # We create a list of all breakfast items, lunch items, etc.
    menu = []
    for cat in ['Breakfast Suggestion', 'Lunch Suggestion', 'Dinner Suggestion', 'Snack Suggestion']:
        unique_meals = df[cat].unique()
        for meal in unique_meals:
            # We find the average price and calories for this specific meal
            stats = df[df[cat] == meal].mean(numeric_only=True)
            menu.append({
                'Item': meal,
                'Category': cat.replace(' Suggestion', ''),
                'Calories': stats['Calories'] / 4,
                'Price_RM': stats['Price_RM'] / 4
            })
    return pd.DataFrame(menu)
