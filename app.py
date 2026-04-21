"""
SSA Conjunction Intelligence — Space-Track Proxy
Run: python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)

ST_BASE = "https://www.space-track.org"

# ── single shared session so we don't re-login on every request ──────
st_session = requests.Session()


@app.route("/proxy/login", methods=["POST"])
def login():
    data = request.get_json()
    identity = data.get("identity", "")
    password = data.get("password", "")

    resp = st_session.post(
        f"{ST_BASE}/ajaxauth/login",
        data={"identity": identity, "password": password},
        timeout=15,
    )

    if resp.status_code == 200 and "Failed" not in resp.text:
        return jsonify({"ok": True})
    return jsonify({"ok": False, "detail": resp.text}), 401


@app.route("/proxy/tle", methods=["GET"])
def get_tle():
    ids = request.args.get("ids", "")
    if not ids:
        return jsonify({"error": "No NORAD IDs provided"}), 400

    url = (
        f"{ST_BASE}/basicspacedata/query/class/gp"
        f"/NORAD_CAT_ID/{ids}"
        f"/orderby/EPOCH%20desc/limit/20/format/json"
    )

    resp = st_session.get(url, timeout=15)

    if resp.status_code == 200:
        return jsonify(resp.json())
    return jsonify({"error": f"Space-Track returned {resp.status_code}"}), resp.status_code


@app.route("/proxy/logout", methods=["POST"])
def logout():
    st_session.get(f"{ST_BASE}/auth/logout", timeout=10)
    st_session.cookies.clear()
    return jsonify({"ok": True})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("\n🛰  SSA Proxy running on http://localhost:5001\n")
    app.run(port=5001, debug=True)
