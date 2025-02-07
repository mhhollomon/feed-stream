# python ./reader_main.py

from src.reader.stream_reader import create_websocket, create_periodic

import logging
import rel

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(name)s:%(levelname)s - %(message)s')

# don't currently need all the stuff from the database
logging.getLogger('peewee').setLevel(logging.INFO)

if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = create_websocket()

    # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    ws.run_forever(dispatcher=rel, reconnect=5) 
    
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    create_periodic()
    rel.dispatch()