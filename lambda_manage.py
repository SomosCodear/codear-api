import os


def handler(event, context):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codear.settings')
    from django.core.management import execute_from_command_line

    execute_from_command_line(['lambda_manage', event['command']])
