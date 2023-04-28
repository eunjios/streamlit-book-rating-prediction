# Streamlit for Book Rating Prediction

![demo file](https://user-images.githubusercontent.com/77034159/235016531-f2b73a9d-4a7b-4916-b12f-8c2eba0a57c4.gif)

## ⚙️ Setting
> *NOTE: `FFM_model.pt` does not exist in this repository. 
You can download it [here](https://drive.google.com/file/d/1dSTjbK63iap1v97FljM2TclHA1Quo6vU/view?usp=share_link).
The file should be located in `saved_model` folder.*
>

## 👀 How to
1. Choose your ID.
2. Choose ISBN.
3. You can check the information of ISBN. (book title, author, and publisher)
4. Click `prediction` button.
5. We predict the rating with user ID and ISBN.

> *NOTE: The prediction is based on `test_ratings.csv`. 
Therefore, the ISBN may not exist for the selected ID. 
It is for fast prediction and can be extended in the future.*
>
<br>

## 🛠️ Trouble Shooting
### 문제 상황
- rating value 뿐만 아니라 해당 index가 함께 출력되는 문제 
    ```python
    st.session_state.rating = test_df[mask]['rating']
    st.header(f"Rating: {print_stars(rating)} ({rating})")
    ```

### 해결 방법
- [Streamlit Documentation](https://docs.streamlit.io/knowledge-base/using-streamlit/hide-row-indices-displaying-dataframe) 확인했으나, 새로운 버전에서는 사용 불가
- `st.session_state.rating` type을 np.array 에서 list type으로 변경하여 rating value에 접근
    ```python
    st.session_state.rating = test_df[mask]['rating'].tolist()[0]
    rating = round(st.session_state.rating, 1)
    st.header(f"Rating: {print_stars(rating)} ({rating})")
    ```