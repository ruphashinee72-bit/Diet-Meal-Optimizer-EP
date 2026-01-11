import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import get_clean_data
from ep_algorithm import EP_Optimizer

st.set_page_config(page_title="Diet Optimizer - Evolutionary Programming", layout="wide")
st.title("🍎 Evolutionary Diet Meal Planner")
st.markdown("This app uses **Evolutionary Programming (EP)** to find the cheapest meal plan that meets your calorie goals.")

# --- STEP 1: LOAD DATA ---
menu_df = get_clean_data('Food_and_Nutrition_with_Price.csv')

# --- STEP 2: SIDEBAR PARAMETERS (Task 5 requirement) ---
st.sidebar.header("🎯 Health Goals")
target_cal = st.sidebar.slider("Daily Calorie Target", 1200, 3500, 2000)

st.sidebar.header("⚙️ Algorithm Parameters")
# These allow you to "dynamically explore parameters" as per the instructions
pop_size = st.sidebar.slider("Population Size", 10, 200, 50)
gens = st.sidebar.slider("Number of Generations", 10, 500, 100)
mut_rate = st.sidebar.slider("Mutation Probability", 0.1, 1.0, 0.3)

# --- STEP 3: RUN OPTIMIZATION ---
if st.button("🚀 Start Optimization"):
    # Create the optimizer
    opt = EP_Optimizer(menu_df, target_cal)
    
    # Run the algorithm using the sliders from the sidebar
    # Note: Make sure your EP_Optimizer.run method accepts these arguments!
    best_plan, history = opt.run(generations=gens, pop_size=pop_size)
    
    st.success("Optimization Complete!")
    
    # Create two columns for the layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Selected Meal Plan")
        total_p = 0
        total_c = 0
        for i, cat in enumerate(['Breakfast', 'Lunch', 'Dinner', 'Snack']):
            items = menu_df[menu_df['Category'] == cat]
            meal = items.iloc[best_plan[i] % len(items)]
            st.write(f"**{cat}**: {meal['Item']}")
            st.caption(f"Price: RM {meal['Price_RM']:.2f} | Calories: {meal['Calories']:.0f} kcal")
            total_p += meal['Price_RM']
            total_c += meal['Calories']
        
        st.divider()
        st.metric("Total Cost", f"RM {total_p:.2f}")
        st.metric("Total Calories", f"{total_c:.0f} kcal", f"{total_c - target_cal:.0f} from target")

    with col2:
        # Task 3: Performance Analysis Visualization
        st.subheader("📈 Convergence Analysis")
        fig, ax = plt.subplots()
        ax.plot(history, color='red', linewidth=2)
        ax.set_title("Fitness Score over Generations")
        ax.set_ylabel("Fitness (Price + Penalty)")
        ax.set_xlabel("Generation")
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
        st.info("The graph shows how the algorithm minimizes the cost and calorie error over time.")
