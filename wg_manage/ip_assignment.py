from ipaddress import IPv4Network, IPv6Network

def gen_peer_ips(config, n):
  v4_network = IPv4Network(config["prefix_v4"])
  v6_network = IPv6Network(config["prefix_v6"])

  v4_host = None
  v6_subnet = None

  for idx, host in enumerate(v4_network.hosts()):
    if idx == n:
      v4_host = host
      break

  for idx, subnet in enumerate(v6_network.subnets(new_prefix=96), -1):
    if idx == n:
      v6_subnet = subnet
      break

  return v4_host, v6_subnet
