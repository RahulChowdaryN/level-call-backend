from chalice import Chalice
from chalicelib.audit_app.audit_controller import audit_app
from chalicelib.roles.roles_controller import roles_app
from chalicelib.session_app.session_controller import session_app
from chalicelib.user_app.user_controller import user_app
from chalicelib.auth import auth_app
from chalicelib import global_auth


app = Chalice(app_name='sessions-app')

app.debug = True


@app.route('/', cors=global_auth.cors_config)
def index():
    return {'hello': 'world'}


# @app.route('/needs-auth', authorizer=auth_app.authorizer())
# def needs_auth():
#     return {'success': True}


app.register_blueprint(audit_app)
app.register_blueprint(roles_app)
app.register_blueprint(session_app)
app.register_blueprint(user_app)
app.register_blueprint(auth_app)
