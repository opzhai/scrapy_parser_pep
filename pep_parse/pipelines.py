import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from scrapy.exceptions import DropItem

BASE_DIR = Path(__file__).parent.parent

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILENAME = 'status_summary_{time}.csv'


class PepParsePipeline:

    def __init__(self):
        self.results_dir = BASE_DIR / 'results'
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.results = defaultdict(int)

    def process_item(self, item, spider):
        self.results[item['status']] += 1
        return item

    def close_spider(self, spider):
        with open(
            self.results_dir / FILENAME.format(
                time=datetime.now().strftime(DATETIME_FORMAT)
            ),
            mode='w',
            encoding='utf-8'
        ) as file:
            csv.writer(
                file,
                dialect=csv.unix_dialect,
                quoting=csv.QUOTE_NONE
            ).writerows(
                [['Статус', 'Количество'],
                 *(self.results.items()),
                 ['Total', sum(self.results.values())]
                 ])
