#!/usr/bin/env python
import os
import sys

# import our environment from .env
import dotenv
dotenv.read_dotenv()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workshop.settings_development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
