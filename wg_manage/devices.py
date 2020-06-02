from wg_manage.ip_assignment import gen_peer_ips


def add_device(config, name, pub_key, shared_key=None):
  ipv4_addr, v6_subnet = gen_peer_ips(config, len(config["peers"]))

  device = {
    "# Name": name,
    "PublicKey": pub_key,
    "AllowedIPs": f"{ipv4_addr}/32, {v6_subnet}"
  }

  if shared_key:
    device["PresharedKey"] = shared_key

  config["peers"].append(device)
  return device


def generate_peers_config(config):
  def peer_config_stub(peer):
    return "[Peer]\n" + "\n".join(f"{k} = {v}" for k, v in peer.items())

  return "\n\n".join(peer_config_stub(p) for p in config["peers"])


def generate_client_config(config, peer):
  return f"""
[Interface]
PrivateKey = ENTER_PRIVATE_KEY
Address = {peer['AllowedIPs']}

[Peer]
PublicKey = {config['hub_public_key']}
Endpoint = {config['hub_address']}
AllowedIPs = {config['prefix_v4']}, {config['prefix_v6']}
{'PresharedKey = ' + peer['PresharedKey'] if 'PresharedKey' in peer else ''}
  """.strip()
