import logging

from django.conf import settings
from django.core.cache import caches
from rest_framework.throttling import SimpleRateThrottle
from cloud_explorer.models import UserRateLimit

logger = logging.getLogger(__name__)


class PerUserThrottling(SimpleRateThrottle):
    """
        Class can use throttling set at user level. Throttling can be set in database.
        Since DB access can be slow, user throttle rate is also stored in cache and it expires strictly after 600 seconds
    """

    cache = caches[settings.THROTTLING_CACHE_BACKEND]
    throttle_info_timeout = 600
    throttle_info_key = "{user_id}_throttle_rate"
    current_requests_key = "{user_id}_current_rate"

    def __init__(self):
        self.user_id = None

    def get_cache_key(self, request, view):
        """
        Should return a unique cache-key which can be used for throttling.
        Must be overridden.
        May return `None` if the request should not be throttled.
        """
        if self.user_id:
            return self.current_requests_key.format(user_id=self.user_id)
        return None

    def get_rate(self, request):
        """
        Determine the string representation of the allowed request rate.
        """
        rate = None
        if request.user.is_authenticated:
            # check for user rate in cache. If not found, pick from
            self.user_id = request.user.id
            cache_key = self.throttle_info_key.format(user_id=request.user.id)
            rate = self.cache.get(cache_key, None)
            if not rate:
                logger.info(f"Rate for user - {self.user_id} not set in cache. Fetching from DB")
                try:
                    user_rate_limit = UserRateLimit.objects.filter(user=request.user)
                    if len(user_rate_limit):
                        rate = user_rate_limit[0].rate_limit
                        self.cache.set(cache_key, rate, timeout=self.throttle_info_timeout)
                    else:
                        logger.info(f"User - {request.user.username} has no rate limit")
                except Exception as e:
                    logger.exception(f"Failed to get rate limit for user - {self.user_id} |  Error  - {e}")
        logger.info(f"Returning rate limit {rate}")
        return rate

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.
        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        rate = self.get_rate(request)
        if rate is None:
            return True

        self.num_requests, self.duration = self.parse_rate(rate)

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        current_requests = self.cache.get(self.key, None)
        if current_requests is None and self.num_requests and self.duration:
            # set key for user
            self.cache.set(self.key, 0, timeout=self.duration)
            current_requests = 0

        self.now = self.timer()

        logger.info(f"Requests already served - {current_requests} | Total Allowed - {self.num_requests}")

        if current_requests >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()

    def throttle_success(self):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        self.cache.incr(self.key, delta=1)
        return True

    def throttle_failure(self):
        """
        Called when a request to the API has failed due to throttling.
        """
        return False

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        return 1
