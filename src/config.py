from dotenv import dotenv_values

_config : dict = dotenv_values(".env")


DB_FILE = _config['DATABASE_LOCATION']

BIND_ADDR = _config['BIND_INTERFACE']

BIND_PORT = _config['BIND_PORT']

HOSTNAME = _config['SERVICE_HOST']

SERVICE_DID = f"did:web:{HOSTNAME}"

OWNER_DID = _config['OWNER_DID']