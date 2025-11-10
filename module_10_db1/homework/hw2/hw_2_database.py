import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_2_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT phone_id, COUNT(phone_id) FROM table_checkout Group by phone_id ORDER by COUNT(*) DESC LIMIT 3")
        most_popular_3 = cursor.fetchall()
        #print(most_popular_3)

        cursor.execute(
            "SELECT phone_id, COUNT(phone_id) FROM table_checkout Group by phone_id ORDER by COUNT(*) ASC LIMIT 3")
        most_unpopular_3 = cursor.fetchall()
        #print(most_unpopular_3)

        # Телефоны какого цвета чаще всего покупают?
        cursor.execute(
            f"SELECT colour FROM table_phones WHERE id in ("
            f"{most_popular_3[0][0]}, {most_popular_3[1][0]}, {most_popular_3[2][0]})"
        )
        colours = cursor.fetchall()
        #print(colours)
        red_color = 0
        blue_color = 0
        for color in colours:
            #print(color[0])
            if color[0] == "синий":
                blue_color += 1
            elif color[0] == "красный":
                red_color +=1
        if blue_color > red_color:
            print(f"Телефоны синего цвета чаще всего покупают\n"
                  f"В тройке популярных {blue_color} - синих и {red_color} - красных")
        else:
            print(f"Телефоны красного цвета чаще всего покупают\n"
                  f"В тройке популярных {blue_color} - синих и {red_color} - красных")

    #Какие телефоны чаще покупают: красные или синие?
    cursor.execute(f"SELECT colour FROM table_phones WHERE id={most_popular_3[0][0]}")
    pop_colour = cursor.fetchall()
    print(f"Популярный цвет {pop_colour[0][0]}\n"
          f"продано {most_popular_3[0][1]} штук")

    #Какой самый непопулярный цвет телефона?
    cursor.execute(f"SELECT colour FROM table_phones WHERE id={most_unpopular_3[0][0]}")
    unpop_colour = cursor.fetchall()
    print(f"Непопулярный цвет {unpop_colour[0][0]}\n"
          f"продано {most_unpopular_3[0][1]} штук")

