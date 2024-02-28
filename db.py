import psycopg
import os
from dotenv import load_dotenv

load_dotenv('.env')

connection_URI = os.getenv("CONNECTION_URI")


def access_database_content(game_name):
    with psycopg.connect(connection_URI) as conn:
        try:
            with conn.cursor() as cur:
                # checking if the game name exists in database or not
                cur.execute("""
                    SELECT COUNT(*) FROM content_based 
                    WHERE "Title" = %s;
                """, [game_name])

                exist_cnt = cur.fetchone()[0]
                if exist_cnt != 1:
                    conn.close()
                    return

                cur.execute(""" 
                    SELECT "r1", "r2", "r3", "r4", "r5" FROM content_based WHERE "Title" = %s;
                """, [game_name])

                recom_indexes = cur.fetchone()

                content_based_data = []
                for ind in recom_indexes:
                    cur.execute("""
                        SELECT "Title", "Original Price", "Game Description", "app_id"  FROM content_based 
                        WHERE "Index" = %s;
                    """, [ind])

                    row_data = cur.fetchone()

                    content_based_data.append({
                        "Name": row_data[0],
                        "Price": row_data[1],
                        "Description": row_data[2],
                        'Image': 'https://cdn.akamai.steamstatic.com/steam/apps/' + str(row_data[3]) + '/header.jpg',
                        'Steam': 'https://store.steampowered.com/app/' + str(row_data[3])
                    })

                conn.commit()
                return content_based_data

        except Exception as err:
            print("Oops! An exception has occurred:", err)
            print("Exception TYPE:", type(err))

        finally:
            conn.close()


def access_database_chosen(chosen_game_name):
    with psycopg.connect(connection_URI) as conn:
        try:
            with conn.cursor() as cur:
                # checking if the game name exists in database or not
                cur.execute("""
                    SELECT COUNT(*) FROM content_based 
                    WHERE "Title" = %s;
                """, [chosen_game_name])

                exist_cnt = cur.fetchone()[0]
                if exist_cnt != 1:
                    conn.close()
                    return

                cur.execute("""
                    SELECT "Original Price", "Game Description", "app_id"  FROM content_based 
                    WHERE "Title" = %s;
                """, [chosen_game_name])

                chosen_one_row = cur.fetchone()

                return [{
                    'Image': 'https://cdn.akamai.steamstatic.com/steam/apps/' + str(chosen_one_row[2]) + '/header.jpg',
                    "Price": chosen_one_row[0],
                    "Description": chosen_one_row[1],
                    'Steam': 'https://store.steampowered.com/app/' + str(chosen_one_row[2])
                }]

        except Exception as err:
            print("Oops! An exception has occurred:", err)
            print("Exception TYPE:", type(err))

        finally:
            conn.close()


def access_database_collaborative(game_name):
    with psycopg.connect(connection_URI) as conn:
        try:
            with conn.cursor() as cur:
                # checking if the game name exists in database or not
                cur.execute("""
                    SELECT COUNT(*) FROM collab_table 
                    WHERE "Title" = %s;
                """, [game_name])

                exist_cnt = cur.fetchone()[0]
                if exist_cnt != 1:
                    conn.close()
                    return

                cur.execute(""" 
                    SELECT "r1", "r2", "r3", "r4", "r5" FROM collab_table WHERE "Title" = %s;
                """, [game_name])

                recom_indexes = cur.fetchone()

                content_based_data = []
                for ind in recom_indexes:
                    cur.execute("""
                        SELECT "Title", "Original Price", "Game Description", "app_id"  FROM collab_table 
                        WHERE "Index" = %s;
                    """, [ind])

                    row_data = cur.fetchone()

                    content_based_data.append({
                        "Name": row_data[0],
                        "Price": row_data[1],
                        "Description": row_data[2],
                        'Image': 'https://cdn.akamai.steamstatic.com/steam/apps/' + str(row_data[3]) + '/header.jpg',
                        'Steam': 'https://store.steampowered.com/app/' + str(row_data[3])
                    })

                conn.commit()
                return content_based_data

        except Exception as err:
            print("Oops! An exception has occurred:", err)
            print("Exception TYPE:", type(err))

        finally:
            conn.close()

