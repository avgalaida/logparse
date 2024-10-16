from django.utils import timezone
import factory
from logs_app.models import LogEntry


class LogEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LogEntry

    ip_address = factory.Faker('ipv4')
    timestamp = factory.Faker('date_time', tzinfo=timezone.utc)
    http_method = factory.Iterator(['GET', 'POST', 'PUT', 'DELETE'])
    uri = factory.Sequence(lambda n: f'/test/uri/{n}')
    response_code = factory.Iterator([200, 404, 500])
    response_size = factory.Faker('random_int', min=0, max=1000)
