import streamlit
import pandas
import snowflake.connector
import requests
streamlit.title('LAVENDER ORACLE VIBES')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')



streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruiy_choice:
        streamlit.error("Please enter a Choice of fruit..")
   else:
        streamlit.text('Food Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      
except URLError as e:
   streamlit.error()
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit Load List Contains:")
streamlit.dataframe(my_data_rows)

fruit_choice_list = streamlit.text_input('What fruit would you like to add?','Jackfruit')

streamlit.text("Thanks for Adding:"+ fruit_choice_list)
my_cur.execute("INSERT INTO fruit_load_list values ('from streamlit')")

