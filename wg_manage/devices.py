from wg_manage import config
from wg_manage.ip_assignment import gen_peer_ips


def add_device(name, pub_key, shared_key=None):
  ipv4_addr, v6_subnet = gen_peer_ips(len(config["peers"]))

  device = {
    "# Name": name,
    "PublicKey": pub_key,
    "AllowedIPs": f"{ipv4_addr}/32, {v6_subnet}"
  }

  if shared_key:
    device["PreSharedKey"] = shared_key

  config["peers"].append(device)
  return device


def generate_peers_config():
  def peer_config_stub(peer):
    return "[Peer]\n" + "\n".join(f"{k} = {v}" for k, v in peer.items())

  return "\n\n".join(peer_config_stub(p) for p in config["peers"])
