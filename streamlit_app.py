import streamlit
import pandas
import snowflake.connector
import requests

streamlit.title('INDIA MART')

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

def get_fruity_vice_data(this_fruit_choice):
   streamlit.text('Food Information from : https://fruityvice.com/api/fruit/'+ this_fruit_choice)
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
   
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
        streamlit.error("Please enter a Choice of fruit..")
   else:
        back_from_function=get_fruity_vice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except:
   streamlit.text("Something went wrong")

def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
       my_cur.execute("INSERT INTO fruit_load_list values ('"+new_fruit+"')")
       return "Thanks for Adding:"+ new_fruit

def fruit_list():
   with my_cnx1.cursor() as my_cur_LIST:
      my_cur_LIST.execute("SELECT * from fruit_load_list")
      my_data_rows = my_cur_LIST.fetchall()
      streamlit.header("The Fruit Load List Contains:")  
      return streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=insert_row_snowflake(add_my_fruit)
   my_cnx.close()
   streamlit.text(back_from_function)

if streamlit.button('Get Fruit List'):
   my_cnx1 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function1=fruit_list()
   my_cnx1.close()
   streamlit.text(back_from_function1)



