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
    protocol: str = typer.Option(
        default="mongodb", envvar="MONGO_PROTOCOL"
    ),
    host: str = typer.Option(
        default="localhost:27017", envvar="MONGO_HOST"
    ),
    username: str = typer.Option(
        default="root", envvar="MONGO_USERNAME"
    ),
    password: str = typer.Option(
        default="1234", envvar="MONGO_PASSWORD"
    ),
    auth_source: str = typer.Option(
        default="admin", envvar="MONGO_AUTH_SOURCE"
    ),
    architecture: str = typer.Option(
        default="standalone", envvar="MONGO_ARCHITECTURE"
    ),
    replica_set_name: str = typer.Option(
        default="rs0", envvar="MONGO_REPLICA_SET_NAME"
    ),
    tls: bool = typer.Option(
        default=False, envvar="MONGO_TLS"
    ),
    ssl: bool = typer.Option(
        default=False, envvar="MONGO_SSL"
    ),
    timeout: int = 60,
):
    # Example: mongodb://<username>:<password>@mongo:27017/<db_name>?authSource=admin
    url = (
        f"{protocol}://{username}:{password}@"
        f"{host}/?authSource={auth_source}"
    )
    if architecture == "replicaset":
        url += f"&replicaSet={replica_set_name}"
    if not tls:
        url += "&tls=false"
    if not ssl:
        url += "&ssl=false"
    
    print(f"Testing mongo connection: {url.replace(password, '****')}")

    client = pymongo.MongoClient(url)

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
