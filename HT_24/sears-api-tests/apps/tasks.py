from apps.celery import app
from services.products.scraper_sears import ScraperSears


@app.task(name='scraper_sears', retry_delay=60, max_retries=3)
def scraping_ids(**kwargs):
    task = ScraperSears(product_ids=kwargs.get('product_ids'))
    task.start()
