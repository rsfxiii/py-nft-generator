""" Main process module - Generates layered image and metadata files """

import json
import os
import random
from typing import Type


from PIL import Image

from config import layers
from src import read_yaml_config


def make_dirs():
    """Creates the directories to store final images and later on, their corresponding json data. If
    the folders already exist, print to confirm and continue with the program.
    """
    print('Creating build directories')
    build_dirs = ['build', 'build/images', 'build/json']

    for _dir in build_dirs:
        if not os.path.isdir(_dir):
            print(f'Directory does not yet exist; creating {_dir}')
            os.mkdir(_dir)

    print('Build directories created')

# TODO: Edit/rewrite loop for non-required layers
def join_layers(assets: str) -> list:
    """Loops through each layer folder and chooses
        a layer from each folder based on the given
        rarity weights. It then appends all the paths
        to a list which act as the final layers for the image.
    """
    final_layers = []

    # For each layer in the config file:
    for layer in layers:

        # Joins absolute path with each layer directory for use in next step
        layer_path = os.path.join(assets, layer['folder'])

        # Sorts images into alphebetical order for use with rarities
        sorted_layers = sorted(os.listdir(layer_path))

        # Choose an image from the given subdirectory based on rarities
        img = random.choices(sorted_layers, weights=(layer['rarities']))

        # Store each chosen image path to a list
        final_layers.append(os.path.join(layer_path, img[0]))

    final_layers = tuple(final_layers)
    return final_layers


def create_metadata(description: str, token_name: str, edition: int, final_layers: list):
    """Takes in some user data, along with the layers of the image
        and create a metadata json for the image. The json object
        can be used to provide token data to IPFS or third-party websites such as OpenSea.
    """

    metadata = {
        'name': f'{token_name} #{edition}',
        'description': description,
        'image': f'ipfs://baseURI/{edition}.png',
        'edition': edition,
        'attributes': [
            #{'trait_type': '', 'value': ''},
            #{'trait_type': '', 'value': ''},
            #{'trait_type': '', 'value': ''}
        ]
    }

    for layer in final_layers:

        intemediary_dict = {}
        split_data = layer.split('/')

        intemediary_dict['trait_type'] = split_data[-2]
        intemediary_dict['value'] = split_data[-1].replace('.png', '')

        metadata['attributes'].append(intemediary_dict)

    with open(f'build/json/{edition}.json', 'w', encoding='utf-8') as outfile:
        json.dump(metadata, outfile, indent=2)


def create_image(token_name: str, edition: int, final_layers: list):
    """Takes a list of final layers, and pastes them all onto the background image to create one
    final image. Saves it in the images folder."""

    # Sets the background layer
    background_layer = Image.open(final_layers[0])

    # Adds each layer to the background
    for filepath in final_layers[1:]:
        img = Image.open(filepath)
        background_layer.paste(img, img)

    background_layer.save(f'build/images/{token_name}-{edition}.png')


def main(config: dict):
    """Takes inputs for the desired images. Creates a build directory, edition counter, then loops
    through for the desired amount. DNA keeps track of each created image to avoid duplicates."""

    token_name = config['token']['name']
    description = config['token']['description']
    amount = config['token']['amount']
    
    assets_path = config['assets_directory']
    
    edition = 0
    dna_set = set()

    make_dirs()
    assets_directory = os.path.join(os.getcwd(), assets_path)

    for _ in range(amount):

        final_layers = join_layers(assets_directory)

        if final_layers in dna_set:

            print(f'DNA already exists! Retrying token {edition}')
            continue

        create_metadata(description, token_name, edition, final_layers)
        create_image(token_name, edition, final_layers)
        dna_set.add(final_layers)
        edition += 1

    print('Image creation complete')


if __name__ == '__main__':
    config = read_yaml_config('config.yaml')
    main(config)
