import streamlit as st
import mysql.connector
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from db_conn import mydb
import plotly.graph_objs as go
import requests





def individual_book_layout(book_name):
        
      
        ## display number of reviews and author and non author
        col1,col2,col3= st.columns(3)

        #to display the number of books depending on its category
        def get_review_count(book_name):
                cursor = mydb.cursor()
                query = f"SELECT COUNT(*) FROM review_fact_table WHERE book_name = '{book_name}'"
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count

        def get_author_review_count(book_name):
                cursor = mydb.cursor()
                query = f"""
                        WITH t1  as 
                                (select rf.name,rf.book_name,rd.author from review_fact_table rf
                                join reviewer_dim_table  rd
                                on rf.review_id=rd.review_id and rd.name = rf.name)
                        select 
                        count(name)
                        from t1
                        WHERE book_name = '{book_name}' AND author in (True)
                """
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count

        def get_non_author_review_count(book_name):
                cursor = mydb.cursor()
                query = f"""
                        WITH t1  as 
                                (select rf.name,rf.book_name,rd.author from review_fact_table rf
                                join reviewer_dim_table  rd
                                on rf.review_id=rd.review_id and rd.name = rf.name)
                        select 
                        count(*)
                        from t1
                        WHERE book_name = '{book_name}' AND author in (False)
                """
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count


        #display the number of reviews
        # book_name = st.selectbox("Select a book name", ["Politik untuk pemula", "Leviathan"])

        review_count = get_review_count(book_name)
        author_review_count=get_author_review_count(book_name)
        non_author_review_count=get_non_author_review_count(book_name)

        #show the metric
        col1.metric(label='Number of reviews',value=review_count)
        col2.metric(label='Number of author reviews',value=author_review_count)
        col3.metric(label='Number of non author reviews',value=non_author_review_count)


        def get_sample_review_with_filter(book_name,filter):


                cursor = mydb.cursor()
                query1 = f"""
                        
                with t5 as (select
                                        name,
                                        review,
                                        ratings_given_out_of_5,
                                        review_likes,
                                        sentiment
                                        from review_fact_table
                                        where book_name='{book_name}' and language='en' )

                                select
                                *
                                from t5
                                where review_likes = (SELECT MAX(review_likes) FROM review_fact_table where book_name='{book_name}')
                                LIMIT 1

                        """

                query2=f"""
                        
                with t5 as (select
                                        name,
                                        review,
                                        ratings_given_out_of_5,
                                        review_comments,
                                        sentiment
                                        from review_fact_table
                                        where book_name='{book_name}' and language='en' )

                                select
                                *
                                from t5
                                where review_comments = (SELECT MAX(review_comments) FROM review_fact_table)
                                LIMIT 1
                        """
                

                query3=f"""
                        
                        select
                                rf.name,
                                rf.review,
                                rf.ratings_given_out_of_5,
                                rd.reviewer_reviews,
                                rf.sentiment
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rf.name=rd.name and rf.review_id=rd.review_id
                        where book_name='{book_name}' and language='en' 
                        order by rd.reviewer_reviews desc
                        LIMIT 1

                        """

                query4=f"""
                        
                        select
                                rf.name,
                                rf.review,
                                rf.ratings_given_out_of_5,
                                rd.reviewer_followers,
                                rf.sentiment
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rf.name=rd.name and rf.review_id=rd.review_id
                        where book_name='{book_name}' and language='en' 
                        order by rd.reviewer_followers desc
                        LIMIT 1
                        """


                query5=f"""
                        
                        select
                                rf.name,
                                rf.review,
                                rf.ratings_given_out_of_5,
                                rd.num_author_followers,
                                rf.sentiment
                        from review_fact_table rf
                        join reviewer_dim_table rd
                        on rf.name=rd.name and rf.review_id=rd.review_id
                        where book_name='{book_name}' and rd.author in (True) and rf.language='en' 
                        order by rd.num_author_followers desc
                        limit 1

                        """

                
                query6=f"""
                        
                        select
                                rf.name,
                                rf.review,
                                rf.ratings_given_out_of_5,
                                rd.num_author_books,
                                rf.sentiment
                                from review_fact_table rf
                                join reviewer_dim_table rd
                                on rf.name=rd.name and rf.review_id=rd.review_id
                                where book_name='{book_name}' and rd.author in (True) and rf.language='en' 
                                order by rd.num_author_books desc
                                limit 1


                        """


                if filter=="Review with the most likes":
                        cursor.execute(query1)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','review_likes','sentiment'])
                elif filter=="Review with the most comments":
                        cursor.execute(query2)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','review_comments','sentiment'])
                elif filter=="Reviewer with the most reviews":
                        cursor.execute(query3)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','reviewer_reviews','sentiment'])
                elif filter=="Reviewer with the most followers":
                        cursor.execute(query4)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','reviewer_followers','sentiment'])
                elif filter== "Author review with the most followers":
                        cursor.execute(query5)
                        data=cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','num_author_followers','sentiment'])
                elif filter=="Author review with the most books":
                        cursor.execute(query6)
                        data=cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','num_author_bookssss','sentiment'])


                return data


        review_with_top_likes_counter = False
        review_with_top_comments_counter = False
        reviewer_with_top_reviews_counter= False
        reviewer_with_top_followers_counter=False

        author_with_top_followers_counter=False
        author_with_top_books_counter=False


        st.header('Sample reviews')
       


        # center align the container using CSS
        st.markdown("""
        <style>
                table {
                margin: auto;
                }
        </style>
        """, unsafe_allow_html=True)

        options = st.selectbox(
        'Select a sample review',
        ['Review with the most likes', 'Review with the most comments', 
        'Reviewer with the most reviews', 'Reviewer with the most followers',
        'Author review with the most followers', 'Author review with the most books'],
        )





        if options == "Review with the most likes":
                review_with_top_likes_counter=True
        elif options == "Review with the most comments":
                review_with_top_comments_counter=True
        elif options == "Reviewer with the most reviews":
                reviewer_with_top_reviews_counter=True
        elif options == "Reviewer with with the most followers":
                reviewer_with_top_followers_counter=True
        elif options == "Author review with the most followers":
                author_with_top_books_counter=True
        elif options == "Author review with the most books":
                author_with_top_followers_counter=True


        if review_with_top_likes_counter:
                sample_review_table_with_filter=get_sample_review_with_filter(book_name=book_name,filter=options)
                st.table(sample_review_table_with_filter)
        elif review_with_top_comments_counter:
                sample_review_table_with_filter=get_sample_review_with_filter(book_name=book_name,filter=options)
                st.table(sample_review_table_with_filter)
        elif reviewer_with_top_reviews_counter:
                sample_review_table_with_filter=get_sample_review_with_filter(book_name=book_name,filter=options)
                st.table(sample_review_table_with_filter)
        elif reviewer_with_top_followers_counter:
                sample_review_table_with_filter=get_sample_review_with_filter(book_name=book_name,filter=options)
                st.table(sample_review_table_with_filter)
        elif author_with_top_followers_counter:
                sample_review_table_with_filter=get_sample_review_with_filter(book_name=book_name,filter=options)
                st.table(sample_review_table_with_filter)
        elif author_with_top_books_counter:
                sample_review_table_with_filter=get_sample_review_with_filter(book_name=book_name,filter=options)
                st.table(sample_review_table_with_filter)
        else:
                sample_review_table_with_filter=get_sample_review_with_filter(book_name=book_name,filter=options)
                st.table(sample_review_table_with_filter)

        cols = st.columns([1,1])

        with cols[0]:

                #visualization of sentiment bar chart
                def get_sentiment_percentage_by_book(book_name):
                
                        cursor = mydb.cursor()
                        query = f"""
                                with t2 as (select
                                        book_name,
                                        sentiment,
                                        count(*) as num_of_sentiment
                                        from review_fact_table
                                        where book_name='{book_name}'
                                        group by book_name,sentiment)

                                select
                                sentiment,
                                CAST(((num_of_sentiment/(select sum(num_of_sentiment) from t2))*100) AS float) as sentiment_percentage
                                from t2
                                ORDER BY sentiment_percentage DESC
                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['sentiment','sentiment_percentage'])
                        return data


                sentiment_percentage_by_book_table=get_sentiment_percentage_by_book(book_name=book_name)
                # st.bar_chart(data=sentiment_percentage_by_book_table,x=sentiment_percentage_by_book_table['sentiment'])

                fig = px.bar(
                        sentiment_percentage_by_book_table,
                        x='sentiment',
                        y='sentiment_percentage',
                        color='sentiment',
                        text_auto=True,
                        title=f'<b>Review sentiments (by percentage %)</b>',
                        labels={'sentiment':'Sentiment','sentiment_percentage':'Percentage'}
                )
                fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),width=550,height=450,xaxis_title='Sentiment',yaxis_title='Sentiment percentage %')
                st.plotly_chart(fig, theme='streamlit')

        

        with cols[0]:
                
                #visualization of languages using pie chart
                def get_language_percentage_by_book(book_name):
                
                        cursor = mydb.cursor()
                        query = f"""
                        
                                with t3 as (select 
                                                count(*) lang_count,
                                                language
                                                from review_fact_table
                                                where book_name='{book_name}'
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

                language_percentage_by_book=get_language_percentage_by_book(book_name=book_name)

        
                piechart= px.pie(language_percentage_by_book, 
                                values='language_percentage',
                                title=f'Language distribution',
                                names='language',
                                labels={'language':'Language','language_percentage':'Percentage %'}
                                )
                piechart.update_layout(margin=dict(l=20, r=20, t=30, b=0),width=10,height=450)
                st.plotly_chart(piechart, use_container_width=True)



        with cols[1]:

        #to display the ratings given by reviewers

                def get_ratings_percentage_by_book(book_name):
        
                        cursor = mydb.cursor()
                        query = f"""
                        
                        with t4 as (select
                                                ratings_given_out_of_5,
                                                sentiment,
                                                count(*) num_of_ratings
                                                from review_fact_table
                                                where book_name='{book_name}' 
                                                group by ratings_given_out_of_5
                                                order by num_of_ratings desc)

                                select
                                        ratings_given_out_of_5,
                                        (num_of_ratings/(select sum(num_of_ratings) from t4)*100) as ratings_given_percentage,
                                        sentiment
                                from t4

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['ratings_given_out_of_5','ratings_given_percentage','sentiment'])
                        return data

                def get_ratings_percetange_by_book_bubble(book_name):
                        
                        cursor = mydb.cursor()
                        query = f"""
                                                
                                        SELECT
                                ratings_given_out_of_5 as ratings,
                                sentiment,
                                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ratings_given_out_of_5) AS percentage
                                FROM
                                review_fact_table
                                where book_name = '{book_name}'
                                GROUP BY
                                ratings,
                                sentiment
                                ORDER BY
                                ratings ASC,
                                sentiment ASC;


                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['ratings','sentiment','ratings_given_percentage'])
                        data['ratings_given_percentage']=data['ratings_given_percentage'].astype(float)
                        return data

                sentiments=['Positive','Neutral','Negative']
                selected_sentiment = st.selectbox("Select Sentiment", sentiments)

                selected_sentiment=selected_sentiment.lower()
                ratings_percentage_by_book_table_bubble=get_ratings_percetange_by_book_bubble(book_name)
                filtered_data = ratings_percentage_by_book_table_bubble[ratings_percentage_by_book_table_bubble['sentiment'] == selected_sentiment]
                opacity_vals = filtered_data['ratings_given_percentage'].apply(lambda x: x / 100.0 * 0.8 + 0.2)

                fig = px.scatter(filtered_data, x="ratings", y="ratings_given_percentage", 
                                 size="ratings_given_percentage", color="sentiment", 
                                 hover_data=["ratings_given_percentage"],
                                 size_max=60,opacity=opacity_vals,width=600, labels={'sentiment':'Sentiment','ratings':'Ratings','ratings_given_percentage':'Percentage'})
                

        # Set the layout
                fig.update_layout(
                title="Ratings given by reviewer grouped by sentiments",
                xaxis_title="Ratings",
                yaxis_title="Sentiment %",
                xaxis=dict(range=[0, 5])
                )
                st.caption('_0 = No ratings were given_')
                # Display the bubble chart
                st.plotly_chart(fig)


        # visualization for wordcloud to get most common words 


                
                def get_review(book_name):
        
                        stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content

                        stopwords = set(stopwords_list.decode().splitlines()) 

                        cursor = mydb.cursor()
                        query = f"""
                        
                        select
                                review,
                                sentiment
                        from review_fact_table
                        where book_name='{book_name}' and language='en'


                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['review','sentiment'])
                        data['review']=data['review'].str.lower().apply(lambda x : ' '.join(review for review in x.split() if review not in stopwords))

                        return data

                review_text_table=get_review(book_name=book_name)
                temp_review=''.join(review_text_table['review'])

                wordcloud = WordCloud(background_color='white').generate(temp_review)

                plt.figure(figsize=(5,5))
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.show()
                st.title('Wordcloud')
                st.pyplot()

        st.subheader('Word frequencies')
        words_freq_options = st.selectbox(
        'Select a sentiment',
        ['Positive','Neutral','Negative'],
        )

        words_freq_options=words_freq_options.lower()
        def words_frequency(dataframe,words_freq_options):
                        filtered_df=dataframe[dataframe['sentiment']==f'{words_freq_options}']
                        word_frequency=pd.Series(filtered_df['review']).str.split(expand=True).stack().value_counts()
                                                
                        plt.figure(figsize=(16,8))
                        word_frequency[:40].plot(kind='barh')
                        plt.xlabel('Word frequency')
                        plt.ylabel('Words')
                        st.pyplot()
        words_frequency(review_text_table,words_freq_options)



        full_reviews_cols=st.columns(1)

        with full_reviews_cols[0]:
                
                
                def get_non_author_reviews(book_name):
        
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
                        where book_name='{book_name}' and rd.author in (False)

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','review_likes','review_comments','sentiment'])
                        return data

                def get_author_review(book_name):
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
                        where book_name='{book_name}' and rd.author in (True)

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','review_likes','review_comments','sentiment'])
                        
                        return data
                

                def get_all_review(book_name):
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
                        where book_name='{book_name}' 

                        """
                        cursor.execute(query)
                        data = cursor.fetchall()
                        data=pd.DataFrame(data,columns=['name','review','ratings_given_out_of_5','review_likes','review_comments','sentiment'])
                        
                        return data

                non_author_review_table=get_non_author_reviews(book_name=book_name)
                author_review_table=get_author_review(book_name=book_name)
                all_review_table=get_all_review(book_name=book_name)

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
                        st.caption('_The tables are adjustable_')



