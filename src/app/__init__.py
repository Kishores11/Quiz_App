from flask import Flask


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://hello_flask:hello_flask@localhost/testdb"
app.config["SECRET_KEY"] = "hgfufhd873h"

try:
    from app import models, routes

    models.db.configure_mappers()
    models.db.create_all()
    models.db.session.commit()
except:
    import traceback

    traceback.print_exc()
