import json
import unittest
from unittest.mock import patch

from app.main import app


class DictObject(object):
    """Because the API wrapper library transforms indexes"""
    def __init__(self, data):
        self._data = data

    def __getattr__(self, item):
        """We can't use any self.attr calls, because we'd have a chain reaction"""
        if item in super().__getattribute__("_data"):
            if isinstance(super().__getattribute__("_data")[item], dict):
                return DictObject(super().__getattribute__("_data")[item])
            else:
                return super().__getattribute__("_data")[item]
        else:
            raise AttributeError(f"{item} not found in this thing")

    def __str__(self):
        return str(super().__getattribute__("_data"))

    def __repr__(self):
        return self.__str__()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_root(self):
        rv = self.app.get('/')
        assert b"Hello World from Flask" in rv.data

    @patch('app.main.translate_text_shakespearian')
    @patch('pokebase.pokemon_species')
    @patch('pokebase.pokemon')
    def test_pokemon(self, mock_pokemon, mock_pokemon_species, mock_shakespearian):
        mock_pokemon.return_value = DictObject({
            "name": "charmander",
            "species": {
                "name": "charmander",
                "url": "blah blah blah"
            }
        })

        mock_pokemon_species.return_value = DictObject({
            "name": "charmander",
            "flavor_text_entries": [
                DictObject({
                    "language": {"name": "fr"},
                    "flavor_text": "Ma francais est tres mal",
                }),
                DictObject({
                    "language": {"name": "en"},
                    "flavor_text": "This describes the data I give in this test",
                }),
            ]
        })

        mock_shakespearian.return_value = "Verily, this describeth the data I giveth in this test."

        rv = self.app.get('/pokemon/charmander')

        data = json.loads(rv.data.decode('utf-8'))

        # Assert we get the right answer
        assert data == {
            "name": "charmander",
            "description": "Verily, this describeth the data I giveth in this test."
        }

        # Also assert we got the right intermediate calls
        mock_pokemon.assert_called_with("charmander")

        mock_pokemon_species.assert_called_with("charmander")
