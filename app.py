import json
from json.decoder import JSONDecodeError
from typing import Dict, Optional

from flask import Flask, render_template, request, Response, send_file

MY_DICT = Dict[str, Optional[str]]

app = Flask(__name__)


def export_json(d: MY_DICT) -> None:
    """Create .json file from the passed dictionary."""
    with open('player_sheet.json', 'w') as file:
        file.write(json.dumps(d))


def get_sheet_info() -> MY_DICT:
    """Return a dictionary with all info from the player sheet."""
    info = {}
    info['max_skill'] = request.form.get('max-skill')
    info['cur_skill'] = request.form.get('cur-skill')
    info['max_hp'] = request.form.get('max-hp')
    info['cur_hp'] = request.form.get('cur-hp')
    info['max_luck'] = request.form.get('max-luck')
    info['cur_luck'] = request.form.get('cur-luck')
    info['checkpoint'] = request.form.get('page-num')
    info['gold'] = request.form.get('gold')
    info['treasures'] = request.form.get('treasures')
    info['food'] = request.form.get('food')
    info['provisions'] = request.form.get('provisions')
    info['inventory'] = request.form.get('equipment-and-items')
    info['special'] = request.form.get('conditions')
    info['notes'] = request.form.get('clues')
    return info


def render_sheet(info: Optional[MY_DICT]= None) -> str:
    """Render player sheet from the passed info, or a basic one if not info given."""
    if info:
        return render_template('index.j2',
            max_skill = info['max_skill'], cur_skill = info['cur_skill'],
            max_hp = info['max_hp'], cur_hp = info['cur_hp'],
            max_luck = info['max_luck'], cur_luck = info['cur_luck'],
            checkpoint = info['checkpoint'], gold = info['gold'],
            treasures = info['treasures'], food = info['food'],
            provisions = info['provisions'], inventory = info['inventory'],
            special = info['special'], notes = info['notes'])
    else:
        return render_template('index.j2')


@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    """Render a basic player sheet."""
    return render_sheet()


@app.route('/download', methods=['POST'])
def download() -> Response:
    """Download the current sheet info to a .json file."""
    info = get_sheet_info()
    export_json(info)
    return send_file('player_sheet.json', attachment_filename='player_sheet.json', as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload() -> str:
    """Render player sheet from the uploaded file, or the current sheet if no file passed."""
    file = request.files['upload']
    try:
        sheet = json.loads(file.read())
        return render_sheet(sheet)
    except (JSONDecodeError, TypeError):
        info = get_sheet_info()
        return render_sheet(info)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)