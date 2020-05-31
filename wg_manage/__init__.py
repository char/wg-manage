from wg_manage.config import read_config, write_config
config = read_config()

from wg_manage.devices import add_device, generate_peers_config


from flask import Flask, Response, request, jsonify
app = Flask(__name__)


def require_auth(route):
  def f(*a, **kw):
    if request.headers.get("Authorization") != f"Bearer {config['auth_token']}":
      return jsonify({ "error": "Missing authorization token" }), 403

    return route(*a, **kw)

  return f


@require_auth
@app.route("/add", methods=["POST"])
def add():
  form = request.get_json()
  name = form.get("name")
  pk = form.get("pk")
  psk = form.get("psk")

  if name is None or pk is None:
    return jsonify({ "error": "Missing parameter 'name' or 'pk'." }), 400

  res = jsonify(add_device(name, pk, psk))
  write_config(config)
  return res


@require_auth
@app.route("/peers")
def peers():
  if request.headers.get("Authorization") != f"Bearer {config['auth_token']}":
    return jsonify({ "error": "Missing authorization token" }), 403

  return Response(generate_peers_config(), content_type="text/plain")
