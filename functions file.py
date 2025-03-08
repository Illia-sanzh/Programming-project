import requests
from bs4 import BeautifulSoup
## defining a class for the reviews
class Ceneo_reviews:
    def __init__(self, opinion_id, user_name, recommendation, stars, content, advantages, disadvantages, helpful, helpful_not, publish_date, purchase_date):
        self.opinion_id = opinion_id
        self.user_name = user_name
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.advantages = advantages
        self.disadvantages = disadvantages
        self.helpful = helpful
        self.helpful_not = helpful_not
        self.publish_date = publish_date
        self.purchase_date = purchase_date
    def print_atributes(self):
        print(f"opinion_id: {self.opinion_id}")
        print(f"user_name: {self.user_name}")
        print(f"recommendation: {self.recommendation}")
        print(f"stars: {self.stars}")
        print(f"content: {self.content}")
        print(f"advantages: {self.advantages}")
        print(f"disadvantages: {self.disadvantages}")
        print(f"helpful: {self.helpful}")
        print(f"helpful_not: {self.helpful_not}")
        print(f"publish_date: {self.publish_date}")
        print(f"purchase_date: {self.purchase_date}")



# function to fetch all the attribs
def fetch_comment(id):
    base_url = f'https://www.ceneo.pl/{id}/opinie-'
    all_reviews = []
    first_url = base_url + '1'
    soup = BeautifulSoup(requests.get(first_url).content, "html.parser")
    review_count = int(soup.find('div', class_="score-extend__review").get_text().strip().split(' ')[0])
    num_pages = (review_count // 10) + (1 if review_count % 10 > 0 else 0)
    for page in range(1, num_pages+1):
        url = base_url + str(page)
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        for link in soup.find_all("div", class_="user-post user-post__card js_product-review"):
            opinion_id = link['data-entry-id']
            user_name = link.find("span", class_="user-post__author-name")
            if user_name is not None:
                user_name = user_name.get_text().strip()
            reccomendation = link.find("em", class_="recommended")
            if reccomendation is not None:
                reccomendation = reccomendation.get_text().strip()
            else:
                reccomendation = 'Nie polecam'
            stars = link.find("span", class_="user-post__score-count")
            if stars is not None:
                stars = stars.get_text().strip()
            content = link.find("div", class_="user-post__text")
            if content is not None:
                content = content.get_text().strip()
            advantages_l = link.find_all("div", class_="review-feature__item review-feature__item--positive")
            advantages = ""
            if advantages_l is not None:
                for advantage in advantages_l:
                    advantages += advantage.get_text().strip() + ' '
            else:
                advantages = 'None'
            disadvantages_l = link.find_all("div", class_="review-feature__item review-feature__item--negative")
            disadvantages = ""
            if disadvantages_l is not None:
                for disadvantage in disadvantages_l:
                    disadvantages += disadvantage.get_text().strip() + ' '
            else:
                disadvantages = 'None'
            helpful = link.find("button", class_="vote-yes js_product-review-vote js_vote-yes")['data-total-vote']
            helpful_not = link.find("button", class_="vote-no js_product-review-vote js_vote-no")['data-total-vote']
            time_a = link.find("time")
            publish_date = time_a['datetime']
            time_b = time_a.find_next("time")
            purchase_date = time_b['datetime']
            opinion_obj = Ceneo_reviews(opinion_id, user_name, reccomendation, stars, content, advantages, disadvantages, helpful, helpful_not, publish_date, purchase_date)
            all_reviews.append(opinion_obj)
    return all_reviews
            

if __name__ == "__main__":
    reviews = fetch_comment("97574473")
    for review in reviews:
        print(review.print_atributes())

