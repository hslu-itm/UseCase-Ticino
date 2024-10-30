
To generate the swissboundaries3d_2024-01_2056_5728_as_WSG84.json I used qgis to reproject the swissboundaries3d_2024-01_2056_5728.shp to WSG84 and save it to geojson format.

To extract the municipalites that make up the Tourism districts use - generate_ticino_districts.py . 

The generates the output directory that contains an overall json file (all districts for Ticino) and a indiviual json file per Tourism district.

create a venv (virtual enviroment) using the requirments.txt file using the following commands:

    >python3 -m venv ./venv

    source the activation script in the virtual environment
    >source venv/bin/activate

    populate the venv with appropriate packages
    >pip install -r requirements.txt

    run the script
    >python generate_ticino_districts.py
