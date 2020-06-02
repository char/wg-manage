from wg_manage.config import read_config, write_config
from wg_manage.devices import add_device, generate_peers_config


from flask import Flask, Response, request, jsonify
app = Flask(__name__)

import functools

def require_auth(route):
  @functools.wraps(route)
  def f(*a, **kw):
    config = read_config()
    if request.headers.get("Authorization") != f"Bearer {config['auth_token']}":
      return jsonify({ "error": "Missing or invalid authorization token" }), 403

    return route(*a, **kw, config=config)

  return f


@app.route("/add", methods=["POST"])
@require_auth
def add(config):
  form = request.get_json()
  if form is None:
    form = request.form

  name = form.get("name")
  pk = form.get("pk")
  psk = form.get("psk")

  if name is None or pk is None:
    return jsonify({ "error": "Missing parameter 'name' or 'pk'." }), 400

  res = jsonify(add_device(config, name, pk, psk))
  write_config(config)
  return res


@app.route("/peers")
@require_auth
def peers(config):
  return Response(generate_peers_config(config), content_type="text/plain")
