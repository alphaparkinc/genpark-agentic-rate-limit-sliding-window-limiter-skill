import sys, json
from client import AgenticRateLimitSlidingWindowLimiterClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    limiter = AgenticRateLimitSlidingWindowLimiterClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-agentic-rate-limit-sliding-window-limiter-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    cid = req.get("client_id", "default_client")
    res = limiter.check_rate_limit(cid)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
