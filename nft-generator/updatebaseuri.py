""" Retroactively replaces the JSON 'baseURI' file after it is known """

import json

def update_base_uri():
    """Takes an input of the metadata URI and amount of json files and updates
    all of the json files with the new URI. This is necessary for places like IPFS
    as you cannot get the URI until the images have been uploaded."""

    amount = (int(input('Enter the amount of json files to change\n')))
    new_uri = input('Copy and paste the image URI\n')

    edition = 1

    for _ in range(amount):

        json_path = f'build/json/{edition}.json'

        # TODO: These probably don't need to be two file operations separately
        # Opens json file
        with open(json_path, 'r', encoding='utf-8') as infile:

            # Load the opened json file into a Python dict
            data = json.load(infile)

            # Changes the necessary data in the now Python dictionary
            data['image'] = data['image'].replace('baseURI', new_uri)

        # Opens the original json file and writes the new data
        with open(json_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=2)

        edition += 1

    print('Base URIs Updated')


update_base_uri()
