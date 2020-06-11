import json

import pokebase as pb
import requests

from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# from flask import Flask
# app = Flask(__name__)


def translate_text_shakespearian(text: str):
    """
    Function for translating text into shakespearian text via API call

    Also helps in mocking out the tests
    """
    response = requests.post("https://api.funtranslations.com/translate/shakespeare.json", data={"text": text})
    data = json.loads(response.content.decode(response.encoding))

    try:
        translated_text = data["contents"]["translated"]
    except Exception as e:
        print(data)
        print(e)
        return "Rate limit exceeded"

    return translated_text


# To enable testing of whether the app is available or not
@app.route("/")
def hello():
    return "Hello World from Flask"


@app.route("/pokemon/<name>")
@cross_origin()
def pokeroute(name):
    # Grab the pokemon
    pokemon = pb.pokemon(name)

    # The descriptions are contained in the species
    species = pb.pokemon_species(pokemon.species.name)

    # Grab one of the english text flavour entries
    flavour_text = ""
    flavour_text_entries = species.flavor_text_entries  # Alias because I'm British
    # This grabs the first english flavour text entry we find
    for flavour_text_entry in flavour_text_entries:
        if flavour_text_entry.language.name == "en":
            flavour_text = flavour_text_entry.flavor_text

    if not flavour_text:
        # I'm sure flask has some error returns of it's own, so find them
        raise ValueError(f"No English entry for the species {species.name}")

    # Now call the shakespearian translator
    shakesperian_flavour_text = translate_text_shakespearian(flavour_text)

    api_response = {
        "name": pokemon.name,
        "description": shakesperian_flavour_text,
    }

    return api_response


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
