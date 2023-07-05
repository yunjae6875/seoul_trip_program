# import pandas as pd
import sqlite3

conn = sqlite3.connect('food.db')
cursor = conn.cursor()


# food_list_= cursor.execute('UPDATE food_list SET main_dishes = Null where main_dishes = ""')
update_food_qury = 'UPDATE food_list SET main_dishes = "카페/디저트", price="만원 미만" where name = "고양이똥3"'
cursor.execute(update_food_qury)
conn.commit()
food_list = cursor.execute("select * from food_list where name = '고양이똥3'")
food_list = cursor.fetchall()
for i in food_list:
    print(i)

conn.close()
