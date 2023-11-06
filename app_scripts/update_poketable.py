import json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean

## Add a search for pokemon.json and update it.
## Source: supereffective.gg github table.

base_sprite = 'static/sprites/'

####
# LOAD JSON
with open('archive/pokemon.json', 'r') as j:
    data = json.loads(j.read())

columns_to_keep = ['name', 'dexNum', 'refs', 'abilities', 'formId', 'isFemaleForm']

filtered_data = [{column: record[column] for column in columns_to_keep if column in record} for record in data]

for row in filtered_data:
    if row['abilities']['hidden'] == None:
        row['abilities'] = row['abilities']['primary']
        row['hiddenAbility'] = False
    else:
        row['abilities'] = row['abilities']['hidden']
        row['hiddenAbility'] = True
    
    row['smogon'] = row['refs']['smogon']
    del row['refs']

    row['sprite'] = base_sprite + row['smogon']

    row['isFemale'] = row['isFemaleForm']
    del row['isFemaleForm']

####
# LOAD SQL
engine = create_engine('sqlite:///database.db')
meta = MetaData()
meta.create_all(engine)

# Create table.
pokemon_table = Table('pokemon', meta,
                    Column('internalId', Integer, primary_key=True, autoincrement=True),
                    Column('name', String),
                    Column('dexNum', Integer),
                    Column('formId', String),
                    Column('smogon', String),
                    Column('hiddenAbility', Boolean),
                    Column('abilities', String),
                    Column('sprite', String))

pokemon_table.create(engine)

# Load data.
with engine.connect() as conn:
    for row in filtered_data:
        insert_query = pokemon_table.insert().values(
                                    name = row['name'],
                                    dexNum = row['dexNum'],
                                    formId = row['formId'],
                                    smogon = row['smogon'],
                                    hiddenAbility = row['hiddenAbility'],
                                    abilities = row['abilities'],
                                    sprite = row['sprite']
                                    )
        conn.execute(insert_query)
    
    conn.commit()
    conn.close()

print("Success rewriting table.")