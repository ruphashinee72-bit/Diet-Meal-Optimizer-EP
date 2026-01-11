import pandas as pd

def get_clean_data(file_path):
    # Load your group's CSV file
    df = pd.read_csv(file_path)
    
    menu = []
    # Mapping the CSV columns to simple names
    categories = {
        'Breakfast Suggestion': 'Breakfast',
        'Lunch Suggestion': 'Lunch',
        'Dinner Suggestion': 'Dinner',
        'Snack Suggestion': 'Snack'
    }
    
    for col, cat_name in categories.items():
        # Get every unique food name in that category (e.g., all unique Breakfasts)
        unique_meals = df[col].unique()
        
        for meal in unique_meals:
            # Find all rows where this specific meal was eaten
            subset = df[df[col] == meal]
            
            # We calculate the average and divide by 4 because the 
            # original CSV values represent the total for the WHOLE day.
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
            
    # Return the processed menu as a clean DataFrame
    return pd.DataFrame(menu)
