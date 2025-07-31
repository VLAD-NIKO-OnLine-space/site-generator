import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


OPENAI_API_KEY = "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"

PROJECT_ID = "proj_ZA6skTuKlWmJKqoiiw8Y7YOv"


client = OpenAI(
    api_key=OPENAI_API_KEY,
    project=PROJECT_ID  # обязательное поле для project-based ключей
)
def extract_text_from_doc(doc_url):
    try:
        doc_id = doc_url.split("/d/")[1].split("/")[0]
        export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
        response = requests.get(export_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[!] Error downloading: {doc_url}\n    {e}")
        return None

def generate_site_html(seo_text, language="English"):
    prompt = f"""
You are an AI website developer. Based on the following SEO audit, generate an HTML homepage.

SEO Audit:
{seo_text}

Requirements:
- Language: {language}
- Include <title> and meta description
- Include header(with burger menu) and footer(with logo) with a anchor links
- Use H1–H3 headings with keywords
- Generate and pass image into the sections 
- Sections: Hero, Services, About, CTA, FAQ
- Clean, minimal HTML (inline CSS or Tailwind)
- Output only HTML code, no explanations
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[!] OpenAI error:\n    {e}")
        return None

def save_html(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Saved: {filename}")

def main():
    language = "English"

    with open("audits.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    for i, url in enumerate(urls, start=1):
        print(f"\n=== Processing [{i}] ===")
        seo_text = extract_text_from_doc(url)
        if not seo_text:
            continue

        html = generate_site_html(seo_text, language)
        if not html:
            continue

        save_html(html, f"site_{i}.html")

if __name__ == "__main__":
    main()
