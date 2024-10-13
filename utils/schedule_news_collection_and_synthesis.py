from datetime import datetime
import sched, time
from feed_collection import collect_feed
from sort_synthesis_news import sort_synthesis_news
from news_synthesis import synthesis_news

def do_something(scheduler): 
    # schedule the next task for every 24 hours
    scheduler.enter(86400, 1, do_something, (scheduler,))
    print("Task executed at " + datetime.now().strftime('%Y-%m-%d-%H%M%S'))
    print("Feed Collection in progress...")
    collect_feed()
    print("News Synthesis in progress...")
    synthesis_news()
    time.sleep(16)
    print("Cleansing the folder...")
    sort_synthesis_news()

if __name__ == "__main__":
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(0, 1, do_something, (my_scheduler,))
    my_scheduler.run()