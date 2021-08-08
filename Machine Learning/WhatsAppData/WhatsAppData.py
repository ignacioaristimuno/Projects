import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from plotly import express as px
from seaborn import *
import seaborn as sns
from heatmap import heatmap
from wordcloud import WordCloud, STOPWORDS
from datetime import *
import re
from nltk import *


# Charts style
sns.set_style('darkgrid')
plt.style.use('seaborn')


#################### FUNCTIONS ####################
# Python code to extract Date from chat file 
def startsWithDateAndTime(s):
    pattern = '^([0-9]+)(/)([0-9]+)(/)([0-9][0-9]), ([0-9]+):([0-9]+):([0-9]+) -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

# Regex pattern to extract username of Author.
def FindAuthor(s):
    patterns = [
        '([w]+):',                      # First Name
        '([w]+[s]+[w]+):',              # First Name + Last Name
        '([w]+[s]+[w]+[s]+[w]+):',      # First Name + Middle Name + Last Name
        '([w]+)[u263a-U0001f999]+:',    # Name and Emoji              
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

# Extracting Date, Time, Author and message from the chat file.
def getDataPoint(line):   
    splitLine = line.split(' - ') 
    dateTime = splitLine[0]
    date, time = dateTime.split(', ') 
    rest = ' - '.join(splitLine[1:])
    rest_split = rest.split(': ')
    author = rest_split[0]
    message = ': '.join(rest_split[1:])
    return date, time, author, message


#################### DATA PREPROCESSING ####################
# Convert data into DataFrame
parsedData = []
conversationPath = 'C:\\Users\\ignia\\Downloads\\_chat2.txt'
with open(conversationPath, encoding="utf-8") as fp:
    fp.readline()               
    fp.readline()
    fp.readline()                    
    messageBuffer = [] 
    date, time, author = None, None, None
    while True:
        line = fp.readline()
        if not line: 
            break
        line = line.strip() 
        if startsWithDateAndTime(line): 
            if len(messageBuffer) > 0: 
                parsedData.append([date, time, author, ' '.join(messageBuffer)]) 
            messageBuffer.clear()
            date, time, author, message = getDataPoint(line)
            messageBuffer.append(message) 
        else:
            messageBuffer.append(line)

df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message']) # Initialising a pandas Dataframe.

# Check basic information and clean the dataset
df["Date"] = pd.to_datetime(df["Date"])
df = df.dropna()
df = df.reset_index(drop=True)
df.shape

# Adding one more column of "Day" for better analysis, here we use datetime library which help us to do this task easily.
weeks = {
0 : 'Monday',
1 : 'Tuesday',
2 : 'Wednesday',
3 : 'Thrusday',
4 : 'Friday',
5 : 'Saturday',
6 : 'Sunday'
}
df['Day'] = df['Date'].dt.weekday.map(weeks)

# Formatting
df = df[['Date','Day','Time','Author','Message']]
df['Day'] = df['Day'].astype('category')
df["Letter's"] = df['Message'].apply(lambda s : len(s))
df["Word's"] = df['Message'].apply(lambda s : len(s.split(' ')))

# Function to count number of links in dataset, it will add extra column and store information in it.
URLPATTERN = r'(http?://S+)'
df['Url_Count'] = df.Message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
links = np.sum(df.Url_Count)

# Function to count number of media in chat.
MEDIAPATTERN = 'omitted'
df['Media_Count'] = df.Message.apply(lambda x : re.findall(MEDIAPATTERN, x)).str.len()
media = np.sum(df.Media_Count)


#################### STATISTICS ####################
# Extract basic statistics from the dataset
total_messages = df.shape[0]
media_messages = df[df['Message'] == '<Media omitted>'].shape[0]
links = np.sum(df.Url_Count)
print('Group Chatting Stats : ')
print('Total Number of Messages : {}'.format(total_messages))
print('Total Number of Media Messages : {}'.format(media_messages))
print('Total Number of Links : {}'.format(links))

# Extract basic statistics from each user
l = df.Author.unique()
for i in range(len(l)):
    req_df = df[df["Author"] == l[i]]
    print(f'--> Stats of {l[i]} <-- ')
    print('Total Message Sent : ', req_df.shape[0])
    words_per_message = (np.sum(req_df["Word's"]))/req_df.shape[0]
    w_p_m = ("%.3f" % round(words_per_message, 2))  
    print('Average Words per Message : ', w_p_m)
    ### media conists of media messages
    media = sum(req_df["Media_Count"])
    print('Total Media Message Sent : ', media)
    ### links consist of total links
    links = sum(req_df["Url_Count"])   
    print('Total Links Sent : ', links)   
    print()
    print('----------------------------------------------------------n')


# Extract words from messages and remove insignificant words
text = " ".join(review for review in df.Message)
stopwords = ['y', 'de', 'la', 'que']
querywords = text.split()
resultwords  = [word for word in querywords if word.lower() not in stopwords]
result = ' '.join(resultwords)

# Word Cloud of mostly used word in our Group
wordcloud = WordCloud(stopwords=STOPWORDS, background_color="black").generate(result)
plt.figure( figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# Extract words from messages and remove insignificant words
text = " ".join(review for review in df.Message)
stopwords = ['y', 'de']
querywords = text.split()
resultwords  = [word for word in querywords if word.lower() not in stopwords]
result = ' '.join(resultwords)

# Word Cloud of mostly used word in our Group
wordcloud = WordCloud(stopwords=STOPWORDS, background_color="black").generate(result)
plt.figure( figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# Mensajes mas enviados
mensajes_repetidos = df['Message'].value_counts()
mensajes_repetidos = mensajes_repetidos.head(30)


# Total no. of messages sent by user
l = df.Author.unique()
for i in range(len(l)):
    req_df = df[df["Author"] == l[i]]
    print(l[i],'  ->  ',req_df.shape[0])

  
# Total messages sent on each day of the week
l = df.Day.unique()
for i in range(len(l)):
    req_df = df[df["Day"] == l[i]]
    print(l[i],'  ->  ',req_df.shape[0])


# Most active Author in the Group
plt.figure(figsize=(9,6))
mostly_active = df['Author'].value_counts()
m_a = mostly_active.head(13)
bars = ['Geo','Sofi','Isa','Fefe','Luli Arévalo','Mauri','Lula Antúnez','Jules','Cyn','Nacho', 'Tien', 'Yann', 'Dami']
x_pos = np.arange(len(bars))
m_a.plot.bar()
plt.xlabel('Buddy',fontdict={'fontsize': 14,'fontweight': 10})
plt.ylabel('Cant. de mensajes',fontdict={'fontsize': 14,'fontweight': 10})
plt.title('Cantidad de mensajes enviados por persona',fontdict={'fontsize': 20,'fontweight': 8})
plt.xticks(x_pos, bars)
plt.show()


# Most active day in the Group
plt.figure(figsize=(8,5))
active_day = df['Day'].value_counts()

# Top people that are mostly active in our Group is : 
a_d = active_day.head(10)
a_d.plot.bar()
plt.xlabel('Día de la semana',fontdict={'fontsize': 12,'fontweight': 10})
plt.ylabel('Cant. de mensajes',fontdict={'fontsize': 12,'fontweight': 10})
plt.title('Mostly active day of Week in the Group',fontdict={'fontsize': 18,'fontweight': 8})
plt.show()


# Top Image contributors of the Group
mm = df
mm['Images'] = mm.Message.str.extract(r'\W*(image omitted)\W*', expand=True)
mm = mm[mm.Images.notnull()]
mm1 = mm['Author'].value_counts()
bars = ['Geo','Fefe','Sofi','Luli Arévalo','Isa','Mauri','Lula Antúnez','Cyn','Nacho','Jules', 'Tien', 'Yann', 'Dami']
x_pos = np.arange(len(bars))
top10 = mm1.head(13)
top10.plot.bar()
plt.xlabel("Buddy",fontdict={'fontsize': 12,'fontweight': 10})
plt.ylabel('Cant. de imágenes',fontdict={'fontsize': 12,'fontweight': 10})
plt.title('Cantidad de Imágenes enviadas por persona',fontdict={'fontsize': 18,'fontweight': 8})
plt.xticks(x_pos, bars)
plt.show()


# Top Stickers contributor of the Group
mm = df
mm['Stickers'] = mm.Message.str.extract(r'\W*(sticker omitted)\W*', expand=True)
mm = mm[mm.Stickers.notnull()]
mm1 = mm['Author'].value_counts()
bars = ['Luli Arévalo', 'Sofi', 'Geo', 'Lula Antúnez', 'Nacho', 'Fefe', 'Jules', 'Isa', 'Cyn', 'Tien', 'Mauri', 'Dami', 'Yann']
x_pos = np.arange(len(bars))
top10 = mm1.head(13)
top10.plot.bar()
plt.xlabel("Buddy",fontdict={'fontsize': 12,'fontweight': 10})
plt.ylabel('Cant de Stickers',fontdict={'fontsize': 12,'fontweight': 10})
plt.title('Cantidad de Stickers enviados por persona ',fontdict={'fontsize': 18,'fontweight': 8})
plt.xticks(x_pos, bars)
plt.show()


### Top-10 Stickers Media Contributor of Group
mm = df
mm['Videos'] = mm.Message.str.extract(r'\W*(video omitted)\W*', expand=True)
mm = mm[mm.Videos.notnull()]
mm1 = mm['Author'].value_counts()
bars = ['Sofi', 'Geo', 'Luli Arévalo', 'Isa', 'Lula Antúnez', ' Cyn', 'Fefe', 'Nacho', 'Mauri', 'Tien', 'Julien']
x_pos = np.arange(len(bars))
top10 = mm1.head(11)
top10.plot.bar()
plt.xlabel("Buddy",fontdict={'fontsize': 12,'fontwedfight': 10})
plt.ylabel('Cant. de Videos',fontdict={'fontsize': 12,'fontweight': 10})
plt.title('Cantidad de Videos enviados por persona',fontdict={'fontsize': 18,'fontweight': 8})
plt.xticks(x_pos, bars)
plt.show()


# Top Audio Contributor of Group
mm = df
mm['Audios'] = mm.Message.str.extract(r'\W*(audio omitted)\W*', expand=True)
mm = mm[mm.Audios.notnull()]
mm1 = mm['Author'].value_counts()
bars = ['Fefe', 'Geo', 'Sofi', 'Isa', 'Luli Arévalo', 'Mauri', 'Lula Antúnez', ' Julien', 'Nacho', 'Tien', 'Dami', 'Yann']
x_pos = np.arange(len(bars))
top10 = mm1.head(11)
top10.plot.bar()
plt.xlabel("Buddy",fontdict={'fontsize': 12,'fontwedfight': 10})
plt.ylabel('Cant. de Audios',fontdict={'fontsize': 12,'fontweight': 10})
plt.title('Cantidad de Audios enviados por persona',fontdict={'fontsize': 18,'fontweight': 8})
plt.xticks(x_pos, bars)
plt.show()


# Words are off course most powerful weapon in the world, so let’s check who has this powerful weapon in the group
max_words = df[['Author',"Word's"]].groupby('Author').sum() / 
m_w = max_words.sort_values("Word's",ascending=False).head(10)
bars = ['A','B','C','D','E','F','G','H','I','J']
x_pos = np.arange(len(bars))
m_w.plot.bar(rot=90)
plt.xlabel('Author')
plt.ylabel('No. of words')
plt.title('Analysis of members who has used max. no. of words in his/her messages')
plt.xticks(x_pos, bars)
plt.show()


# Let’s check Top-10 author who has shared maximum no. of links in the group
### Member who has shared max numbers of link in Group 
max_words = df[['Author','Url_Count']].groupby('Author').sum()
m_w = max_words.sort_values('Url_Count',ascending=False).head(10)
bars = ['A','B','C','D','E','F','G','H','I','J']
x_pos = np.arange(len(bars))
m_w.plot.bar(rot=90)
plt.xlabel('Author')
plt.ylabel("No. of link's")
plt.title("Analysis of member's who has shared max no. of link's in Group")
plt.xticks(x_pos, bars)
plt.show()



# Let’s check the time whenever the group was highly active
### Time whenever our group is highly active
plt.figure(figsize=(8,5))
t = df['Time'].value_counts().head(20)
tx = t.plot.bar()
tx.yaxis.set_major_locator(MaxNLocator(integer=True))  #Converting y axis data to integer
plt.xlabel('Time',fontdict={'fontsize': 12,'fontweight': 10})
plt.ylabel('No. of messages',fontdict={'fontsize': 12,'fontweight': 10})
plt.title('Analysis of time when Group was highly active.',fontdict={'fontsize': 18,'fontweight': 8})
plt.show()


# Converting 12-hour formate to 24 hours will help us for better analysis : 
lst = []
for i in df['Time'] :
out_time = datetime.strftime(datetime.strptime(i,"%I:%M %p"),"%H:%M")
lst.append(out_time)
df['24H_Time'] = lst
df['Hours'] = df['24H_Time'].apply(lambda x : x.split(':')[0])


# Let’s check the most suitable hour of the day whenever there will be more chances of getting a response from group members
### Most suitable hour of day, whenever there will more chances of getting responce from group members.
plt.figure(figsize=(8,5))
std_time = df['Hours'].value_counts().head(15)
s_T = std_time.plot.bar()
s_T.yaxis.set_major_locator(MaxNLocator(integer=True))  #Converting y axis data to integer
plt.xlabel('Hours (24-Hour)',fontdict={'fontsize': 12,'fontweight': 10})
plt.ylabel('No. of messages',fontdict={'fontsize': 12,'fontweight': 10})
plt.title('Most suitable hour of day.',fontdict={'fontsize': 18,'fontweight': 8})
plt.show()


# Let’s create a word cloud of Top-10 highly active members
active_m = 

for i in range(len(active_m)) :
    # Filtering out messages of particular user
    m_chat = df[df["Author"] == active_m[i]]
    print(f'--- Author :  {active_m[i]} --- ')
    # Word Cloud of mostly used word in our Group
    msg = ' '.join(x for x in m_chat.Message)
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(msg)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    print('____________________________________________________________________________________n')


# Let's check the date on which our group was highly active
### Date on which our Group was highly active.
plt.figure(figsize=(8,5))
df['Date'].value_counts().head(15).plot.bar()
plt.xlabel('Date',fontdict={'fontsize': 14,'fontweight': 10})
plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
plt.title('Analysis of Date on which Group was highly active',fontdict={'fontsize': 18,'fontweight': 8})
plt.show()

# Let's create a time series plot w.r.t. no. of messages
z = df['Date'].value_counts() 
z1 = z.to_dict() #converts to dictionary
df['Msg_count'] = df['Date'].map(z1)
### Timeseries plot 
fig = px.line(x=df['Date'],y=df['Msg_count'])
fig.update_layout(title='Analysis of number of message's using TimeSeries plot.',
                  xaxis_title='Month',
                  yaxis_title='No. of Messages')
fig.update_xaxes(nticks=20)
fig.show()


# Let's create a separate column for Month and Year for better analysis
df['Year'] = df['Date'].dt.year
df['Mon'] = df['Date'].dt.month
months = {
     1 : 'Jan',
     2 : 'Feb',
     3 : 'Mar',
     4 : 'Apr',
     5 : 'May',
     6 : 'Jun',
     7 : 'Jul',
     8 : 'Aug',
     9 : 'Sep',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec'
}
df['Month'] = df['Mon'].map(months)
df.drop('Mon',axis=1,inplace=True)


# Let's check mostly active month
### Mostly Active month 
plt.figure(figsize=(12,6))
active_month = df['Month_Year'].value_counts()
a_m = active_month
a_m.plot.bar()
plt.xlabel('Month',fontdict={'fontsize': 14,'fontweight': 10})
plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
plt.title('Analysis of mostly active month.',fontdict={'fontsize': 20,
        'fontweight': 8})
plt.show()


# Let's analyze the most active month using a line plot
z = df['Month_Year'].value_counts() 
z1 = z.to_dict() #converts to dictionary
df['Msg_count_monthly'] = df['Month_Year'].map(z1)
plt.figure(figsize=(18,9))
sns.set_style("darkgrid")
sns.lineplot(data=df,x='Month_Year',y='Msg_count_monthly',markers=True,marker='o')
plt.xlabel('Month',fontdict={'fontsize': 14,'fontweight': 10})
plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
plt.title('Analysis of mostly active month using line plot.',fontdict={'fontsize': 20,'fontweight': 8})
plt.show()


# Let's check the total message per year
### Total message per year
### As we analyse that the group was created in mid 2019, thats why number of messages in 2019 is less.
plt.figure(figsize=(12,6))
active_month = df['Year'].value_counts()
a_m = active_month
a_m.plot.bar()
plt.xlabel('Year',fontdict={'fontsize': 14,'fontweight': 10})
plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
plt.title('Analysis of mostly active year.',fontdict={'fontsize': 20,'fontweight': 8})
plt.show()


# Let's use a heatmap and analyze highly active Day w.r.t. Time
df2 = df.groupby(['Hours', 'Day'], as_index=False)["Message"].count()
df2 = df2.dropna()
df2.reset_index(drop = True,inplace = True)
### Analysing on which time group is mostly active based on hours and day.
analysis_2_df = df.groupby(['Hours', 'Day'], as_index=False)["Message"].count()
### Droping null values
analysis_2_df.dropna(inplace=True)
analysis_2_df.sort_values(by=['Message'],ascending=False)
day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday', 'Saturday', 'Sunday']
plt.figure(figsize=(15,8))
heatmap(
    x=analysis_2_df['Hours'],
    y=analysis_2_df['Day'],
    size_scale = 500,
    size = analysis_2_df['Message'], 
    y_order = day_of_week[:-1],
    color = analysis_2_df['Message'], 
    palette = sns.cubehelix_palette(128)
)
plt.show()




  
  