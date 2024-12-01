from flask import Flask, jsonify, request
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime, timezone, date, timedelta
from json import dumps
import asyncio


current_timestamptz = datetime.now(timezone.utc)
last_node_purge = datetime.now(timezone.utc)
next_node_purge = last_node_purge + timedelta(minutes=5)
should_trigger_purge_var = False

def should_trigger_purge() -> bool:
    if datetime.now(timezone.utc) >= next_node_purge:
        return True
    else:
        return False


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s cannot be serialized " % type(obj))


load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/register_ip', methods=['POST'])
async def register_ip():
    try:
        should_trigger_purge_var = should_trigger_purge()
        if should_trigger_purge_var:
            asyncio.create_task(purge_old_nodes())
        uuid_client = uuid.uuid4()
        current_timestamptz = datetime.now(timezone.utc)
        current_timestampzJSON = dumps(current_timestamptz, default=json_serial)
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        if ip_address and ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        response = supabase.table('ips').insert({'address': str(uuid_client), 'ip': ip_address, 'last_alive': current_timestampzJSON}).execute()
        if response.data:
            print("Succesfully registered ip")
            return jsonify({"message": f"IP {ip_address} registered successfully"}), 201
        else:
            print("Unknown error occured")
            return jsonify({"error": "Unknown error occurred"}), 500
    except Exception as e:
        print("Error 400")
        return jsonify({"error": str(e)}), 400

async def purge_old_nodes():
    response = supabase.table('ips').delete().filter("last_alive", "lt", datetime.now(timezone.utc) - timedelta(days=1)).execute()
    if response.data:
        for row in response.data:
            print(row)
        else:
            print("No rows found or error:", response)
    print("Purging finished")
    should_trigger_purge_var = False


@app.route('/list_ips', methods=['GET'])
def list_ips():
    should_trigger_purge_var = should_trigger_purge()
    try:
        data = supabase.table('ips').select('*').execute()
        
        return jsonify({"ips": [ip['ip'] for ip in data.data]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    