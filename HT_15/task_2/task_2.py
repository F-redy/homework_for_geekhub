# 2. Викорисовуючи requests, заходите на ось цей сайт "https://www.expireddomains.net/deleted-domains/"
# (з ним будьте обережні), вибираєте будь-яку на ваш вибір доменну зону і парсите список  доменів -
# їх там буде десятки тисяч (звичайно ураховуючи пагінацію). Всі отримані значення зберігти в CSV файл.


import csv
import http
from dataclasses import asdict, dataclass, fields
from time import sleep
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass()
class Domain:
    domain: str  # Domain Name
    bl: str  # Majestic External Backlinks, Click on the Number for Related Links
    dp: str  # SEOkicks Domain Pop - Number of Backlinks from different Domains
    aby: str  # The Birth Year of the Domain using the first found Date from archive.org
    acr: str  # Archive.org Number of Crawl Results
    dmoz: str  # Status of the Domain in Dmoz.org
    status_com: str  # DNS Status .com of Domain Name
    status_net: str  # DNS Status .net of Domain Name
    status_org: str  # DNS Status .org of Domain Name
    status_de: str  # DNS Status .de of Domain Name
    status_tld_registered: str  # Number of TLDs the Domain Name is Registered
    related_cnobi: str  # Numberof Related Domains in .com/.net/.org/.biz/.info
    end_date: str  # Date the Domain will be removed from this Domain List


class ExpiredDomainsScraper:
    BASE_URL = 'https://www.expireddomains.net'
    PAGE_URL = '/expired-domains/'
    DOMAIN_FIELDS = [field.name for field in fields(Domain)]
    DOMAIN_CSV_FILE = 'deleted-domains.csv'
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                  "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://www.expireddomains.net/expired-domains/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "X-Amzn-Trace-Id": "Root=1-6571bae8-18ec31306354ea3c30934a5b"
    }

    def write_headers_to_csv(self):
        with open(f'{self.DOMAIN_CSV_FILE}', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.DOMAIN_FIELDS)
            writer.writeheader()

    def write_to_csv(self, domains: [Domain]):
        with open(f'{self.DOMAIN_CSV_FILE}', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.DOMAIN_FIELDS)
            writer.writerows([asdict(domain) for domain in domains])

    @staticmethod
    def parse_domain(domain):
        return Domain(
            domain=domain.select_one('.field_domain').text.strip(),
            bl=domain.select_one('.field_bl').a.text.strip(),
            dp=domain.select_one('.field_domainpop').text.strip(),
            aby=domain.select_one('.field_abirth').text.strip(),
            acr=domain.select_one('.field_aentries').text.strip(),
            dmoz=domain.select_one('.field_dmoz').text.strip(),
            status_com=domain.select_one('.field_statuscom').text.strip(),
            status_net=domain.select_one('.field_statusnet').text.strip(),
            status_org=domain.select_one('.field_statusorg').text.strip(),
            status_de=domain.select_one('.field_statusde').text.strip(),
            status_tld_registered=domain.select_one('.field_statustld_registered').text.strip(),
            related_cnobi=domain.select_one('.field_related_cnobi').text.strip(),
            end_date=domain.select_one('.field_enddate').text.strip()
        )

    def get_domains(self):
        response = requests.get(f'{urljoin(self.BASE_URL, self.PAGE_URL)}', headers=self.HEADERS)
        if response.status_code == http.HTTPStatus.OK:
            domains = []
            soup = BeautifulSoup(response.content, 'lxml')

            try:
                for domain in soup.select_one('tbody').find_all('tr'):
                    domains.append(self.parse_domain(domain))

                next_page = soup.find('a', class_='next')
            except AttributeError:
                self.PAGE_URL = None
                return

            if next_page:
                self.PAGE_URL = next_page['href']
            else:
                self.PAGE_URL = None

            return domains
        else:
            print(response.status_code)

    def scrape(self):
        self.write_headers_to_csv()

        while True:
            domains = self.get_domains()

            if domains:
                self.write_to_csv(domains)

            if self.PAGE_URL is None:
                print('Stop scraper. Need login...')
                break

            timer_sleep = 10
            print(f'Sleeping for {timer_sleep} seconds...')
            sleep(timer_sleep)


if __name__ == '__main__':
    ExpiredDomainsScraper().scrape()
