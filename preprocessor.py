import pandas as pd
import re

# preprocess data
def preprocess(data):
    '''preprocessing function to get every vital detail we need'''

    # apply some regular expressions
    pattern = '\d{2,4}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message data type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%Y/%m/%d, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # seperate users and messagees
    users = []
    messages = []
    for mssg in df['user_message']:
        # split the user and the message
        entry = re.split('([\w\W]+?):\s', mssg)
        if entry[1:]:
            # add user name to the list
            users.append(entry[1])
            # add message to the mssges list
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # unpack the dat column to get different values
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period =[]
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period

    return df
