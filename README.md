# Track Announcer MPRIS

This is a command line program that speaks the track/media title when a new track starts playing on a media player that follows the [MPRIS D-Bus interface specification](https://specifications.freedesktop.org/mpris-spec/latest/).

## Setup

You will need:
* D-Bus (e.g. libdbus-1-dev on Ubuntu)
* GObject Introspection (e.g. libgirepository1.0-dev on Ubuntu)
* Python 3
* A text to speech program (e.g. eSpeak NG, Festival, Flite)

You can use a Python virtual environment:
```sh
python -m venv venv
. venv/bin/activate
```

Install Python dependencies with:
```sh
pip install -r requirements.txt
```

## Usage

Run the `bin/track-announcer` script.
When the script is running, it will detect when a new track starts playing.

By default, track-announcer uses the speak executable (provided by eSpeak NG).
You can use a different program by using the `--speak-command-template` option with a command template string where `%s` will be replaced by the track title.

## Tests

To run the unit tests, run:
```sh
python -m unittest
```
