from sqlalchemy import create_engine, Table, Column, Integer, Boolean, String, MetaData, text
from sqlalchemy.orm import sessionmaker, declarative_base
import requests
import os

engine = create_engine('sqlite:///database.db')
meta = MetaData()
meta.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

with engine.connect() as conn:
    internalId = conn.execute(text("SELECT internalId FROM pokemon"))
    names = conn.execute(text("SELECT smogon FROM pokemon"))
    form = conn.execute(text("SELECT formId FROM pokemon"))

    pokemon = [(id[0], name[0], formId[0]) for id, name, formId in zip(internalId, names, form)]

base_url = 'https://pokeapi.co/api/v2/pokemon/'

total = len(pokemon)


for id, name, form in pokemon:

    print(f"Starting {id}/{total}")

    response = requests.get(base_url + name)
    if response.status_code == 200:
        data = response.json()

        with open('static/sprites/pokemon/'+str(id)+'.png', 'wb') as file:
            if not form:
                try:
                    asset_response = requests.get(data['sprites']['front_default'])
                except:
                    print(f"\tCould not obtain url.")
                    continue
            elif form == 'f':
                try:
                    asset_response = requests.get(data['sprites']['front_female'])
                except:
                    asset_response = requests.get(data['sprites']['front_default'])  
            else:
                try:
                    asset_response = requests.get(data['sprites']['front_default'])
                except:
                    print(f"\tCould not obtain url.")
                    continue

            if asset_response.status_code == 200:
                file.write(asset_response.content)
                print(f"\tfinished {id}: {name}")
            else:
                print(f"\tFailed to download. Id {id}, name {name}, form {form}.")

    else:
        print(f"\tRequest FAILED for id {id}, name {name}, form {form}.")

