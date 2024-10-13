#!/usr/bin/env python

import feedparser
import time
from datetime import datetime
from progress_verbose import print_progress_bar

RECORD_SUMMARY = True
RECORD_TITLE_ONLY = not RECORD_SUMMARY

def crawl_from_cna():
    time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    rss_list = [
        {'source': 'cna_asia', 'url': 'https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6511'},
        {'source': 'cna_sgp', 'url': 'https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=10416'},
        #{'source': 'cna_world', 'url': 'https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6311'},
    ]

    for rss in rss_list:
        tick = time.time()
        print("Start crawling news from RSS source: " + rss['source'] + " (" + rss['url'] + ")")
        feeds = feedparser.parse(rss['url'])
        output_file_name = 'data/data_collection/' + rss['source'] + '_' + time_str + '.log'
        with open(output_file_name,"w+", encoding='utf8') as f:
            entries = feeds['entries']
            print_progress_bar(0, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
            for feed_index, feed in enumerate(entries):
                if RECORD_SUMMARY and 'summary' in feed:
                    f.write(merge_title_and_summary(feed['title'], feed['summary']))
                else:
                    f.write(feed['title'])                
                f.write('\n')
                print_progress_bar(feed_index + 1, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
        elapsed_time = time.time() - tick  
        print("Finished crawling " + str(len(entries)) + " news from the source. Elapsed time: " + "{:.2f}".format(elapsed_time) + "s")


def crawl_from_bbc():
    time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    rss_list = [
        #{'source': 'bbc_top', 'url': 'https://feeds.bbci.co.uk/news/rss.xml'},
        {'source': 'bbc_world', 'url': 'https://feeds.bbci.co.uk/news/world/rss.xml'},
        {'source': 'bbc_business', 'url': 'https://feeds.bbci.co.uk/news/business/rss.xml'},
        {'source': 'bbc_politics', 'url': 'https://feeds.bbci.co.uk/news/politics/rss.xml'}, 
        {'source': 'bbc_ent_n_arts', 'url': 'https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml'},
        {'source': 'bbc_health', 'url': 'https://feeds.bbci.co.uk/news/health/rss.xml'}, 
        {'source': 'bbc_sci_n_environ', 'url': 'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml'},
        {'source': 'bbc_education', 'url': 'https://feeds.bbci.co.uk/news/education/rss.xml'}, 
        {'source': 'bbc_tech', 'url': 'https://feeds.bbci.co.uk/news/technology/rss.xml'}, 
    ]

    for rss in rss_list:
        tick = time.time()
        print("Start crawling news from RSS source: " + rss['source'] + " (" + rss['url'] + ")")
        feeds = feedparser.parse(rss['url'])
        output_file_name = 'data/data_collection/' + rss['source'] + '_' + time_str + '.log'
        with open(output_file_name,"w+", encoding='utf8') as f:
            entries = feeds['entries']
            print_progress_bar(0, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
            for feed_index, feed in enumerate(entries):
                if RECORD_SUMMARY and 'summary' in feed.keys():
                    f.write(merge_title_and_summary(feed['title'], feed['summary']))                    
                else:
                    f.write(feed['title'])
                f.write('\n')
                print_progress_bar(feed_index + 1, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
        elapsed_time = time.time() - tick  
        print("Finished crawling " + str(len(entries)) + " news from the source. Elapsed time: " + "{:.2f}".format(elapsed_time) + "s")


def crawl_from_nyt():
    time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    rss_list = [
        {'source': 'nyt_world', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'},
        {'source': 'nyt_business', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/Business.xml'},
        {'source': 'nyt_tech', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml'},
        {'source': 'nyt_sports', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml'},
        {'source': 'nyt_science', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/Science.xml'},
        {'source': 'nyt_health', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/Health.xml'},
    ]

    for rss in rss_list:
        tick = time.time()
        print("Start crawling news from RSS source: " + rss['source'] + " (" + rss['url'] + ")")
        feeds = feedparser.parse(rss['url'])
        output_file_name = 'data/data_collection/' + rss['source'] + '_' + time_str + '.log'
        with open(output_file_name,"w+", encoding='utf8') as f:
            entries = feeds['entries']
            print_progress_bar(0, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
            for feed_index, feed in enumerate(entries):
                if RECORD_SUMMARY and 'summary' in feed.keys():
                    f.write(merge_title_and_summary(feed['title'], feed['summary']))                    
                else:
                    f.write(feed['title'])
                f.write('\n')
                print_progress_bar(feed_index + 1, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
        elapsed_time = time.time() - tick  
        print("Finished crawling " + str(len(entries)) + " news from the source. Elapsed time: " + "{:.2f}".format(elapsed_time) + "s")


# Not accessible
def crawl_from_reuters():
    time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    rss_list = [
        {'source': 'reuters_biz_n_finance', 'url': 'https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best'},
        {'source': 'reuters_politics', 'url': 'https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best'},
        {'source': 'reuters_environment', 'url': 'https://www.reutersagency.com/feed/?best-topics=environment&post_type=best'},
        {'source': 'reuters_tech', 'url': 'https://www.reutersagency.com/feed/?best-topics=tech&post_type=best'},
        {'source': 'reuters_human_interest', 'url': 'https://www.reutersagency.com/feed/?best-topics=human-interest&post_type=best'},
        {'source': 'reuters_lifestyle', 'url': 'https://www.reutersagency.com/feed/?best-topics=lifestyle-entertainment&post_type=best'},
        {'source': 'reuters_sports', 'url': 'https://www.reutersagency.com/feed/?best-topics=sports&post_type=best'},
        {'source': 'reuters_health', 'url': 'https://www.reutersagency.com/feed/?best-topics=health&post_type=best'},
    ]

    for rss in rss_list:
        tick = time.time()
        print("Start crawling news from RSS source: " + rss['source'] + " (" + rss['url'] + ")")
        feeds = feedparser.parse(rss['url'])
        output_file_name = 'data/data_collection/' + rss['source'] + '_' + time_str + '.log'
        with open(output_file_name,"w+", encoding='utf8') as f:
            entries = feeds['entries']
            print_progress_bar(0, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
            for feed_index, feed in enumerate(entries):
                # Reuters does not provide a summary on its RSS source
                f.write(feed['title'])
                f.write('\n')
                print_progress_bar(feed_index + 1, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
        elapsed_time = time.time() - tick  
        print("Finished crawling " + str(len(entries)) + " news from the source. Elapsed time: " + "{:.2f}".format(elapsed_time) + "s")


def crawl_from_fox():
    time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    rss_list = [
        {'source': 'fox_world', 'url': 'https://moxie.foxnews.com/google-publisher/world.xml'},
        {'source': 'fox_politics', 'url': 'https://moxie.foxnews.com/google-publisher/politics.xml'},
        {'source': 'fox_sports', 'url': 'https://moxie.foxnews.com/google-publisher/sports.xml'},
        {'source': 'fox_health', 'url': 'https://moxie.foxnews.com/google-publisher/health.xml'},
        {'source': 'fox_science', 'url': 'https://moxie.foxnews.com/google-publisher/science.xml'},
    ]
    

    for rss_index, rss in enumerate(rss_list):
        tick = time.time()
        print("Start crawling news from RSS source: " + rss['source'] + " (" + rss['url'] + ")")
        feeds = feedparser.parse(rss['url'])
        output_file_name = 'data/data_collection/' + rss['source'] + '_' + time_str + '.log'
        with open(output_file_name,"w+", encoding='utf8') as f:
            entries = feeds['entries']
            print_progress_bar(0, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
            for feed_index, feed in enumerate(entries):
                if RECORD_SUMMARY and 'summary' in feed.keys():
                    f.write(merge_title_and_summary(feed['title'], feed['summary']))                    
                else:
                    f.write(feed['title'])
                f.write('\n')
                print_progress_bar(feed_index + 1, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
        elapsed_time = time.time() - tick  
        print("Finished crawling " + str(len(entries)) + " news from the source. Elapsed time: " + "{:.2f}".format(elapsed_time) + "s")


def crawl_from_google():
    time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    rss_list = [
        {'source': 'google_news_us', 'url': 'https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en'},
        {'source': 'google_news_uk', 'url': 'https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en'},
        {'source': 'google_news_ca', 'url': 'https://news.google.com/rss?gl=CA&hl=en-CA&ceid=CA:en'},
        {'source': 'google_news_au', 'url': 'https://news.google.com/rss?gl=AU&hl=en-AU&ceid=AU:en'},
        {'source': 'google_news_nz', 'url': 'https://news.google.com/rss?gl=NZ&hl=en-NZ&ceid=NZ:en'},
        {'source': 'google_news_za', 'url': 'https://news.google.com/rss?gl=ZA&hl=en-ZA&ceid=ZA:en'},
        {'source': 'google_news_sg', 'url': 'https://news.google.com/rss?hl=en-SG&gl=SG&ceid=SG:en'},
    ]
    

    for rss_index, rss in enumerate(rss_list):
        tick = time.time()
        print("Start crawling news from RSS source: " + rss['source'] + " (" + rss['url'] + ")")
        feeds = feedparser.parse(rss['url'])
        output_file_name = 'data/data_collection/' + rss['source'] + '_' + time_str + '.log'
        with open(output_file_name,"w+", encoding='utf8') as f:
            entries = feeds['entries']
            print_progress_bar(0, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
            for feed_index, feed in enumerate(entries):
                # Reuters does not provide a summary on its RSS source
                title_str = feed['title']
                if title_str.rfind("-") > 0:
                    title_str = title_str[:title_str.rfind("-")]
                f.write(title_str)
                f.write('\n')
                print_progress_bar(feed_index + 1, len(entries), prefix = 'Progress:', suffix = 'Complete', length = 50)
        elapsed_time = time.time() - tick  
        print("Finished crawling " + str(len(entries)) + " news from the source. Elapsed time: " + "{:.2f}".format(elapsed_time) + "s")


def merge_title_and_summary(title, summary):
    # check if the title is a substring of the summary, or identical to the summary
    if title in summary:
        return summary
    else:
        if title.endswith(".") or title.endswith("!") or title.endswith("?"):
            return title + " " + summary
        else:
            return title + ": " + summary


def collect_feed():
    if RECORD_SUMMARY:
        print(">>> Record summary mode is ON. Both the title and short summary of each news will be recorded. ")
    else:
        print(">>> Record summary mode if OFF, only news title will be recorded. ")
    
    crawl_from_bbc()
    crawl_from_fox()
    crawl_from_google()
    crawl_from_nyt()


if __name__ == "__main__":
    collect_feed()