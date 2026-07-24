def print_patient(patient_data):

    print("\n========== Patient Monitor ==========\n")

    order=[

        "HR",

        "BP",

        "RESP",

        "SP02",

        "PULSE"

    ]

    for key in order:

        value=patient_data.get(

            key,

            "Not Detected"

        )

        print(f"{key:<6}: {value}")

    print("\n====================================")