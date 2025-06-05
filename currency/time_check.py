from django.core.cache import cache
from functools import wraps


def current_rate_limit(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        cache_key = f"api_data_{request.path}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        response = view_func(request, *args, **kwargs)
        cache.set(cache_key, response, timeout=10)
        return response
    return wrapped_view


