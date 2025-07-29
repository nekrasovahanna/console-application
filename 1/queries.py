from db_connect import connect

select_movies = """SELECT title, year, genres, runtime, `imdb.rating` FROM movies"""

def search_keyword(conn, keyword):
    query = f"""{select_movies} WHERE title LIKE %s OR plot LIKE %s LIMIT 10;"""
    keyword_param = f"%{keyword}%"
    cursor = conn.cursor()
    cursor.execute(query, (keyword_param, keyword_param))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_top_movies(conn):
    cursor = conn.cursor()
    query = """
        SELECT title, `imdb.rating`
        FROM movies 
        ORDER BY `imdb.rating` DESC 
        LIMIT 5
    """
    cursor.execute(query)
    # Возвращаем список словарей для удобного отображения
    return [{"title": row[0], "rating": row[1]} for row in cursor.fetchall()]

def search_by_year_and_genre(conn, year, genre):
    query = f"""{select_movies} where genres like %s AND year = %s LIMIT 10;"""
    year_param = f"{year}"
    genre_param = f"%{genre}%"
    cursor = conn.cursor()
    cursor.execute(query, ( genre_param, year_param))
    result = cursor.fetchall()
    cursor.close()
    return result

def insert_into_search_query(conn, user_query):
    try:
        query = f"""INSERT INTO search_query (query) VALUES (%s);"""
        cursor = conn.cursor()
        cursor.execute(query, (user_query,))
        conn.commit()
        result = cursor.lastrowid
        cursor.close()
        return result
    except mysql.connector.Error as e:
        print(f"Error inserting query: {e}")
        return None



def print_queries(conn):
    query = f"""SELECT `query`, count(`query`) AS count_q FROM search_query GROUP BY `query` ORDER BY count_q DESC LIMIT 10;"""
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result




# Подключение к базе данных
conn = connect()