from io import BytesIO
import unicodedata
import mimetypes
from flask import Flask, request, make_response, jsonify
from werkzeug.routing import BaseConverter, ValidationError
from PIL import Image, ImageFont, ImageDraw
import board
from cors import crossdomain
import os


class HexConverter(BaseConverter):
    def to_python(self, value):
        try:
            return int(value, base=16)
        except ValueError as e:
            raise ValidationError(e)
    def to_url(self, value):
        return hex(value)


#FONT_PATH = "fonts/unifont.tff"
#FONT_PATH = "fonts/wqy-zenhei.ttc"
#FONT_PATH = "fonts/DejaVuSans.ttf"
FONT_PATH = "fonts/CODE2000.TTF"

app = Flask(__name__)
app.url_map.converters['int16'] = HexConverter
app.config['font'] = ImageFont.truetype(FONT_PATH, 30)
app.debug = True


def image_data(string, format):
    image = Image.new("L", (60, 60), 255)
    drawer = ImageDraw.Draw(image)
    drawer.text((20, 10), string, fill=0, font=app.config['font'])
    buffer = BytesIO()
    image.save(buffer, format=format, optimize=1)
    return buffer.getvalue()


def charname(char):
    try:
        return unicodedata.name(char)
    except ValueError:
        return "Name not found"


@app.route('/characters/unicode/U+<int16:codepoint>')
@app.route('/characters/unicode/U+<int16:codepoint>.<format>')
@crossdomain(origin='*')
def display_codepoint(codepoint, format='json'):
    if format in ("png", "jpg", "jpeg", "gif", "tiff"):
        data = image_data(chr(codepoint), format)
        response = make_response(data)
        response.headers['Content-Type'] = mimetypes.types_map.get('.' + format)
        return response
    elif format == "html":
        big = u"<h1>{char}</h1>".format(char=chr(codepoint))
        response = make_response(big)
        response.headers['Content-Type'] = "text/html; charset=\"UTF-8\""
        return response
    elif format == "json":
        return character_data(chr(codepoint))
    else:
        return chr(codepoint)


@app.route('/characters/utf8/<char>')
@app.route('/characters/utf8/<char>.<format>')
@crossdomain(origin='*')
def character_data(char, format="json"):
    chardata = {}
    chardata['name'] = charname(char)
    chardata['raw'] = char
    try:
        chardata['integer_codepoint'] = ord(char)
        chardata['codepoint'] = "U+{0:0=4X}".format(ord(char))
    except TypeError:
        chardata['codepoint'] = "Multiple characters"
    chardata['encodings'] = {}
    for coding in ["latin1", "utf8", "utf-16-be", "utf-32-be"]:
        bytes = ["0x%02x" % c for c in bytearray(char.encode(coding, 'ignore'))] or None
        chardata['encodings'][coding] = bytes

    if "text/plain" in request.headers.get('Accept', '') or format == "txt":
        info = "{name}: {codepoint}".format(**chardata)
        lines = [info]
        for coding, bytes in chardata['encodings'].items():
            bytes = bytes or "No encoding!"
            lines.append("In {coding}: {bytes}".format(coding=coding, bytes=bytes))
        response = make_response("\n".join(lines))
        response.headers['Content-Type'] = "text/plain; charset=\"UTF-8\""
        return response
    else:
        return jsonify(**chardata)


@app.route('/chessboard/<int16:light>/<int16:dark>')
@crossdomain(origin='*')
def chessboard(light, dark):
    fen = request.args.get("fen", board.start_fen)
    response = u"""<html><head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="maximum-scale=1.0,minimum-scale=1.0,width=device-width,initial-scale=1.0" />
        <style>
        body {{
            font-size: 36px; 
            font-family: Helvetica;
            font-family: "Helvetica Neue";
            white-space: pre;
        }}
        </style>
    </head>
    <body>{chessboard}</body></html>
    """.format(chessboard=board.fen_to_unicode(fen, light=light, dark=dark))
    response = make_response(response)
    response.headers['Content-Type'] = "text/html; charset=\"UTF-8\""
    return response


if __name__ == "__main__":
    app.run(debug=True, port=os.environ['PORT'], host="0.0.0.0")
