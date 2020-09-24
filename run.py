from flask import Flask
from gift_list.views import gift_list_bp

app = Flask(__name__)
app.register_blueprint(gift_list_bp)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 20
