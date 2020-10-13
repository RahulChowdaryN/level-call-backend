from chalice import Chalice
from chalicelib import global_auth
from chalicelib.roles.roles_controller import roles_app
from chalicelib.audit_app.audit_controller import audit_app
from chalicelib.feedback_app.feedback_controller import feedback_app


app = Chalice(app_name='audit-feedback')


app.debug = True
_USER_AUDIT_DB = None
_SESSION_AUDIT_DB = None
_FEEDBACK_DB = None
_USER_ROLES_DB = None
_SESSION_ROLES_DB = None
_USER_ROLES = None
_SESSION_ROLES = None


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/api/custom-auth', methods=['GET'], authorizer=global_auth.authorizer)
def authenticated():
    return {"success": True}


app.register_blueprint(audit_app)
app.register_blueprint(feedback_app)
app.register_blueprint(roles_app)

