import os
import json
import time
import requests
import ast
from bs4 import BeautifulSoup


# =========================
# 1. 配置区
# =========================

OUTPUT_PATH = "transcript.jsonl"
SLEEP_OK = 3
SLEEP_ERROR = 5

# HEADERS / COOKIES unchanged
HEADERS = {}
COOKIES = {}

YOUTUBE_LINKS = [
    "https://www.youtube.com/watch?v=m5Kn9WmOCrw"
]


# =========================
# 2. 工具函数
# =========================

def extract_video_id(youtube_url: str) -> str:
    if "v=" in youtube_url:
        return youtube_url.split("v=")[-1].split("&")[0]
    raise ValueError(f"Invalid YouTube URL: {youtube_url}")


def load_finished_ids(path: str) -> set:
    """
    Load already-collected video_ids.
    Handles BOTH valid JSON and old Python-dict lines.
    """
    finished = set()

    if not os.path.exists(path):
        return finished

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # 🔧 FIX: support old broken lines
                try:
                    data = ast.literal_eval(line)
                except Exception:
                    continue

            if isinstance(data, dict):
                finished.update(data.keys())

    return finished


def get_transcript(youtube_url: str) -> str:
    video_id = extract_video_id(youtube_url)
    page_url = f"https://youtubetotranscript.com/transcript?v={video_id}"

    response = requests.get(
        page_url,
        headers=HEADERS,
        cookies=COOKIES,
        timeout=15
    )

    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.find("div", id="transcript")
    if not container:
        return ""

    segments = container.find_all("span", class_="transcript-segment")
    return " ".join(seg.get_text(strip=True) for seg in segments)


# =========================
# 3. 主程序（断点续跑）
# =========================

def main():
    finished_ids = load_finished_ids(OUTPUT_PATH)
    print(f"Already collected: {len(finished_ids)}")

    with open(OUTPUT_PATH, "a", encoding="utf-8") as out:
        for url in YOUTUBE_LINKS:
            video_id = extract_video_id(url)

            if video_id in finished_ids:
                print(f"[SKIP] {video_id}")
                continue

            try:
                transcript = get_transcript(url)

                if not transcript:
                    print(f"[EMPTY] {video_id}")
                    continue

                # ✅ CORRECT JSONL WRITE (this is the key)
                json.dump(
                    {video_id: transcript},
                    out,
                    ensure_ascii=False
                )
                out.write("\n")
                out.flush()

                finished_ids.add(video_id)
                print(f"[OK] {video_id}")

                time.sleep(SLEEP_OK)

            except KeyboardInterrupt:
                print("\n[STOP] Manual interrupt, progress saved.")
                break

            except Exception as e:
                print(f"[ERROR] {video_id}: {e}")
                time.sleep(SLEEP_ERROR)


# =========================
# 4. 入口
# =========================

if __name__ == "__main__":
    main()
