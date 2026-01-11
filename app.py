import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import get_clean_data
from ep_algorithm import EP_Optimizer

st.set_page_config(page_title="Diet Optimizer - Evolutionary Programming", layout="wide")
st.title("🍎 Evolutionary Diet Meal Planner")
st.markdown("This app uses **Evolutionary Programming (EP)** to find the cheapest meal plan that meets your specific nutritional needs.")

# --- STEP 1: LOAD DATA ---
menu_df = get_clean_data('Food_and_Nutrition_with_Price.csv')

# --- STEP 2: SIDEBAR PARAMETERS ---
st.sidebar.header("🎯 Nutritional Targets")
target_cal = st.sidebar.slider("Target Calories", 1200, 3500, 2000)
# Adding these satisfies your objective of 'Nutritional Requirements'
target_prot = st.sidebar.slider("Min Protein (g)", 40, 200, 100)
target_fat = st.sidebar.slider("Max Fat (g)", 20, 150, 70)

st.sidebar.header("⚙️ Algorithm Parameters")
pop_size = st.sidebar.slider("Population Size", 10, 200, 50)
gens = st.sidebar.slider("Number of Generations", 10, 500, 100)
mut_rate = st.sidebar.slider("Mutation Probability", 0.1, 1.0, 0.3)

# --- STEP 3: RUN OPTIMIZATION ---
if st.button("🚀 Start Optimization"):
    # Pass the new nutritional targets to your optimizer
    opt = EP_Optimizer(menu_df, target_cal, target_prot, target_fat)
    
    # Run algorithm
    best_plan, history = opt.run(generations=gens, pop_size=pop_size, mut_rate=mut_rate)
    
    st.success("Optimization Complete!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Selected Meal Plan")
        # Initialize totals
        total_price = 0
        total_cal = 0
        total_prot = 0
        total_fat = 0
        
        for i, cat in enumerate(['Breakfast', 'Lunch', 'Dinner', 'Snack']):
            items = menu_df[menu_df['Category'] == cat]
            meal = items.iloc[best_plan[i] % len(items)]
            
            st.write(f"**{cat}**: {meal['Item']}")
            st.caption(f"Prot: {meal['Protein']:.1f}g | Fat: {meal['Fat']:.1f}g | Price: RM {meal['Price_RM']:.2f}")
            
            # Sum up the totals
            total_price += meal['Price_RM']
            total_cal += meal['Calories']
            total_prot += meal['Protein']
            total_fat += meal['Fat']
        
        st.divider()
        
        # Displaying 4 metrics to show multi-objective balance
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Cost", f"RM {total_price:.2f}")
        m2.metric("Calories", f"{total_cal:.0f}")
        m3.metric("Protein", f"{total_prot:.1f}g")
        m4.metric("Fat", f"{total_fat:.1f}g")

    with col2:
        st.subheader("📈 Convergence Analysis")
        fig, ax = plt.subplots()
        ax.plot(history, color='red', linewidth=2)
        ax.set_title("Optimization Progress (Fitness Score)")
        ax.set_ylabel("Penalty + Cost (Lower is Better)")
        ax.set_xlabel("Generation")
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
        st.info("EP minimizes a 'Fitness Score' which is a combination of Total Price and penalties for missing nutrition targets.")
