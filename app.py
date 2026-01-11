import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import get_clean_data
from ep_algorithm import EP_Optimizer

st.set_page_config(page_title="My Diet Optimizer")
st.title("🍎 Evolutionary Diet Planner")

# Load the file you uploaded
menu_df = get_clean_data('Food_and_Nutrition_with_Price.csv')

st.sidebar.header("Your Goals")
target_cal = st.sidebar.slider("Target Calories", 1200, 3000, 2000)

if st.button("Find Best Cheap Meal Plan"):
    # Run the algorithm
    opt = EP_Optimizer(menu_df, target_cal)
    best_plan, history = opt.run()
    
    # Show Results
    st.success("Optimization Done!")
    for i, cat in enumerate(['Breakfast', 'Lunch', 'Dinner', 'Snack']):
        items = menu_df[menu_df['Category'] == cat]
        meal = items.iloc[best_plan[i] % len(items)]
        st.write(f"**{cat}**: {meal['Item']} (RM {meal['Price_RM']:.2f})")
    
    # Show the Graph (Task 3 Performance Analysis)
    st.subheader("How the algorithm learned")
    fig, ax = plt.subplots()
    ax.plot(history)
    ax.set_ylabel("Fitness (Cost Score)")
    ax.set_xlabel("Generation")
    st.pyplot(fig)
