from main import app, db
from flask_migrate import Migrate

app = app 
db = db
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db}
