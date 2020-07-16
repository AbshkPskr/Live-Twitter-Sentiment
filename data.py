# import pandas as pd
# import sqlite3

# conn = sqlite3.connect('twitter.db')
# c = conn.cursor()

# df = pd.read_sql("select * from sentiment",conn)
# df['smoothed_sentiment'] = df['sentiment'].rolling(int(len(df)/5)).mean()
# df.dropna(inplace=True)


# print(df)

import threading 
import twitter
  
class thread(threading.Thread): 
    def __init__(self, thread_name, thread_ID): 
        threading.Thread.__init__(self) 
        self.thread_name = thread_name 
        self.thread_ID = thread_ID 
    def run(self): 
        print(str(self.thread_name) +"  "+ str(self.thread_ID)); 
        twitter.get_tweets()
  
thread1 = thread("GFG", 1000) 
thread2 = thread("GeeksforGeeks", 2000); 
  
thread1.start() 

  
print("Exit") 

