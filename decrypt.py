import base64
import json
from phpserialize import unserialize
from crypto.Cipher import AES
from crypto.Util.Padding import pad, unpad

key = b'my secret key'
enc_pass = 'eyJpdiI6IndFb0diT0FVYWdsMFhnbVBXcmxRaEE9PSIsInZhbHVlIjoiR0YrY1hJQ25PcGhmcDhYeEVoKzJRTDVuQXBlVDJOWWNqZXU2M01tQ0hiYz0iLCJtYWMiOiI2ZTg4ZDY0YzFkZDlmNzhiYWRkYWQwYTVmZjJhZWM3ZTUyNzFmNDcwMWE3YWUxYjUwZGJjN2ZmYmFkMWQyNmQ0IiwidGFnIjoiIn0='

p_obj = json.loads(base64.b64decode(enc_pass).decode())
decobj = AES.new(key, AES.MODE_CBC, base64.b64decode(p_obj['iv']))
data = decobj.decrypt(base64.b64decode(p_obj['value']))
dec_pass = unserialize(unpad(data, 16)).decode()
print(dec_pass)