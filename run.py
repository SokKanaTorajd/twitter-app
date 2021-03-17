from crawlers.twitter_crawler import tweet_crawler

keyword = 'bankbri_id'
start_date= '2021-03-07'
tweet_crawler(keyword,start_date, n=10)
print('data inserted')


