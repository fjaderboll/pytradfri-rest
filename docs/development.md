# Development setup
Below is tested on Raspbian (stretch) and Linux Mint 20.3 (Una),
but should work in all similar environments.

## With docker
Install Docker first if you haven't:
```shell
sudo apt install docker-ce   # Raspbian
sudo apt install docker.io   # other
```

Then run:
```shell
./docker/build.sh      # builds the image
./docker/run.sh 2080   # starts server at http://localhost:2080/
```

## Without docker (development)
First time only:
```shell
sudo ./docker/install-coap-client.sh
sudo apt install python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
./create-crypt-key.sh  # creates rest/crypt.key (login tokens depend on this)
```

Run:
```shell
source .venv/bin/activate
./rest/rest.py 2080    # start server at http://localhost:2080/

./test/test.py --help  # automatically test some of the endpoints
```