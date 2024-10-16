from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('timestamp', models.DateTimeField()),
                ('http_method', models.CharField(max_length=10)),
                ('uri', models.CharField(max_length=200)),
                ('response_code', models.IntegerField()),
                ('response_size', models.IntegerField()),
            ],
            options={
                'indexes': [models.Index(fields=['ip_address'], name='logs_app_lo_ip_addr_53a00b_idx'), models.Index(fields=['timestamp'], name='logs_app_lo_timesta_c6b8de_idx'), models.Index(fields=['response_code'], name='logs_app_lo_respons_65e789_idx')],
            },
        ),
    ]
