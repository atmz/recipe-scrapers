from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, get_yields


class NYTimes(AbstractScraper):

    @classmethod
    def host(self):
        return 'cooking.nytimes.com'

    def title(self):
        return normalize_string(self.soup.find('h1', {'class': 'recipe-title'}).get_text())

    def total_time(self):
        return sum([
            get_minutes(self.soup.find(
                'span',
                {'class': 'recipe-details__cooking-time-prep'}
            ).find('span')),

            get_minutes(self.soup.find(
                'span',
                {'class': 'recipe-details__cooking-time-cook'}
            ).find('span'))
        ])

    def get_yields(self):
        return normalize_string(self.soup.find(
            'span',
            {'class': 'recipe-yield-value'}
        ))

    def image(self):
        image = self.soup.find(
            'img',
            {'itemprop': 'image', 'src': True}
        )
        return image['src'] if image else None

    def ingredients(self):
        ingredients = self.soup.find( 'ul',   
            {'class': "recipe-ingredients"})
        ingredients = ingredients.findAll( 'li')

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients
        ]

    def instructions(self):
        instructions = self.soup.findAll(
            'li',
            {'itemprop': 'recipeInstructions'}
        )

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions
        ])
