from django.core.files.storage import FileSystemStorage
from django.conf import settings

class CacheStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(location=settings.CACHE_ROOT, *args, **kwargs)