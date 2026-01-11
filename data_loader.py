import pandas as pd

def get_clean_data(file_path):
    df = pd.read_csv(file_path)
    
    menu = []
    # Mapping the columns from your specific dataset
    categories = {
        'Breakfast Suggestion': 'Breakfast',
        'Lunch Suggestion': 'Lunch',
        'Dinner Suggestion': 'Dinner',
        'Snack Suggestion': 'Snack'
    }
    
    for col, cat_name in categories.items():
        unique_meals = df[col].unique()
        for meal in unique_meals:
            subset = df[df[col] == meal]
            
            # Extracting averages and dividing by 4 since CSV values are daily totals
            avg_calories = subset['Calories'].mean() / 4
            avg_protein = subset['Protein'].mean() / 4
            avg_fat = subset['Fat'].mean() / 4
            avg_price = subset['Price_RM'].mean() / 4
            
            menu.append({
                'Item': meal,
                'Category': cat_name,
                'Calories': avg_calories,
                'Protein': avg_protein,
                'Fat': avg_fat,
                'Price_RM': avg_price
            })
            
    return pd.DataFrame(menu)
