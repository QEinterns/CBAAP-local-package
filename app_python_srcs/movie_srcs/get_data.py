import wikipedia

def get_data(movie):
    print("movie from app.py",movie)
    movie_name = wikipedia.search(movie+" (film)", results=5, suggestion=True)
    #print(movie_name[0])
    page = wikipedia.WikipediaPage(movie_name[0][0])
    print(page.section("Plot"))

    return page.section("Plot")