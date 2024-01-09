import streamlit as st
import numpy as np
import pickle
import json

background_image_url = r'C:\Users\Admin\Downloads\flats.jpg'

# Create a div with a background image using custom HTML and CSS
background_image_style = f"""
    <style>
        body {{
            background-image: url("{background_image_url}");
            background-size: cover;
        }}
    </style>
"""
st.markdown(background_image_style, unsafe_allow_html=True)

with open('bangalore_home_prices_model.pickle', 'rb') as f:
        global regressor
        regressor = pickle.load(f)
with open("columns.json", "r") as f:
      global __data_columns
      global __locations
      
      __data_columns = json.load(f)['data_columns']
      __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk


def get_estimated_price(location,bath,bhk,float_sqft):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = bath
    x[1] = bhk
    x[2] = float_sqft
    if loc_index>=0:
        x[loc_index] = 1

    prediction = round(regressor.predict([x])[0],2)
    print(prediction)
    return round(regressor.predict([x])[0],2)

def main():

    st.title("Bangalore Home Price Predictor")

    locations = st.selectbox('Select an option:', __locations)
    bath = st.text_input('How many bathrooms?')
    bhk = st.text_input('How many rooms')
    sqft = st.text_input('Provide Sqft ')
    result =""
    if st.button("Predict"):
        result = get_estimated_price(location=locations,bath=bath,bhk=bhk,float_sqft=sqft)
    st.success("The predicted price is {}".format(result))

if __name__ == "__main__":
    main()