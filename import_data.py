import pandas as pd
from alive_progress import alive_bar
from db_config import get_redis_connection

r = get_redis_connection()


def empty_db():
    print('Emptying DataBase\n')
    r.flushdb()
    print('Done Emptying DB')


def import_data():
    file_path = (
        "//Users//ryan//Desktop//car_prices_trunc.csv"
    )

    # Read the CSV file
    df = pd.read_csv(file_path)
    # Ingest data into Redis
    print('Importing Data Into Redis\n')
    with alive_bar(len(df.index)) as bar:
        for index, row in df.iterrows():
            bar()
            # Using the index as part of the key for simplicity; consider a more meaningful key for production
            key = f'CarSale:{index}'
            # Convert row to a dict and store in Redis
            r.hset(key, mapping=row.to_dict())

    print('Data Import Complete')