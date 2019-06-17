from bot.crawl_comments import crawl_predictions

user_predictions = crawl_predictions("m1", "af9yq5")

for p in user_predictions:
    print(p)
    print("-----")

