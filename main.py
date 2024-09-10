import streamlit as st
import streamlit_option_menu
from streamlit_extras.stoggle import stoggle
from processing import preprocess
from processing.display import Main

# Setting the wide mode as default
st.set_page_config(layout="wide")
# Adding background image
bg_image_url = "https://t3.ftcdn.net/jpg/02/97/91/38/240_F_297913876_pxLCVBrLEyznyqdHvNpKmNRPvYWoqlEW.jpg"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({bg_image_url});
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

displayed = []

if 'movie_number' not in st.session_state:
    st.session_state['movie_number'] = 0

if 'selected_movie_name' not in st.session_state:
    st.session_state['selected_movie_name'] = ""

if 'user_menu' not in st.session_state:
    st.session_state['user_menu'] = ""


def main():
    
    def initial_options():
        # To display menu
        st.session_state.user_menu = streamlit_option_menu.option_menu(
            menu_title='Looking for Something? ( ఠ ͟ʖ ఠ)',
            options=['Get Similar Movies', 'Get THIS Movie Details', 'A-Z Movies List'],
            icons=['film', 'film', 'film'],
            menu_icon='list',
            orientation="horizontal",
        )

        if st.session_state.user_menu == 'Get Similar Movies':
            recommend_display()

        elif st.session_state.user_menu == 'Get THIS Movie Details':
            display_movie_details()

        elif st.session_state.user_menu == 'A-Z Movies List':
            paging_movies()

    def recommend_display():

        st.title('MovieFinder')

        selected_movie_name = st.selectbox(
            'Choose/Type a Movie...', new_df['title'].values
        )

        rec_button = st.button('GET Recommedations')
        if rec_button:
            st.session_state.selected_movie_name = selected_movie_name
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tags.pkl',"are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_genres.pkl',"on the basis of genres are")
            recommendation_tags(new_df, selected_movie_name,
                                r'Files/similarity_tags_tprduction_comp.pkl',"from the same production company are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_keywords.pkl',"on the basis of keywords are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tcast.pkl',"on the basis of cast are")

    def recommendation_tags(new_df, selected_movie_name, pickle_file_path,str):

        movies, posters = preprocess.recommend(new_df, selected_movie_name, pickle_file_path)
        st.subheader(f'Best Recommendations {str}...')

        rec_movies = []
        rec_posters = []
        cnt = 0
        # Adding only 5 uniques recommendations
        for i, j in enumerate(movies):
            if cnt == 5:
                break
            if j not in displayed:
                rec_movies.append(j)
                rec_posters.append(posters[i])
                displayed.append(j)
                cnt += 1

        # Columns to display informations of movies i.e. movie title and movie poster
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(rec_movies[0])
            st.image(rec_posters[0])
        with col2:
            st.text(rec_movies[1])
            st.image(rec_posters[1])
        with col3:
            st.text(rec_movies[2])
            st.image(rec_posters[2])
        with col4:
            st.text(rec_movies[3])
            st.image(rec_posters[3])
        with col5:
            st.text(rec_movies[4])
            st.image(rec_posters[4])

    def display_movie_details():
        selected_movie_name = st.session_state.selected_movie_name
        info = preprocess.get_details(selected_movie_name)

        if info is None:
            st.error(f"Details for movie '{selected_movie_name}' not found.")
            return  # Exit the function if info is None

        with st.container():
            image_col, text_col = st.columns((1, 2))
            with image_col:
                st.text('\n')
                st.image(info[0])

            with text_col:
                st.text('\n')
                st.text('\n')
                st.title(selected_movie_name)
                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Rating")
                    st.write(info[8])
                with col2:
                    st.text("No. of ratings")
                    st.write(info[9])
                with col3:
                    st.text("Runtime")
                    st.write(info[6])

                st.text('\n')
                st.write("Overview")
                st.write(info[3], wrapText=False)
                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Release Date")
                    st.text(info[4])
                with col2:
                    st.text("Budget")
                    st.text(info[1])
                with col3:
                    st.text("Revenue")
                    st.text(info[5])

                st.text('\n')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text("Genres")
                    genre_str = " . ".join(info[2]) if info[2] else "N/A"
                    st.write(genre_str)

                with col2:
                    st.text("Available in")
                    languages_str = " . ".join(info[13]) if info[13] else "N/A"
                    st.write(languages_str)

                with col3:
                    st.text("Directed by")
                    st.text(info[12][0] if info[12] else "N/A")
                st.text('\n')

        # Displaying information of casts
        st.header('Cast')
        cnt = 0
        urls = []
        bio = []
        for i in info[14]:
            if cnt == 5:
                break
            url, biography = preprocess.fetch_person_details(i)
            urls.append(url)
            bio.append(biography)
            cnt += 1

        # Check if we have enough URLs and bio data
        if len(urls) >= 5 and len(bio) >= 5:
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.image(urls[0])
                stoggle("Show More", bio[0])
            with col2:
                st.image(urls[1])
                stoggle("Show More", bio[1])
            with col3:
                st.image(urls[2])
                stoggle("Show More", bio[2])
            with col4:
                st.image(urls[3])
                stoggle("Show More", bio[3])
            with col5:
                st.image(urls[4])
                stoggle("Show More", bio[4])
        else:
            st.error("Not enough cast information available.")
    

    def paging_movies():
        # To create pages functionality using session state.
        max_pages = movies.shape[0] / 10
        max_pages = int(max_pages) - 1

        col1, col2, col3 = st.columns([1, 9, 1])

        with col1:
            st.text("Previous page")
            prev_btn = st.button("Prev")
            if prev_btn:
                if st.session_state['movie_number'] >= 10:
                    st.session_state['movie_number'] -= 10

        with col2:
            new_page_number = st.slider("Jump to page number", 0, max_pages, st.session_state['movie_number'] // 10)
            st.session_state['movie_number'] = new_page_number * 10

        with col3:
            st.text("Next page")
            next_btn = st.button("Next")
            if next_btn:
                if st.session_state['movie_number'] + 10 < len(movies):
                    st.session_state['movie_number'] += 10

        display_all_movies(st.session_state['movie_number'])

    def display_all_movies(start):

        i = start
        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

        st.session_state['page_number'] = i

    with Main() as bot:
        bot.main_()
        new_df, movies, movies2 = bot.getter()
        initial_options()

    # Adding footer
    st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        # background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        # color: #333;
    }
    </style>
    <div class="footer">
        Made by Srijan Arya | <a href="https://github.com/Srijan-Arya" target="_blank">Github</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
