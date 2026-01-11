import pandas as pd

def get_clean_data(file_path):
    # Load your group's CSV file
    df = pd.read_csv(file_path)
    
    menu = []
    # These are the columns from your specific CSV
    categories = {
        'Breakfast Suggestion': 'Breakfast',
        'Lunch Suggestion': 'Lunch',
        'Dinner Suggestion': 'Dinner',
        'Snack Suggestion': 'Snack'
    }
    
    for col, cat_name in categories.items():
        # Get every unique food name in that column
        unique_meals = df[col].unique()
        
        for meal in unique_meals:
            # Look at all rows where this meal appears to find its average stats
            # This links your individual items back to your original CSV data
            subset = df[df[col] == meal]
            
            # We divide by 4 because the CSV values are for the WHOLE day (4 meals)
            avg_calories = subset['Calories'].mean() / 4
            avg_price = subset['Price_RM'].mean() / 4
            
            menu.append({
                'Item': meal,
                'Category': cat_name,
                'Calories': avg_calories,
                'Price_RM': avg_price
            })
            
    # Return a nice clean table of single food items
    return pd.DataFrame(menu)
