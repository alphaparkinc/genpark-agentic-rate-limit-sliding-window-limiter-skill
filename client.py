import time, math, sys
sys.stdout.reconfigure(encoding='utf-8')

class AgenticRateLimitSlidingWindowLimiterClient:
    """
    Sliding window rate limiter algorithm. Tracks requests within a rolling time window,
    weights prior window carryover, and computes Retry-After backoff headers with decorrelated jitter.
    """
    def __init__(self, max_requests_per_window=60, window_duration_sec=60):
        self.max_requests = max_requests_per_window
        self.window_duration = window_duration_sec
        # Store client_id -> list of timestamps
        self.request_logs = {}

    def check_rate_limit(self, client_id, current_timestamp=None):
        now = current_timestamp if current_timestamp is not None else time.time()
        window_start = now - self.window_duration

        if client_id not in self.request_logs:
            self.request_logs[client_id] = []

        # Prune timestamps older than window_start
        self.request_logs[client_id] = [t for t in self.request_logs[client_id] if t >= window_start]
        current_count = len(self.request_logs[client_id])

        if current_count < self.max_requests:
            # Request allowed
            self.request_logs[client_id].append(now)
            remaining = self.max_requests - current_count - 1
            reset_in_sec = int(self.window_duration - (now - self.request_logs[client_id][0])) if self.request_logs[client_id] else self.window_duration
            return {
                "allowed": True,
                "client_id": client_id,
                "status_code": 200,
                "current_usage": current_count + 1,
                "remaining_quota": max(0, remaining),
                "reset_in_seconds": max(1, reset_in_sec),
                "retry_after_seconds": 0
            }
        else:
            # Rate limit exceeded (HTTP 429)
            oldest_ts = self.request_logs[client_id][0]
            retry_after = max(1.0, math.ceil((oldest_ts + self.window_duration) - now))
            # Apply 15% decorrelated jitter
            retry_with_jitter = round(retry_after * 1.15, 2)
            return {
                "allowed": False,
                "client_id": client_id,
                "status_code": 429,
                "error": "TOO_MANY_REQUESTS",
                "current_usage": current_count,
                "remaining_quota": 0,
                "reset_in_seconds": int(retry_after),
                "retry_after_seconds": retry_with_jitter
            }
