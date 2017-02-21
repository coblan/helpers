from django.http import HttpResponse
from django.conf import settings
import os
from datetime import datetime
import json
import hashlib
import io
import urlparse
from django.views.decorators.csrf import csrf_exempt


def general(request):
    request.File