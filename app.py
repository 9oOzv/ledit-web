from flask import Flask, request, render_template
from .device import Device
import socket
from .store import Store
from .error import SafeError


app = Flask(__name__)

devices = [
    Device(id='foo', name='Foo', ip='127.0.0.1', port=1234),
    Device(id='bar', name='Bar', ip='127.0.0.2', port=2345)
]

effects = []
bindings = []
store = Store(devices=devices, effects=effects, bindings=bindings)


def send_udp(device: Device, port: int, message: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message, (str(device.ip), port))


@app.errorhandler(SafeError)
def handle_error(error):
    return str(error), 400


@app.route("/update", methods=["POST"])
def update():
    data = request.json
    type_ = data.get("type")
    id = data.get("id")
    fields = data.get("fields")
    if not type_:
        raise SafeError("Missing type")
    if not id:
        raise SafeError("Missing id")
    if not fields:
        raise SafeError("Missing fields")
    if type_ == "device":
        store.update_device(fields, id)
    elif type_ == "effect":
        store.update_effect(fields, id)
    elif type_ == "binding":
        store.update_binding(fields, id)
    else:
        raise SafeError(f"Unknown type: {type_}")
    return "OK"


@app.route("/")
def index():
    return render_template(
        "index.html.jinja",
        devices=[vars(d) for d in store.devices],
        effects=[vars(e) for e in store.effects],
        bindings=[vars(b) for b in store.bindings]
    )
