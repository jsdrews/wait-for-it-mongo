import sys
import datetime

import typer
import pymongo


def test_connection(client: pymongo.MongoClient) -> bool:
    try:
        client.list_databases()
        return True
    except pymongo.errors.OperationFailure as err:
        print(f"Error connection to database: {err}")
        sys.exit(1)
    except pymongo.errors.ServerSelectionTimeoutError:
        return False
        

def main(
    db_uri: str = typer.Option(
        default="mongodb://localhost:27017", envvar="DB_URI"
    ),
    username: str = typer.Option(
        default=None, envvar="DB_ROOT_USERNAME"
    ),
    password: str = typer.Option(
        default=None, envvar="DB_ROOT_PASSWORD"
    ),
    timeout: int = 60,
):
    # Example: mongodb://<username>:<password>@mongo:27017/<db_name>?authSource=admin
    print(f"Testing mongo connection: {db_uri}")

    client = pymongo.MongoClient(
        db_uri,
        username=username,
        password=password,
    )

    timeout_obj = datetime.timedelta(seconds=timeout)
    then = datetime.datetime.utcnow()
    while not test_connection(client):
        now = datetime.datetime.utcnow()
        elapsed = now - then
        if now - then >= timeout_obj:
            print(
                f"We have exceeded the timeout limit: {elapsed.total_seconds()} of {timeout}s ..."
            )
            sys.exit(1)

    now = datetime.datetime.utcnow()
    total_elapsed = now - then
    print(f"Connection achieved after {total_elapsed.total_seconds()}s")


def run():
    typer.run(main)
