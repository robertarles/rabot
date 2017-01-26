from curator import Curator
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from newspaper import Article
from  newspaper.article import ArticleException
from pymongo import MongoClient

class Reporter:
    
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.rabot_db = self.client.rabot32
        self.hot_search_count_min = 500000

    def get_trends(self):
        driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
        driver.get("https://www.google.com/trends/hottrends")
        trends = driver.find_elements_by_css_selector("div.hottrends-single-trend-container")
        driver.close()
        trend_list = []
        # response = requests.get("https://www.google.com/trends/hottrends")
        # soup = BeautifulSoup(content, 'html.parser')
        # trends = soup.find_all("div")#, "hottrends-single-trend-container")
        for trend in trends:
            search_term = trend.find_element_by_css_selector("span.hottrends-single-trend-title").text
            article_href = trend.find_element_by_tag_name("a").get_attribute("href")
            search_count = trend.find_element_by_css_selector("span.hottrends-single-trend-info-line-number").text
            search_count = int(search_count.replace("+", "").replace(",", ""))
            trend_list.append({"search_term": search_term, "search_count": search_count, "href": article_href})
        curator = Curator()
        curator.process_trends(trend_list, ["`store`", "trends"], "rabot32")
        return trend_list

    def get_hot_trends(self):
        hot_trends = []
        trends_list = self.get_trends()
        for trend in trends_list:
            if trend["search_count"] >= self.hot_search_count_min:
                print(trend)
                hot_trends.append(trend)
        return hot_trends

    def post_articles(self, article_list):
        for article in article_list:
            url = article["href"]
            doc = Article(url)
            try:
                doc.download()
                doc.parse()
            except ArticleException:
                print("Exception getting article from url [{}]".format(url))
                return
            article["image"] = ""
            if doc.has_top_image():
                article["image"] = "<img src={}>".format(doc.top_image)
            article["title"] = doc.title
            article["source_title"] = "notYetSet"
            article["summary"] = article["image"] + doc.text[:300] + " ...</br>"
            self.post_article_api(article["href"], article)

    def post_article_api(self, siteurl, article):
        '''
        post an article to a wordpress site using the jetpack/wordpress api
        :param siteurl: urls of the site to post to
        :param article: the article object to post
        :return:

        '''
        # make sure we haven't already posted this article
        url_posted_count = self.rabot_db.posted_timely.find({"href": {"$eq": article["href"]}}).count()
        if url_posted_count > 0:
            print("already posted article [{}]".format(article["href"]))
            return
        title = article["title"]
        summary = article["summary"]
        summary += "<b>See the original posting at <a href='" + \
                  article["href"] + "'>" + article["title"] + "</a></b>"
        payload = {"title": title, "content": summary, "categories": article["source_title"]}
        headers = {"authorization": "BEARER ME6ofxetCuYR4)^53Jhq^n$W@j*ascOPy&)tL(3yNfgVhve5EpJhqxqkxkLvdXE9"}
        response = requests.post(
                                "https://public-api.wordpress.com/rest/v1/sites/122975976/posts/new",
                                data=json.dumps(payload),
                                headers=headers)
        if response.status_code == 200:
            db_result = self.rabot_db.posted_timely.insert_one(article)
            article["reposted"] = 1
        print("[DEBUG] post complete with response " + str(response.status_code))



if __name__ == "__main__":
    johnny_onthespot = Reporter()
    hot_trends_list = johnny_onthespot.get_hot_trends()
    johnny_onthespot.post_articles(hot_trends_list)
    # article = {"title": "Poodle Doop", "summary": "this is not about doodle poop, feel free to carry on", \
    #            "href": "http://robert.arles.us", "source_title": "title of source here"}
    # johnny_onthespot.post_article_api("",article)
