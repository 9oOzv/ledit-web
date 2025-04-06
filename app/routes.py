from flask import Flask, request, render_template, current_app, Blueprint
from .device import Device
from .effect import Effect
from .binding import Binding
import socket
from .store import Store
from .error import SafeError
from .util import float_to_uint16, int_to_uint16, int_to_uint8
from .jinja_utils import jinja_utils

bp = Blueprint('routes', __name__)

devices = [
    Device(id='bedroom', name='Bedroom', ip='192.168.12.201', port=4210),
]


def color_correct(color: list[float]) -> list[float]:
    return [
        color[0],
        color[1] * 0.6,
        color[2] * 0.4,
    ]

effects = [
    Effect(id='yellow', name='Yellow', number=2, parameters=color_correct([1.0, 1.0, 0.0])),
    Effect(id='cyan', name='Cyan', number=2, parameters=color_correct([0.0, 1.0, 1.0])),
    Effect(id='magenta', name='Magenta', number=2, parameters=color_correct([1.0, 0.0, 1.0])),
    Effect(id='white', name='White', number=2, parameters=[1.0, 1.0, 1.0]),
    Effect(id='dark1', name='Dark 1', number=2, parameters=[0.1, 0.1, 0.1]),
    Effect(id='dark2', name='Dark 2', number=2, parameters=[0.02, 0.02, 0.02]),
    Effect(id='dark3', name='Dark 3', number=2, parameters=[0.01, 0.01, 0.01]),
    Effect(id='red', name='Red', number=2, parameters=[1.0, 0.0, 0.0]),
    Effect(id='green', name='Green', number=2, parameters=[0.0, 1.0, 0.0]),
    Effect(id='blue', name='Blue', number=2, parameters=[0.0, 0.0, 1.0]),
    Effect(id='darkpink', name='Dark Pink', number=2, parameters=[0.1, 0.0, 0.05]),
    Effect(id='darkpink2', name='Dark Pink 2', number=2, parameters=[0.05, 0.0, 0.02]),
    Effect(id='darkpurple', name='Dark Purple', number=2, parameters=[0.1, 0.0, 0.1]),
    Effect(id='darkpurple2', name='Dark Purple 2', number=2, parameters=[0.02, 0.0, 0.02]),
    Effect(id='rainbow1', name='Rainbow 1', number=1, parameters=[20 / 65535]),
    Effect(id='rainbow2', name='Rainbow 2', number=1, parameters=[100 / 65535]),
    Effect(id='rainbow3', name='Rainbow 3', number=1, parameters=[500 / 65535]),
    Effect(id='off', name='Off', number=2, parameters=[0.0, 0.0, 0.0]),
]
bindings = [ ]
store = Store(devices=devices, effects=effects, bindings=bindings)


def send_udp(device: Device, message: bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(message, (str(device.ip), device.port))

@bp.context_processor
def inject_jinja_utils():
    def random_string(length: int = 16) -> str:
        import random
        import string
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))
    def to_input_value(value):
        if isinstance(value, list):
            return ",".join(str(v) for v in value)
        return str(value)
    return dict(random_string=random_string)


@bp.app_template_test(name='list')
def is_list(value):
    return isinstance(value, list)


@bp.errorhandler(SafeError)
def handle_error(error):
    return str(error), 400


def send_updates():
    for b in store.bindings:
        d = store.get_device(b.device_id)
        e = store.get_effect(b.effect_id)
        data = (
            int_to_uint8(e.number) +
            b"".join(float_to_uint16(p) for p in e.parameters)
        )
        send_udp(d, data)


@bp.route("/update", methods=["POST"])
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
    send_updates()
    return "OK"


@bp.route("/")
def index():
    return render_template(
        "index.html.jinja",
        devices=[vars(d) for d in store.devices],
        effects=[vars(e) for e in store.effects],
        bindings=[vars(b) for b in store.bindings]
    )

send_updates()
