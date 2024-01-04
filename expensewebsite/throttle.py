from rest_framework import throttling

class automation_throttle(throttling.UserRateThrottle):
    scope='automation'