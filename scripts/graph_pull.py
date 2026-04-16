import sys
import requests
from pathlib import Path

OUTPUT_PATH = Path("../graphs/awesome.ttl")

def pull_ttl(url: str):
    print(f"Downloading from {url}...")

    response = requests.get(url)
    response.raise_for_status()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "wb") as f:
        f.write(response.content)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No URL provided")
        sys.exit(1)

    url = sys.argv[1]
    pull_ttl(url)