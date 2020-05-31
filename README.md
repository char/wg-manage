# wg-manage

A super simple WireGuard configuration management service. Bring your own front-end.

## Setup

```shell
$ cp config.sample.json config.json
$ $EDITOR config.json
$ pipenv install
[pipenv] $ python3 ./run_dev.py # Start a local server
```

## Usage

Supply the HTTP header 'Authorization' with a bearer token set to the value provided for `auth_token` in `config.json`.

- Call `GET /peers` to get a WireGuard config-compatible list of peers
- Call `POST /add` to add to a device, with the body of the request being JSON, supplying a device name `name`, public key `pk`, and (optionally) a pre-shared key `psk`.
