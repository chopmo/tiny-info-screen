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

Or use the helper script:

```bash
./bin/update-display
```

## Scheduled Updates (Cron)

To automatically update the display every hour on a Raspberry Pi:

1. Edit your crontab:
```bash
crontab -e
```

2. Add this line to run every hour:
```bash
0 * * * * /home/jtj/tiny-info-screen/bin/update-display >> /home/jtj/tiny-info-screen/cron.log 2>&1
```

The display will now update automatically every hour on the hour. Check `cron.log` for any errors.

## Development

Use this to re-execute whenever the file changes:

```bash
while inotifywait -e close_write main.py; do python3 ./main.py --dev; done
```
