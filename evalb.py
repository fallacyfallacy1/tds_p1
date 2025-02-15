# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "faker",
#     "httpx",
#     "numpy",
#     "pillow",
#     "python-dateutil",
#     "python-dotenv",
#     "requests",
#     "scipy",
#     "uvicorn",
#     "fastapi",
#     "duckdb",
#     "pandas",
#     "markdown",
# ]
# ///
import os
import requests
import subprocess
import sqlite3
import duckdb
import markdown
from PIL import Image

def B1(filepath):
    """Ensures data outside /data is never accessed or exfiltrated."""
    return filepath.startswith("/data")

def B2(filepath):
    """Ensures data is never deleted anywhere on the file system."""
    return B1(filepath) and not os.path.exists(filepath)

def B3(url, save_path):
    """Fetch data from an API and save it."""
    if not B1(save_path):
        return None
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

def B4(repo_url, commit_message):
    """Clone a git repo and make a commit."""
    repo_path = "/data/repo"
    if not B1(repo_path):
        return None
    subprocess.run(["git", "clone", repo_url, repo_path])
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message])

def B5(db_path, query, output_filename):
    """Run a SQL query on SQLite or DuckDB and save results."""
    if not B1(db_path) or not B1(output_filename):
        return None
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

def B6(url, output_filename):
    """Extract data (scrape) from a website."""
    if not B1(output_filename):
        return None
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))

def B7(image_path, output_path, resize=None):
    """Compress or resize an image."""
    if not B1(image_path) or not B1(output_path):
        return None
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)

def B8(audio_path, output_text_path):
    """Transcribe audio from an MP3 file (Mock Implementation)."""
    if not B1(audio_path) or not B1(output_text_path):
        return None
    # Mock transcription result (replace with actual API call)
    transcription = "Transcribed text from audio."
    with open(output_text_path, 'w') as file:
        file.write(transcription)

def B9(md_path, output_path):
    """Convert Markdown to HTML."""
    if not B1(md_path) or not B1(output_path):
        return None
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)

def B10(csv_path, filter_column, filter_value, output_json):
    """Filter a CSV file and return JSON data."""
    import pandas as pd
    if not B1(csv_path) or not B1(output_json):
        return None
    df = pd.read_csv(csv_path)
    filtered = df[df[filter_column] == filter_value]
    filtered.to_json(output_json, orient='records')



openai_api_base = os.getenv(
    "OPENAI_API_BASE", "https://aiproxy.sanand.workers.dev/openai/v1"
)
openai_api_key = os.getenv("OPENAI_API_KEY")


def num(str):
    return int(hashlib.sha256(str.encode()).hexdigest(), 16) % (2**32)


def mismatch(msg, expected, result):
    logging.error(f"🔴 {msg}\n⚠️ EXPECTED:\n{expected}\n⚠️ RESULT:\n{result}")
    return False


async def run(task: str):
    async with httpx.AsyncClient(timeout=30) as client:
        logging.warning(f"🟡 Running task: {task.strip()}")
        response = await client.post("http://localhost:8000/run", params={"task": task})
        try:
            response_text = json.dumps(response.json(), indent=2)
        except json.JSONDecodeError:
            response_text = response.text
        if response.status_code < 400:
            logging.info(f"🟢 HTTP {response.status_code} {response_text}")
        else:
            logging.error(f"🔴 HTTP {response.status_code} {response_text}")
        return response.status_code, response_text


async def read(path: str):
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(f"http://localhost:8000/read?path={path}")
        if response.status_code != 200:
            raise Exception(f"Cannot read {path}")
        return response.text

async def main(email: str):
    score, total = 0, 0
    for task in [B1, B2, B3, B4, B5, B6, B7, B8, B9, B10]:
        total += 1
        try:
            success = await task(email=email)
        except Exception as e:
            logging.error(f"🔴 {task.__name__.upper()} failed: {e}")
            success = False
        if success:
            logging.info(f"✅ {task.__name__.upper()} PASSED")
        else:
            logging.error(f"❌ {task.__name__.upper()} FAILED")
        score += 1 if success else 0
    logging.info(f"🎯 Score: {score} / {total}")


if __name__ == "__main__":
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate tasks with configurable logging"
    )
    parser.add_argument(
        "--email", default="user@example.com", help="Set the email address"
    )
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    parser.add_argument(
        "--log-level", default="INFO", choices=levels, help="Set logging level"
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, format="%(message)s\n")
    asyncio.run(main(args.email))
