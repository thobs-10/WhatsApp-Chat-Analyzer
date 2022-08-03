from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
from urlextract import URLExtract
import re

extract = URLExtract()

# fetch the stats for the analytics display
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    # fetch num of mssgs
    num_messages= df.shape[0]


    #total num of words
    tot_words =[]
    for mssg in df['messages']:
        tot_words.extend(mssg.split())

    # num of media messages
    num_media_mssgs = df[df['messages']=='<Media omitted>\n'].shape[0]

    # num of shared links
    links = []
    for mssg in df['messages']:
        links.extend(extract.find_urls(mssg))


    return num_messages,len(tot_words),num_media_mssgs,len(links)

def most_busy_users(df):
    '''get the stats of the most busy users on the group chat'''
    #get the top users
    top_users = df['users'].value_counts().head()
    df_top_users = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns ={'index':'name','users':'percent'}
    )
    return top_users,df_top_users

def create_word_cloud(selected_user,df):
    '''get data about the words that are frequently used in the group chat by the selected user'''
    #get stop words txt file
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df =df[df['users']==selected_user]

    temp = df[df['users']!='group_notification']
    temp = temp[temp['messages']!='<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    word_cloud = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_word_cloud = word_cloud.generate(temp['messages'].str.cat(sep=" "))
    return df_word_cloud

def most_common_words(selected_user,df):
    '''get the most common words wused in the group chat'''
    # get stop words txt file
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []

    for word in temp['messages']:
        if word not in stop_words:
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    """get the most common emojis used in the group chat by this selected user"""
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis =[]
    for mssg in df['messages']:
        emojis.extend([c for c in mssg if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df
def monthly_timeline_data(selected_user,df):
    '''get the stats of monthly usage of the selected user or the ovearall'''
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+ str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline_data(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    monthly_count = df['month'].value_counts()
    return monthly_count

def weekly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    weekly_count = df['day_name'].value_counts()
    return weekly_count


def activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name',columns='period', values='messages',aggfunc='count').fillna(0)
    return user_heatmap




