import sqlalchemy as sa

class SQL:

    def __init__(self, drivername="postgresql", username="alumnodb", password="1234", host="localhost", database="si1"):
        connection_url = self._create_connection_URL(drivername, username, password, host, database)
        self.db_engine = sa.create_engine(connection_url, echo=False)

    def _create_connection_URL(self, drivername, username, password, host, database):
        connection_url = sa.engine.URL.create(drivername=drivername,
                                              username=username,
                                              password=password,
                                              host=host,
                                              database=database)
        return connection_url

    def _connect(self):
        self.db_conn = self.db_engine.connect()

    def _disconnect(self):
        self.db_conn.close()

    def _apply_select(self, query, params=None):
        if params:
            return list(self.db_conn.execute(sa.text(query), params))
        else:
            return list(self.db_conn.execute(sa.text(query)))

    def get_all_imdb_actors(self):
        self._connect()
        query = "SELECT * FROM imdb_actors;"
        results = self._apply_select(query)
        self._disconnect()
        return results

    def exist_actor(self, actor_name):
        self._connect()
        query = "SELECT * FROM imdb_actors WHERE actorname = :actor_name"
        params = {"actor_name": actor_name}
        results = self._apply_select(query, params)
        self._disconnect()
        return len(results) >= 1
