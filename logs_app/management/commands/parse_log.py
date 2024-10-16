import re
import requests
import orjson
import logging
from datetime import datetime
from django.db import transaction
from django.core.management.base import BaseCommand
from requests.exceptions import RequestException
from logs_app.models import LogEntry

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Парсит Nginx лог-файл по Google Drive ссылке'

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            type=str,
            help='Google Drive URL лог-файла'
        )

    def handle(self, *args, **options):
        url = options['url']

        try:
            file_id = self.extract_file_id(url)
            download_url = self.get_direct_download_link(file_id)

            session = requests.Session()
            try:
                response = session.get(download_url, stream=True, timeout=10)
            except RequestException as e:
                self.stderr.write(f'Ошибка сети при загрузке файла: {e}')
                return

            # TODO: Обработка подтверждения загрузки

            if response.status_code != 200:
                self.stderr.write(f'Ошибка загрузки файла: {response.status_code}')
                return

            success_count, error_count = self.process_log_file(response)

            self.stdout.write(self.style.SUCCESS(
                f'Лог-файл успешно обработан. Успешно обработано записей: {success_count}, ошибок: {error_count}'
            ))

        except ValueError as e:
            self.stderr.write(f'Ошибка валидации: {e}')
        except Exception as e:
            logger.exception('Непредвиденная ошибка')
            self.stderr.write(f'Непредвиденная ошибка: {e}')

    def extract_file_id(self, url):
        match = re.match(r'^https?://drive\.google\.com/file/d/([^/]+)/', url)
        if match:
            return match.group(1)
        else:
            raise ValueError('Некорректная ссылка Google Drive')

    def get_direct_download_link(self, file_id):
        return f'https://drive.google.com/uc?export=download&id={file_id}'

    def process_log_file(self, response):
        line_buffer = ''
        objects = []
        batch_size = 1000
        chunk_size = 4096
        success_count = 0
        error_count = 0

        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                decoded_chunk = chunk.decode('utf-8')
                lines = (line_buffer + decoded_chunk).split('\n')
                line_buffer = lines.pop()
                for line in lines:
                    if line.strip():
                        try:
                            obj = self.parse_line(line)
                            objects.append(obj)
                            success_count += 1
                            if len(objects) >= batch_size:
                                self.save_to_db(objects)
                                objects = []
                        except Exception as e:
                            error_count += 1
                            logger.error(f'Ошибка при разборе строки: {e}')
                            self.stderr.write(f'Ошибка при разборе строки: {e}')

        if line_buffer.strip():
            try:
                obj = self.parse_line(line_buffer)
                objects.append(obj)
                success_count += 1
            except Exception as e:
                error_count += 1
                logger.error(f'Ошибка при разборе строки: {e}')
                self.stderr.write(f'Ошибка при разборе строки: {e}')

        if objects:
            self.save_to_db(objects)

        return success_count, error_count

    def parse_line(self, line):
        data = orjson.loads(line)
        timestamp = datetime.strptime(data['time'], '%d/%b/%Y:%H:%M:%S %z')
        return LogEntry(
            ip_address=data['remote_ip'],
            timestamp=timestamp,
            http_method=data['request'].split(' ')[0],
            uri=data['request'].split(' ')[1],
            response_code=int(data['response']),
            response_size=int(data['bytes']),
        )

    def save_to_db(self, objects):
        with transaction.atomic():
            LogEntry.objects.bulk_create(objects)
