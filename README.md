# tiny-info-screen

Display local electricity prices for the coming few hours on a small e-paper display.
The idea is to make it easy to see when it's least expensive to charge our cars.

## Install requirements

pip3 install -r requirements.txt

## Run

python3 main.py

## Development

Use this to re-execute whenever the file changes

```
while inotifywait -e close_write main.py; do python3 ./main.py; done
```
