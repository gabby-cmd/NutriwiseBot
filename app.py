import pandas as pd
import streamlit as st

# Load the CSV file into a Pandas DataFrame
@st.cache_data
def load_data():
    file_path = './food 2.csv'  # Ensure this matches the uploaded file's name
    data = pd.read_csv(file_path)
    return data

# Load the data from the uploaded CSV file
food_data = load_data()

# Streamlit App Title
st.title("Nutriwise Bot")

# Input boxes for user's height and weight
st.header("Personalized Nutrition Information")
height = st.number_input("Enter your height (in cm):", min_value=50, max_value=300, step=1)
weight = st.number_input("Enter your weight (in kg):", min_value=10, max_value=300, step=1)

# Input for calorie consumption
st.header("Calorie and Nutrition Assistant")
calories_input = st.number_input("Enter the calories you wish to consume per meal:", min_value=0, step=1)

# User Query
user_query = st.text_input("Ask me a nutrition question:")

# Process user query
if st.button("Submit"):
    # Respond to questions about calories for specific foods
    if "calories" in user_query.lower():
        try:
            # Attempt to extract the food name after "is a"
            food_name = user_query.lower().split("is a")[1].strip("?").strip()
            food_info = food_data[food_data['Food'].str.lower() == food_name]

            if not food_info.empty:
                calories = food_info.iloc[0]['Calories']
                protein = food_info.iloc[0]['Protein']
                fat = food_info.iloc[0]['Fat']
                carbs = food_info.iloc[0]['Carbs']
                st.write(f"**{food_name.capitalize()}** contains:")
                st.write(f"- Calories: {calories}")
                st.write(f"- Protein: {protein} g")
                st.write(f"- Fat: {fat} g")
                st.write(f"- Carbohydrates: {carbs} g")
            else:
                st.write("Sorry, I couldn't find that food in the database. Please try another!")
        except IndexError:
            st.write("Sorry, I couldn't extract the food name from your question. Please try asking in a different format.")

    # Respond to glucose control
    elif "how to control glucose" in user_query.lower() or "blood sugar spikes" in user_query.lower():
        st.write("You can control glucose by choosing foods that have a low impact on blood sugar levels, avoiding artificial sugars, and minimizing chemically processed foods.")

    # Protein Calculator
    elif "how to calculate protein" in user_query.lower():
        if height and weight:
            protein_required = weight * 0.8  # Example formula for protein requirement
            st.write(f"Based on your height and weight, you need approximately {protein_required:.2f} grams of protein per day.")
            st.write("Foods high in protein include chicken breast, eggs, lentils, tofu, and Greek yogurt.")
        else:
            st.write("Please enter your height and weight to calculate protein requirements!")

    # General fallback response
    else:
        st.write("I'm not sure how to answer that. Please try rephrasing your question or ask about a specific food or nutrition topic.")

# Display food data in a table for user reference
st.header("Explore Food Nutrition Data")
st.write("Here is the nutrition data from the database:")
st.dataframe(food_data)
