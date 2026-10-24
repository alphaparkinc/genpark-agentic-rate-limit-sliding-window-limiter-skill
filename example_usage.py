from client import AgenticRateLimitSlidingWindowLimiterClient
import time, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    limiter = AgenticRateLimitSlidingWindowLimiterClient(max_requests_per_window=5, window_duration_sec=10)
    print("=== AGENTIC RATE LIMIT SLIDING WINDOW LIMITER ===")
    
    client_id = "agent_crawler_01"
    base_time = 1000.0
    
    print(f"Policy: Max 5 requests per 10-second rolling window for {client_id}")
    print()
    for req_num in range(1, 8):
        t = base_time + (req_num * 0.8)
        res = limiter.check_rate_limit(client_id, current_timestamp=t)
        status_msg = "ALLOWED" if res['allowed'] else f"REJECTED (Retry in {res['retry_after_seconds']}s)"
        print(f"Request {req_num} (t={t:.1f}s): [{res['status_code']}] {status_msg} | Remaining: {res['remaining_quota']}")

if __name__ == "__main__":
    main()
