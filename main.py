import requests
import json
from selenium import webdriver
from bs4 import BeautifulSoup


class Recipes:
    BASE_URI = 'https://api.spoonacular.com/recipes/complexSearch?number=1&apiKey=d44ec4adccbb4905a3b64b4becb783cd&fillIngredients=true'

    def __init__(self, recipe_name):
        self.recipe_name = recipe_name

    def get_recipe(self):
        full_url = f'{self.BASE_URI}&query={self.recipe_name}'
        response = requests.get(full_url)
        return json.loads(response.text)['results'][0]

    def get_main_ingredient(self):
        recipe = self.get_recipe()
        amounts = [ingredient['amount']
                   for ingredient in recipe['missedIngredients']]
        names = [ingredient['name']
                 for ingredient in recipe['missedIngredients']]

        main_ingredient_index = amounts.index(max(amounts))

        return names[main_ingredient_index]


class ScrapAllRecipes:

    BASE_URI = 'https://www.allrecipes.com/search?q='

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Remote(
            command_executor='http://localhost:3000/webdriver',
            options=chrome_options
        )

    def get_recipes(self, ingredient):
        full_url = f'{self.BASE_URI}{ingredient.replace(" ", "+")}'
        self.driver.get(full_url)
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        a_tags = soup.find_all("a", {
            "class": 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image'}, href=True)
        links = [a['href'] for a in a_tags]
        return links[:5]


def run():
    recipe = Recipes(recipe_name='pasta')
    scraper = ScrapAllRecipes()
    main_ingredient = recipe.get_main_ingredient()
    links = scraper.get_recipes(main_ingredient)
    for link in links:
        print(link)


if __name__ == '__main__':
    run()
