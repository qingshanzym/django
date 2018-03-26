#!/usr/bin/env python
# 这是启动文件，如果django那里报红，则是因为django-py3的虚拟环境没有加载。
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
