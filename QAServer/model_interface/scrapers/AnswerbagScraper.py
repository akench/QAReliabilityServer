import requests
from bs4 import BeautifulSoup

SELECTOR = '#main > div:nth-of-type(4) > div.col-md-5 > div > div.panel-body > div > div.col-md-9.col-lg-9 > table > tbody > tr:nth-of-type({}) > td:nth-of-type(2)'
FOLLOWERS_DIV_NUM = 4
FOLLOWING_DIV_NUM = 6

class AnswerbagParser():

    def __init__(self, username):
        self.username = username.lower()

    def get_user_stats(self):
        r = requests.get('http://answerbag.com/profile/{}'.format(self.username))
        html = r.text
        soup = BeautifulSoup(html, 'html5lib')

        followers = int(soup.select(SELECTOR.format(FOLLOWERS_DIV_NUM))[0].text)
        following = int(soup.select(SELECTOR.format(FOLLOWING_DIV_NUM))[0].text)

        return followers, following

if __name__ == '__main__':
    parser = AnswerbagParser('Bootsiebaby')
    followers, following = parser.get_user_stats()
    print(str(followers))
    print(str(following))