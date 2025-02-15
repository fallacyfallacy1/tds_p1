import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests


load_dotenv()

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")


def B12(filepath):
    if filepath.startswith("/data"):
        # raise PermissionError("Access outside /data is not allowed.")
        # print("Access outside /data is not allowed.")
        return True
    else:
        return False


# B3: Fetch Data from an API
def B3(url, save_path):
    if not B12(save_path):
        return None
    import requests

    response = requests.get(url)
    with open(save_path, "w") as file:
        file.write(response.text)


# B4: Clone a Git Repo and Make a Commit
def B4(repo_url, commit_message):
    import subprocess, os

    repo_path = "/data/repo"
    subprocess.run(["git", "clone", repo_url, repo_path])
    subprocess.run(["git", "-C", repo_path, "add", "."])  # Stage all changes
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message])


# B5: Run SQL Query
def B5(db_path, query, output_filename):
    if not B12(db_path) or not B12(output_filename):
        return None
    if db_path.endswith(".db"):
        import sqlite3

        conn = sqlite3.connect(db_path)
    elif db_path.endswith(".duckdb"):
        import duckdb

        conn = duckdb.connect(db_path)
    else:
        raise ValueError("Unsupported database type")

    cur = conn.cursor() if hasattr(conn, "cursor") else conn
    result = cur.execute(query).fetchall()
    conn.close()

    with open(output_filename, "w") as file:
        file.write(str(result))
    return result


# B6: Web Scraping
def B6(url, output_filename):
    import requests

    result = requests.get(url).text
    with open(output_filename, "w") as file:
        file.write(str(result))


# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image

    if not B12(image_path):
        return None
    if not B12(output_path):
        return None
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)


# B8: Audio Transcription
def B8(audio_path):

    print("audio_path", audio_path)


# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    import markdown

    if not B12(md_path):
        return None
    if not B12(output_path):
        return None
    with open(md_path, "r") as file:
        html = markdown.markdown(file.read())
    with open(output_path, "w") as file:
        file.write(html)


# B10: API Endpoint for CSV Filtering
# from flask import Flask, request, jsonify
# app = Flask(__name__)
# @app.route('/filter_csv', methods=['POST'])
# def filter_csv():
#     import pandas as pd
#     data = request.json
#     csv_path, filter_column, filter_value = data['csv_path'], data['filter_column'], data['filter_value']
#     B12(csv_path)
#     df = pd.read_csv(csv_path)
#     filtered = df[df[filter_column] == filter_value]
#     return jsonify(filtered.to_dict(orient='records'))
