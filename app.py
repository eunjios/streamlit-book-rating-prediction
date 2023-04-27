import streamlit as st
import pandas as pd
from data_load import context_data_load, context_data_split, context_data_loader, merge_book
from predict import model_load, test

# Setting page config to wide mode
st.set_page_config(layout="wide")


@st.cache_data
def predict():
    # load data and model
    data = context_data_load()
    data = context_data_split(data)
    data = context_data_loader(data)
    model = model_load(data=data)

    predicts = test(model, data)
    test_df = pd.read_csv('data/test_ratings.csv')
    test_df['rating'] = predicts
    test_df = merge_book(test_df)

    return test_df


def print_stars(rating):
    if 9 <= rating:
        return '⭐️⭐️⭐️⭐️⭐️'
    elif 7.5 <= rating < 9:
        return '⭐️⭐️⭐️⭐️'
    elif 5.5 <= rating < 7.5:
        return '⭐️⭐️⭐️'
    elif 3.5 <= rating < 5.5:
        return '⭐️⭐️'
    elif 1.5 <= rating < 3.5:
        return '⭐️'
    else:
        return '🌧️'


def print_string(rating):
    if rating >= 8:
        return "100% your type! Read it right now! 🥰"
    elif 6.5 <= rating < 8:
        return "I recommend this book! 😉"
    elif 5 <= rating < 6.5:
        return "Just try it! 🙂"
    elif 3 <= st.session_state.rating < 5:
        return "Hmm.. I'm not sure.. 🤔"
    else: 
        return "No.. no.. no.. save your time 🤯"


def main():
    test_df = predict()
    st.session_state.rating = 0

    # title
    st.title("📚 Book Rating Prediction")

    # test
    # st.write(test_df)

    # change id and isbn
    st.write("Life is short and there are so many books to read. Just choose your ID and ISBN that you are interested in")
    
    # spacing
    vert_space = '<div style="padding: 18px 5px;"></div>'
    st.markdown(vert_space, unsafe_allow_html=True)

    user_ids = test_df.sort_values('user_id')['user_id'].unique()
    selected_user_id = st.selectbox("Choose your ID", user_ids) # 638

    mask = test_df['user_id'] == selected_user_id
    df = test_df[mask].sort_values('isbn')
    book_isbns = df['isbn']
    selected_book_isbn = st.selectbox("Choose ISBN", 
                                      options=book_isbns, 
                                    #   format_func=lambda x: df[df['isbn']==x]['book_title'].tolist()[0] # format: title
                                      )

    # spacing
    st.markdown(vert_space, unsafe_allow_html=True)

    # print
    st.subheader(f"{df[df['isbn']==selected_book_isbn]['book_title'].tolist()[0].title()}")
    st.write(f"\t Author: {df[df['isbn']==selected_book_isbn]['book_author'].tolist()[0]}")
    st.write(f"\t Publisher: {df[df['isbn']==selected_book_isbn]['publisher'].tolist()[0]}")
    
    # spacing
    st.markdown(vert_space, unsafe_allow_html=True)

    # button
    if st.button("Prediction"):
        st.session_state.rating = 0
        mask = ((test_df['user_id'] == selected_user_id) & (test_df['isbn'] == selected_book_isbn))
        st.session_state.rating = test_df[mask]['rating'].tolist()[0]

    rating = round(st.session_state.rating, 1)
    st.header(f"Rating: {print_stars(rating)} ({rating})" if rating > 0 else "")
    st.subheader(f"{print_string(rating)}" if rating > 0 else "")

main()