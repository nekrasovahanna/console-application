from db_connect import connect  # импорт подключения из отдельного файла
from queries import search_keyword, get_top_movies, search_by_year_and_genre, insert_into_search_query, print_queries
from tabulate import tabulate
# импорт функций поиска

# Запустить подключение
conn = connect()

while True:
    print("""\nЭта программа умеет:\n
        1. Искать по ключевому слову
        2. Искать по году и жанру
        3. Топ-10 популярных запросов 
        4. Выход\n""")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        # Искать по ключевому слову
        keyword = input("Enter keyword: ").strip()
        result = search_keyword(conn, keyword)

        if conn:
            user_query = f'Фильм по ключевому слову {keyword}'
            print(user_query)
            insert_into_search_query(conn, user_query)


        if result:
            print(tabulate(result, headers=['Title', 'Genres', 'Year', 'Runtime', 'Rating'], tablefmt='psql',
                           maxcolwidths=[None]))
        #    for row in result:
        #        print(*row)
        else:
            print("Ничего не найдено.")

    elif choice == "2":
        # Искать по году и жанру
        try:
            year = input("Enter year: ")
            genre = input("Enter genre: ")
            result = search_by_year_and_genre(conn, year, genre)

            if conn:
                user_query = f'Фильм по жанру {genre} и году {year}'
                print(user_query)
                insert_into_search_query(conn, user_query)

            if result:
                print(tabulate(result, headers=['Title', 'Year', 'Genres', 'Runtime', 'Rating'], tablefmt='psql',
                               maxcolwidths=[None]))
                #for row in result:
                    #print(*row)
            else:
                print("Ничего не найдено.")
        except ValueError:
            print("Неверный формат года. Попробуйте снова.")

    elif choice == "3":
     # Топ 10 самых популярных запросов
        if conn:
            try:
                print("Топ 10 запросов")
                result = print_queries(conn)
                if result:
                    print(tabulate(result, headers=['Query', 'Rating'], tablefmt='psql',
                                   maxcolwidths=[None]))

                    #for row in result:
                        #print(*row)
                else:
                    print("Ничего не найдено.")
            except Exception as e:
                print(f"Произошла ошибка: {e}")



    elif choice == "4":
        # Показать топ-5 фильмов перед выходом
        print("\nТоп-5 фильмов с самым высоким рейтингом:")
        top_movies = get_top_movies(conn)
        if top_movies:
            for rank, movie in enumerate(top_movies, start=1):
                print(f"{rank}. {movie['title']} - {movie['rating']}")
        else:
            print("Нет доступных данных для отображения.")

        # Закрыть подключение и выйти из программы
        conn.close()
        print("Подключение закрыто. Выход из программы.")
        break
    else:
        print("Неверный выбор, попробуйте снова.")