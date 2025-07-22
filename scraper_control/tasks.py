from celery import shared_task
import subprocess
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
    
@shared_task
def run_zoomit_spider_task(pages="1"):
    try:
        scrapy_project_path = BASE_DIR / 'news_scraper'

        if not scrapy_project_path.exists():
            return f"Scrapy project path not found: {scrapy_project_path}"

        env = os.environ.copy()
        env["PYTHONPATH"] = str(BASE_DIR)

        subprocess.run(
            ['scrapy', 'crawl', 'zoomit', '-a', f'pages={pages}'],
            cwd=str(BASE_DIR), 
            env=env,
            check=True
        )
        return f"Spider run successful for pages: {pages}"
    except subprocess.CalledProcessError as e:
        return f"Spider run failed: {e}"
