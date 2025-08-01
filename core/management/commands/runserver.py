print("Custom runserver.py loaded!")

from django.contrib.staticfiles.management.commands.runserver import Command as StaticfilesRunserverCommand
from pyngrok import ngrok
from decouple import config
import os

class Command(StaticfilesRunserverCommand):
    def inner_run(self, *args, **options):
        print("Custom runserver inner_run started!")
        auth_token = config("NGROK_AUTH_TOKEN", default=None)
        if auth_token:
            ngrok.set_auth_token(auth_token)

        addrport = options.get('addrport')
        if addrport is None:
            port = '8000'
        else:
            if ':' in addrport:
                port = addrport.split(':')[1]
            else:
                port = addrport

        public_url = ngrok.connect(port)
        os.environ["NGROK_PUBLIC_URL"] = public_url.public_url
        print(f"\n🌐 Ngrok tunnel: {public_url.public_url}\n")

        super().inner_run(*args, **options)
