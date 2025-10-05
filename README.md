# tiny-info-screen

Display local electricity prices for the coming few hours on a small e-paper display.
The idea is to make it easy to see when it's least expensive to charge our cars.

## Setup

Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install requirements:

```bash
pip3 install -r requirements.txt
```

## Run

Development mode (saves to PNG):

```bash
python3 main.py --dev
```

Production mode (displays on InkyPHAT):

```bash
python3 main.py
```

## Development

Use this to re-execute whenever the file changes:

```bash
while inotifywait -e close_write main.py; do python3 ./main.py --dev; done
```
