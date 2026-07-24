import json

def save_json(patient_data):

    with open(

        "output/patient_data.json",

        "w"

    ) as f:

        json.dump(

            patient_data,

            f,

            indent=4

        )