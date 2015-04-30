from flask import Flask,send_file,request
import StringIO
import base64
import io
import re
import urllib2
import qrcode
import json


path = dict()
path['method'] = '/root/.kiwivm-shadowsocks-encryption'
path['password'] = '/root/.kiwivm-shadowsocks-password'
path['port'] = '/root/.kiwivm-shadowsocks-port'

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_qrcode():
    if request.method == 'GET':
        if request.args.get('type', None) == "json":
            return json.dumps(get_ss_info())
        else:
            return generateQRImage(gen_ss_code())



def generateQRImage(your_string):

    qr = qrcode.QRCode(version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
    qr.add_data(your_string)
    qr.make(fit=True)

    # creates qrcode base64
    s_io = StringIO.StringIO()
    qr_img = qr.make_image()
    qr_img.save(s_io)

    #response = Flask.make_response(s_io.getvalue())
    #response.headers["Content-Type"] = "image/jpeg"
    #response.headers["Content-Disposition"] = "attachment; filename=image.jpg"

    return send_file(io.BytesIO(s_io.getvalue()),"image/png")
    #return send_file('asdasdasd',"image/png")


def get_ss_info(file=True):
    config = {}
    config['ip'] = urllib2.urlopen('http://ip.42.pl/raw').read()
    if file:
        with open(path['method']) as f:
            config['method'] = f.readline().strip('\n')
        with open(path['password']) as f:
            config['password'] = f.readline().strip('\n')
        with open(path['port']) as f:
            config['port'] = f.readline().strip('\n')
    else:
        pass

    return config

def gen_config_str(config):
    return "%s:%s@%s:%s" % (config['method'], config['password'], config['ip'], config['port'])

def gen_ss_code():
    config_string = gen_config_str(get_ss_info())
    config_string = base64.b64encode(config_string)
    config_string = "ss://" + config_string
    return config_string

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=9537)
