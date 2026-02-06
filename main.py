import os
from bs4 import BeautifulSoup
from markdownify import markdownify as md

INPUT_FILE = "messages.html"
OUTPUT_DIR = "posts_md"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

messages = soup.find_all("div", class_="message")

for i, msg in enumerate(messages, start=1):
    text_block = msg.find("div", class_="text")

    if not text_block:
        continue

    html_content = str(text_block)
    markdown_content = md(html_content, heading_style="ATX")

    date_div = msg.find("div", class_="pull_right date")
    date = date_div["title"].replace(":", "-") if date_div else f"post_{i}"

    filename = f"{i:04d}_{date}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as out:
        out.write(markdown_content)

print("✅ Conversion completed.")
