# quasar_tunnel
Quasar RAT port forwarding tunnel server and client

Must know: networking and port forwarding

# Setup

## Server
- Edit `server.py`.
- Set `SRC_LISTEN_PORT` to where Quasar client will connect.
- Set `DST_LISTEN_PORT` to where `client.py` will connect.
- Set `DST_HOST` to your IP address. If you're running `server.py` over your SSH server like DigitalOcean, you must set it to your public IP address (api.ipify.org).
- Run the script.

## Client
- Edit `client.py`.
- Set `SERVER_HOST` to your running server.
- Set `SERVER_PORT` to where your server `DST_LISTEN_PORT` is listening to.
- Set `ROUTE_TO_PORT` to where your Quasar server is listening to.
- Run the script.

# Known Issues
- SRC client (victim side) packet router session not ending. Do not close `client.py` if you don't want this to happen, if so, just rerun `server.py` in your VPS.

## Diagram
![Quasar Tunnel Diagram](https://user-images.githubusercontent.com/54730301/154272509-f0bfc10e-0e11-46e3-8d63-a919e085a716.jpg)

Goodluck!
