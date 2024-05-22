from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from justfortest.models import Beverage  # 수정된 부분

class Command(BaseCommand):
    help = 'Import beverages from HTML file'

    def handle(self, *args, **options):
        # HTML 파일 열기
        with open('/app/justfortest/templates/justfortest/mega_over50.html', 'r', encoding='utf-8') as f:
            contents = f.read()

        soup = BeautifulSoup(contents, 'html.parser')

        # 각 div 태그에 대해
        for div in soup.find_all('div'):
            # id, title, data-price 속성이 있는 경우
            if div.get('id') and div.get('title') and div.get('data-price'):
                name = div.get('id')
                category = div.get('title')
                price = div.get('data-price')

                # Beverage 객체 생성 및 저장
                beverage = Beverage(name=name, category=category, price=price)
                beverage.save()