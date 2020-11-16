import os
import dotenv


def handler(event, context):
    dotenv.read_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codear.settings')
    from django.core.management import execute_from_command_line

    execute_from_command_line(event['command'])
