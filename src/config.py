from dotenv import dotenv_values

_config : dict = dotenv_values()


DB_FILE = _config['DATABASE_LOCATION']

HOSTNAME = _config['SERVICE_HOST']

SERVICE_DID = f"did:web:{HOSTNAME}"

OWNER_DID = _config['OWNER_DID']

WAITRESS_LISTEN = _config.get('WAITRESS_LISTEN') or 'localhost:3000'

WAITRESS_PREFIX = _config.get('WAITRESS_PREFIX')