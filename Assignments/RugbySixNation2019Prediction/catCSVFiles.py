# -*- coding: utf-8 -*-

import pandas as pd # This is the standard

# Reading a csv into Pandas.
# df1 = pd.read_csv('Scraped Data/RugbyData_Matchup_england v france.csv', header=0)

# Getting first x rows.
# df1.head(5)
# df1.tail(5)

# df1.columns
# df1['HomeTeam']
# len(df1)


# Finding out basic statistical information on your dataset.
# pd.options.display.float_format = '{:,.3f}'.format # Limit output to 3 decimal places.
# df1.describe()

# df1[df1.HomeTeam == 'France']

# df2 = pd.read_csv('Scraped Data/RugbyData_Matchup_england v ireland.csv', header=0)
# df1.to_csv('total.csv')
# df2.to_csv('total.csv')


# with open('total.csv', 'a') as f:
#     df2.to_csv(f, header=0)
    
    

# Combine all the matchups data together into total.csv
countries = ['england', 'france', 'ireland', 'italy', 'scotland', 'wales']
for c1 in countries:
    for c2 in countries:
        try:
            df = pd.read_csv('Scraped Data/RugbyData_Matchup_'+c1+' v '+c2+'.csv', header=1)
            df.to_csv('allmatchup.csv', mode='a', header = False)
        except:
            print('wrong opening file with:'+c1+' v '+c2)
            continue
            
        
matchup_all = pd.read_csv('allmatchup.csv', names = ["num", "Unnamed", "HomeTeam", "Score", "AwayTeam", "Date", "Ground"])
matchup_all.head(5)
matchup_all.columns
# matchup_all = matchup_all.drop("num",1)
# matchup_all.reset_index()
# matchup_all["num"][5]

matchup_all.to_csv("allmatchup.csv")


# For question 1.1 What are the possible matchups (Team A vs Team B)
# And how many times they matchuped up as this fixtures

matchup_count = matchup_all.groupby(["HomeTeam","AwayTeam"]).size().reset_index().rename(columns = {0:'total'})

# Split the Score column into HomeTeam Score and AwayTeam Score

# matchup_all["Score"].str.split(' - ',1).tolist()
matchup_all["HomeTeamScore"] = matchup_all["Score"].str.split(' - ',1).str[0]
matchup_all["AwayTeamScore"] = matchup_all["Score"].str.split(' - ',1).str[1]

# check the splitted scores
matchup_all.columns
matchup_all[["Score", "HomeTeamScore", "AwayTeamScore"]]

# mark HomeTeam or AwayTeam is the winner
# WhoWin = 1 : HomeTeam Win
# WhoWin = 2 : AwayTeam Win
# WhoWin = 0 : Draw
matchup_all.loc[matchup_all["HomeTeamScore"] > matchup_all["AwayTeamScore"],"WhoWin"] = int(1)
matchup_all.loc[matchup_all["HomeTeamScore"] < matchup_all["AwayTeamScore"],"WhoWin"] = int(2)
matchup_all.loc[matchup_all["HomeTeamScore"] == matchup_all["AwayTeamScore"],"WhoWin"] = int(0)


# For question 1.2 What has historically been the winning percentage of each matchup (Team A vs Team B). 
win_count = matchup_all.groupby(["HomeTeam","AwayTeam", "WhoWin"]).size().reset_index().rename(columns = {0:'count'})
win_all = pd.merge(win_count, matchup_count, on=['HomeTeam', 'AwayTeam']) #inner join two dataframes
win_all["pctg"] = win_all["count"]/win_all["total"]

win_all.to_csv("winningPercentage.csv")

# calculate in each setting, the winning possibility of each team
win_stats = win_all.groupby(["HomeTeam","AwayTeam"]).apply(lambda t:t[t.pctg == t.pctg.max()])

win_stats.to_csv("winningPercentage.csv", mode = 'a')



#################################3
matchup_all["Date"]

matchup_all.sort_values(['Date'],ascending=1).Date.to_datetime
matchup_all['day'] = matchup_all["Date"].str.split(' ',2).str[0]
matchup_all['month'] = matchup_all["Date"].str.split(' ',2).str[1]
matchup_all['year'] = matchup_all["Date"].str.split(' ',2).str[2]

matchup_all.month = matchup_all.month.replace(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                          [1,2,3,4,5,6,7,8,9,10,11,12])

toDateConv = matchup_all[['year', 'month', 'day']]
matchup_all["DateNew"] = pd.to_datetime(toDateConv)



# for the recent N competition of each matchup, what are the results
recent3 = matchup_all[['HomeTeam','AwayTeam','WhoWin','Score','DateNew']].sort_values(by=['HomeTeam', 'AwayTeam', 'DateNew'], 
                        ascending = False).groupby(['HomeTeam','AwayTeam']).head(3)

recent3_cnt = recent3.groupby(["HomeTeam","AwayTeam", "WhoWin"]).size().reset_index().rename(columns = {0:'count'})
recent3 = pd.merge(recent3, recent3_cnt, on=['HomeTeam','AwayTeam','WhoWin'])
recent3["pctg"] = recent3["count"]/3
recent3["period"] = "recent3"
recent3.to_csv("recentWinning.csv")


recent5 = matchup_all[['HomeTeam','AwayTeam','WhoWin','Score','DateNew']].sort_values(by=['HomeTeam', 'AwayTeam', 'DateNew'], 
                        ascending = False).groupby(['HomeTeam','AwayTeam']).head(5)
recent5_cnt = recent5.groupby(["HomeTeam","AwayTeam", "WhoWin"]).size().reset_index().rename(columns = {0:'count'})
recent5 = pd.merge(recent5, recent5_cnt, on=['HomeTeam','AwayTeam','WhoWin'])
recent5["pctg"] = recent5["count"]/5
recent5["period"] = "recent5"
recent5.to_csv("recentWinning.csv", mode='a')


recent10 = matchup_all[['HomeTeam','AwayTeam','WhoWin','Score','DateNew']].sort_values(by=['HomeTeam', 'AwayTeam', 'DateNew'], 
                        ascending = False).groupby(['HomeTeam','AwayTeam']).head(10)
recent10_cnt = recent10.groupby(["HomeTeam","AwayTeam", "WhoWin"]).size().reset_index().rename(columns = {0:'count'})
recent10 = pd.merge(recent10, recent10_cnt, on=['HomeTeam','AwayTeam','WhoWin'])
recent10["pctg"] = recent10["count"]/10
recent10["period"] = "recent10"
recent10.to_csv("recentWinning.csv", mode='a')

recentWinning = pd.concat([recent3, recent5,recent10], sort = False)
recentWinning = recentWinning.drop_duplicates(subset=['HomeTeam','AwayTeam','WhoWin','pctg','count','period'])

recentWinning.to_csv("recentWinning.csv")


