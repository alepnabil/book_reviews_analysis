import streamlit as st
import mysql.connector
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from db_conn import mydb
import altair as alt
import plotly.graph_objs as go
import numpy as np 
import requests
import seaborn as sns
from book_intro import *



def main_page_layout(theme_selected):

        
        
        first_col_width=100
        sec_col_width=100
        third_col_width=100
        fourth_col_width=100
        col1,col2,col3,col4= st.columns([first_col_width,sec_col_width,third_col_width,fourth_col_width])

        if theme_selected=='Social contract':
                st.text_area(f'This the page for {theme_selected} theme',social_contract_theme,height=100)
        elif theme_selected=='Communism':
                st.text_area(f'This the page for {theme_selected} theme',communism_theme,height=100)
        elif theme_selected=='Utilitarianism':
                st.text_area(f'This the page for {theme_selected} theme',utilitarianism_theme,height=100)

        def get_count_of_books(theme_selected):
                cursor = mydb.cursor()
                query = f"""
                        select
                        count(distinct book_name) 
                        from book_dim_table
                        where book_theme='{theme_selected}'
                """
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count
        
        #to display the number of books depending on its category
        def get_review_count(theme_selected):
                cursor = mydb.cursor()
                query = f"""
                
                    select
                        count(*)
                        from review_fact_table rf 
                        join book_dim_table bd
                        on rf.book_id=bd.book_id
                        where bd.book_theme='{theme_selected}'
                """
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count

        def get_author_review_count(theme_selected):
                cursor = mydb.cursor()
                query = f"""
                      select
                        count(*)
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rf.review_id=rd.review_id

                        join book_dim_table bd
                        on rf.book_id=bd.book_id

                        where bd.book_theme='{theme_selected}' and rd.author in (TRUE,1)
                """
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count

        def get_non_author_review_count(theme_selected):
                cursor = mydb.cursor()
                query = f"""
                        select
                        count(*)
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rf.review_id=rd.review_id

                        join book_dim_table bd
                        on rf.book_id=bd.book_id

                        where bd.book_theme='{theme_selected}' and rd.author in (False,0)
                """
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count


        book_count=get_count_of_books(theme_selected)
        review_count = get_review_count(theme_selected)
        author_review_count=get_author_review_count(theme_selected)
        non_author_review_count=get_non_author_review_count(theme_selected)

        #show the metric
        col1.metric(label='Number of books',value=book_count)
        col2.metric(label='Number of reviews',value=review_count)
        col3.metric(label='Number of author reviews',value=author_review_count)
        col4.metric(label='Number of author reviews',value=non_author_review_count)


       
        def get_sentiment_percentage_by_book(theme_selected):
                       
                        cursor = mydb.cursor()
                        query = f"""
                                                
                        select
                        bd.book_name,
                        rf.sentiment,
                        count(*)*100 / SUM(count(*)) over (partition by rf.book_name) as sentiment_percentage
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rf.review_id=rd.review_id

                        join book_dim_table bd
                        on rf.book_id=bd.book_id

                        where bd.book_theme='{theme_selected}'

                        group by bd.book_name,rf.sentiment

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['book_name','sentiment','sentiment_percentage'])
                        data['sentiment_percentage'] = data['sentiment_percentage'].astype(float)

                        return data


        sentiment_percentage_by_book_table=get_sentiment_percentage_by_book(theme_selected)


        graph_col=st.columns([1,1],gap='large')
        with graph_col[0]:
                chart = alt.Chart(sentiment_percentage_by_book_table,width=550,height=500).mark_bar().encode(
                x=alt.X('sentiment_percentage:Q', stack='normalize',title='Percentage (%)'),
                y=alt.Y('book_name:N',title='Books'),
                color=alt.Color('sentiment:N', scale=alt.Scale(scheme='set1'),title='Sentiments'),
                tooltip=[
                        alt.Tooltip('book_name:N', title='Book'),
                        alt.Tooltip('sentiment:N', title='Sentiment'),
                        alt.Tooltip('sentiment_percentage:Q', title='Percentage', format='.2f') 
                ]
                ).properties(title='Books sentiment percentage')

                st.altair_chart(chart)


        def get_ratings_percetange_by_book_bubble(theme_selected):
                        
                        cursor = mydb.cursor()
                        query = f"""
                                                
                        select
                        bd.book_name,
                        rf.sentiment,
                        rf.ratings_given_out_of_5,
                        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY rf.ratings_given_out_of_5) AS percentage
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rf.review_id=rd.review_id

                        join book_dim_table bd
                        on rf.book_id=bd.book_id

                        where bd.book_theme='{theme_selected}'

                        group by bd.book_name,rf.ratings_given_out_of_5,rf.sentiment


                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['book_name','sentiment','ratings','ratings_given_percentage'])
                        data['ratings_given_percentage']=data['ratings_given_percentage'].astype(float)
                        return data
        
        with graph_col[1]:
                sentiments=['Positive','Neutral','Negative']
                selected_sentiment = st.selectbox("Select Sentiment", sentiments)
                selected_sentiment=selected_sentiment.lower()
                ratings_percentage_by_book_table_bubble=get_ratings_percetange_by_book_bubble(theme_selected)
                filtered_data = ratings_percentage_by_book_table_bubble[ratings_percentage_by_book_table_bubble['sentiment'] == selected_sentiment]
                opacity_vals = filtered_data['ratings_given_percentage'].apply(lambda x: x / 100.0 * 0.8 + 0.2)

                
                fig = px.scatter(filtered_data, x="ratings", y="ratings_given_percentage", size="ratings_given_percentage", 
                                 color="book_name", hover_data=["ratings_given_percentage"],
                                 size_max=45,width=700,title='Ratings given by reviewer grouped by sentiments',
                                 labels={'book_name':'Book name','ratings':'Ratings','ratings_given_percentage':'Percentage'})

                # Set the layout
                fig.update_layout(
                        xaxis_title="Ratings",
                        yaxis_title="Sentiment %",
                        xaxis=dict(range=[0, 5])
                        )

                        # Display the bubble chart
                st.caption('_0 = No ratings were given_')
                st.plotly_chart(fig)





        

        def get_avg_ratings_by_book(theme_selected):
                        
            

                        cursor = mydb.cursor()
                        query = f"""
                                                
                        SELECT
                        bd.book_name,
                        CASE rd.author
                        WHEN 0 THEN 'Non author'
                        WHEN 1 THEN 'Author'
                        ELSE 'unknown'
                        END AS author_type,
                        AVG(ratings_given_out_of_5) AS avg_comp
                        FROM review_fact_table rf
                        JOIN book_dim_table bd ON rf.book_id=bd.book_id
                        JOIN reviewer_dim_table rd ON rd.review_id=rf.review_id
                        WHERE bd.book_theme='{theme_selected}' AND rd.author IN (0,1)
                        GROUP BY 1,2



                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['book_name','author','average_ratings'])

                        return data

        avg_ratings_by_book_table=get_avg_ratings_by_book(theme_selected)

        with graph_col[0]:
                
                fig = px.bar(
                        avg_ratings_by_book_table,
                        title='Books average ratings',
                        x='book_name',
                        y='average_ratings',
                        color='author',
                        barmode='group',
                        text='average_ratings',
                        labels={
                        'book_name': 'Book',
                        'average_ratings': 'Average rating',
                        'author': 'Author',
                        },
                )
                fig.update_layout(
                        margin=dict(l=20, r=20, t=30, b=0),
                        width=550,
                        height=450,
                        legend=dict(x=1, y=1.0, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'),

                )
                st.plotly_chart(fig, theme='streamlit')

        with graph_col[1]:
                def get_language_percentage_by_book(theme_selected):
                
                        cursor = mydb.cursor()
                        query = f"""
                        
                                with t3 as (select 
                                                count(*) lang_count,
                                                language
                                                from review_fact_table rf
                                                join book_dim_table bd
                                                on rf.book_id=bd.book_id
                                                where book_theme='{theme_selected}'
                                                group by  language
                                                order by lang_count DESC
                                                LIMIT 5
                                        )
                                SELECT
                                        language,
                                        (lang_count/ (SELECT sum(lang_count) FROM t3) * 100 ) as percentage
                                from t3

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['language','language_percentage'])
                        return data

                language_percentage_by_book=get_language_percentage_by_book(theme_selected)

                
                piechart= px.pie(language_percentage_by_book, 
                                values='language_percentage',
                                names='language',
                                title='Language distribution',
                                labels= {'language': 'Language',
                                'language_percentage': 'Percentage % '
                                })
                piechart.update_layout(margin=dict(l=20, r=20, t=30, b=0),width=10,height=400)
                st.plotly_chart(piechart, use_container_width=True)

        with graph_col[0]:
                
            

                def get_review(theme_selected):
                        
                        stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content

                        stopwords = set(stopwords_list.decode().splitlines()) 


                        cursor = mydb.cursor()
                        query = f"""
                                        
                                        SELECT
                                        rf.review,
                                        rf.sentiment
                                        FROM review_fact_table rf
                                        JOIN book_dim_table bd ON rf.book_id=bd.book_id
                                        JOIN reviewer_dim_table rd ON rd.review_id=rf.review_id
                                        WHERE bd.book_theme='{theme_selected}' and rf.language='en'

                                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['review','sentiment'])
                        data['review']=data['review'].str.lower().apply(lambda x : ' '.join(review for review in x.split() if review not in stopwords))

                        return data

           
                review_text_table=get_review(theme_selected)
                temp_review=''.join(review_text_table['review'])

                st.subheader("Wordcloud")
                wordcloud = WordCloud(background_color='white').generate(temp_review)

                plt.figure(figsize=(10,10))
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.show()
                st.pyplot()

                st.subheader("Word frequency")
                def words_frequency(dataframe):

                                word_frequency=pd.Series(dataframe['review']).str.split(expand=True).stack().value_counts()
                                                        
                                plt.figure(figsize=(10,12.5))
                                word_frequency[2:40].plot(kind='barh')
                                plt.xlabel('Word frequency')
                                plt.ylabel('Words')
                                st.pyplot()

                words_frequency(review_text_table)
        
        def get_total_likes_comments(theme_selected):
                        cursor = mydb.cursor()
                        query = f"""
                        
                        SELECT
                        rf.book_name,
                        sum(rf.review_likes) total_likes,
                        sum(rf.review_comments) total_comments
                        FROM
                        review_fact_table rf
                        JOIN
                        book_dim_table bd ON rf.book_id = bd.book_id
                        WHERE
                        bd.book_theme = '{theme_selected}' 
                        group by 1 

                        

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['book_name','total_likes','total_comments'])

                        
                        return data

        books_total_likes_comments_table=get_total_likes_comments(theme_selected)



        with graph_col[1]:
              
                fig = px.pie(books_total_likes_comments_table, values='total_likes', names='book_name', 
                        hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel,
                        width=600,height=500,title='Total review likes',
                        labels={'book_name':'Book',
                                'total_likes':'Total likes'})

                fig.update_traces(textinfo='percent', pull=[0.1]*len(books_total_likes_comments_table))

                st.plotly_chart(fig)

        with graph_col[1]:
             
                fig = px.pie(books_total_likes_comments_table, values='total_comments', names='book_name', 
                        hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel,
                        width=600, height=500,title='Total review comments',
                        labels={'book_name':'Book',
                                'total_comments':'Total comments'})

                fig.update_traces(textinfo='percent', pull=[0.1]*len(books_total_likes_comments_table))

                st.plotly_chart(fig)


                

        def get_non_author_reviews(theme_selected):
        
                        cursor = mydb.cursor()
                        query = f"""
                        
                        select
                                        rf.name,
                                        rf.review,
                                        rf.ratings_given_out_of_5,
                                        rf.review_likes,
                                        rf.review_comments,
                                        rf.sentiment
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rd.name = rf.name and rd.review=rf.review

                        join book_dim_table bd
                        on rf.book_id=bd.book_id
                        where bd.book_theme='{theme_selected}' and rd.author in (False,0)

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','review_likes','review_comments','sentiment'])
                        return data

        def get_author_review(theme_selected):
                        cursor = mydb.cursor()
                        query = f"""
                        
                        select
                                        rf.name,
                                        rf.review,
                                        rf.ratings_given_out_of_5,
                                        rf.review_likes,
                                        rf.review_comments,
                                        rf.sentiment
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rd.name = rf.name and rd.review=rf.review

                        join book_dim_table bd
                        on rf.book_id=bd.book_id
                        where bd.book_theme='{theme_selected}' and rd.author in (True,1)

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','review_likes','review_comments','sentiment'])
                        
                        return data
                

        def get_all_review(theme_selected):
                        cursor = mydb.cursor()
                        query = f"""
                        
                        select
                                        rf.name,
                                        rf.review,
                                        rf.ratings_given_out_of_5,
                                        rf.review_likes,
                                        rf.review_comments,
                                        rf.sentiment
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rd.name = rf.name and rd.review=rf.review

                        join book_dim_table bd
                        on rf.book_id=bd.book_id

                        where bd.book_theme='{theme_selected}' 

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','review_likes','review_comments','sentiment'])
                        
                        return data

        non_author_review_table=get_non_author_reviews(theme_selected)
        author_review_table=get_author_review(theme_selected)
        all_review_table=get_all_review(theme_selected)

        st.header('Reviews')
        st.write('Click on review to read more')

        reviews_col_checkbox=st.columns([1,1],gap='large')
        with reviews_col_checkbox[0]:
                        author_filter_checkbox=st.checkbox('Author reviews')
                        non_author_filter_checkbox=st.checkbox('Non author reviews')
        with reviews_col_checkbox[1]:
                        positive_filter_checkbox = st.checkbox("Positive sentiment")
                        neutral_filter_checkbox = st.checkbox("Neutral sentiment")
                        negative_filter_checkbox = st.checkbox("Negative sentiment")
        

                #if press then change variable
        if positive_filter_checkbox:
                filter_positive_sentiment = True
        else:
                filter_positive_sentiment = False
        
        if neutral_filter_checkbox:
                filter_neutral_sentiment = True
        else:
                filter_neutral_sentiment = False
        
        if negative_filter_checkbox:
                filter_negative_sentiment = True
        else:
                filter_negative_sentiment = False

        if author_filter_checkbox:
                filter_author_reviews=True
        else:
                filter_author_reviews=False

        if non_author_filter_checkbox:
                filter_non_author_reviews=True
        else:
                filter_non_author_reviews=False
                
        
        ##case if non author and sentiments
        if filter_positive_sentiment and filter_non_author_reviews:
                filtered_df = non_author_review_table[non_author_review_table['sentiment'] == 'positive']
        elif filter_neutral_sentiment and filter_non_author_reviews:
                filtered_df = non_author_review_table[non_author_review_table['sentiment'] == 'neutral']
        elif filter_negative_sentiment and filter_non_author_reviews:
                filtered_df = non_author_review_table[non_author_review_table['sentiment'] == 'negative']
        #if not checked then just show the original dataframe

        #case if author and sentiments
        elif filter_positive_sentiment and filter_author_reviews:
                filtered_df=author_review_table[author_review_table['sentiment'] == 'positive']
        elif filter_neutral_sentiment and filter_author_reviews:
                filtered_df=author_review_table[author_review_table['sentiment'] == 'neutral']
        elif filter_negative_sentiment and filter_author_reviews:
                filtered_df=author_review_table[author_review_table['sentiment'] == 'negative']

        #case if only sentiments
        elif filter_positive_sentiment:
                filtered_df=all_review_table[all_review_table['sentiment'] == 'positive']
        elif filter_neutral_sentiment:
                filtered_df=all_review_table[all_review_table['sentiment'] == 'neutral']
        elif filter_negative_sentiment:
                filtered_df=all_review_table[all_review_table['sentiment'] == 'negative']

        #case if only author/non author
        elif filter_author_reviews:
                filtered_df = author_review_table
        else:
                filtered_df = non_author_review_table

        container = st.container()
        container.markdown(
        """
        <style>
        .centered {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 80vh;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )

        with container.container():
                st.dataframe(filtered_df,width=9000)
                st.caption('The table is adjustable')


