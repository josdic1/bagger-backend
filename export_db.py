import sqlite3
import json
import os
import sys
from datetime import datetime
from pathlib import Path

def get_timestamp():
    return datetime.now().strftime("%m%d%y_%I%M%p")

def get_data():
    db_name = 'bagger.db'
    if not os.path.exists(db_name):
        print(f"Error: {db_name} not found in {os.getcwd()}")
        return None
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row['name'] for row in cursor.fetchall()]
    data = {table: [dict(row) for row in cursor.execute(f"SELECT * FROM {table}").fetchall()] for table in tables}
    conn.close()
    return data

def save_json(data, ts, path):
    filename = os.path.join(path, f"bagger_json_{ts}.txt")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Exported JSON: {filename}")

def save_db_text(data, ts, path):
    filename = os.path.join(path, f"bagger_db_{ts}.txt")
    with open(filename, 'w') as f:
        for table, rows in data.items():
            f.write(f"=== TABLE: {table} ===\n")
            for row in rows:
                f.write(f"{str(row)}\n")
            f.write("\n")
    print(f"✅ Exported DB Text: {filename}")

def save_html(data, ts, path):
    filename = os.path.join(path, f"bagger_html_{ts}.html")
    html_content = f"<html><body style='background:#0f0f10;color:#ececec;font-family:sans-serif;'><h1>Bagger Archive {ts}</h1>"
    for table, rows in data.items():
        html_content += f"<h2>{table}</h2>"
        for r in rows:
            html_content += f"<div style='background:#141415;border:1px solid #242424;padding:10px;margin:10px;border-radius:8px;'><pre>{json.dumps(r, indent=2)}</pre></div>"
    html_content += "</body></html>"
    with open(filename, 'w') as f:
        f.write(html_content)
    print(f"✅ Exported HTML: {filename}")

def main():
    data = get_data()
    if not data: return
    ts = get_timestamp()
    downloads = str(Path.home() / "Downloads")
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if arg == "json": save_json(data, ts, downloads)
    elif arg == "db": save_db_text(data, ts, downloads)
    elif arg == "html": save_html(data, ts, downloads)
    else:
        save_json(data, ts, downloads)
        save_db_text(data, ts, downloads)
        save_html(data, ts, downloads)

if __name__ == "__main__":
    main()
