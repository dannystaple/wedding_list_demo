from flask import Flask
from gift_list.views import gift_list

app = Flask(__name__)
app.register_blueprint(gift_list)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 20
