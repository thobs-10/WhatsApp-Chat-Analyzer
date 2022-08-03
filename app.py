import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

# title of the web app
st.sidebar.title("Whatsapp Chat Analyzer")

#upload section to upload the txt files
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode(encoding="utf-8")
    #pass the raw data in thee preprocessing file and get dataframe formated data
    df = preprocessor.preprocess(data)

    #get all the unique users
    users_list = df['users'].unique().tolist()
    #remove the group not added to the list
    users_list.remove('group_notification')
    #sort the names
    users_list.sort()
    #inser the list to the drop down option
    users_list.insert(0, "Overall")

    # get the selected user from the list
    selected_user = st.sidebar.selectbox("Show Analysis for ",users_list)

    # a button to click for the analyytics display
    if st.sidebar.button("Show Analysis"):
        #analytics
        num_messages, words, num_media_messages, num_shared_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_shared_links)
        # monthly stats
        st.title("Monthly Timeline")
        moonthly_timeline = helper.monthly_timeline_data(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(moonthly_timeline['time'], moonthly_timeline['messages'], color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily stats
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline_data(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col_1,col_2 = st.columns(2)
        with col_1:
            st.header("Most Busy Days")
            busy_day_data = helper.weekly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day_data.index, busy_day_data.values, color = 'purple')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col_2:
            st.header("Most Busy Months")
            busy_month_data = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month_data.index, busy_month_data.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # weekly activity map
        st.title("Weekly Activity Map")
        user_heatmap_data = helper.activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap_data)
        st.pyplot(fig)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='blue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # most common words
        #st.title('Most commmon words')
        #most_common_df = helper.most_common_words(selected_user, df)
        #fig, ax = plt.subplots(figsize=(15, 15))
        #ax.barh(most_common_df[0].head(), most_common_df[1].head())
        #plt.xticks(rotation='vertical')
        #st.pyplot(fig)

        # emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)






