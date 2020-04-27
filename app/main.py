import json

import pokebase as pb
import requests

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World from Flask"


@app.route("/pokemon/<name>")
def pokeroute(name):
    # Grab the pokemon
    pokemon = pb.pokemon(name)
    print(pokemon.species.name)

    # The descriptions are contained in the species
    species = pb.pokemon_species(pokemon.species.name)
    print(species)
    print(species.flavor_text_entries)

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
    response = requests.post("https://api.funtranslations.com/translate/shakespeare.json", data={"text": flavour_text})
    data = json.loads(response.content.decode(response.encoding))

    shakeperian_flavor_text = data["contents"]["translated"]

    api_response = {
        "name": pokemon.name,
        "description": shakeperian_flavor_text,

    }

    return api_response


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)


# def application(env, start_response):
#     version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
#     start_response("200 OK", [("Content-Type", "text/plain")])
#     message = "Hello World from a default Nginx uWSGI Python {} app in a Docker container (default)".format(
#         version
#     )
#     return [message.encode("utf-8")]
