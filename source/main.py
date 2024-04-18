import uvicorn

from tauvlo.server.persistence.configuration import CONFIG
from tauvlo.server.persistence.database import ORM
from tauvlo.server.webserver import app, ws

# needed global variable for external uvicorn launching
assert(app is not None)

# configure DB connection
ORM.configure_db_connection(CONFIG.db_connection_string,
                            json_serializer=ws.json_serializer)

if __name__ == "__main__":
    # debug app startup
    print("Starting application in debug mode")
    uvicorn.run("main:app", host=CONFIG.debug_ws_host, port=CONFIG.debug_ws_port, reload=True)
