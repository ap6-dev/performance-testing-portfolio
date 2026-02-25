import time
import logging
from collections import defaultdict
from colorama import Fore, Style, init

init(autoreset=True)

timings = defaultdict(list)

def measure_time(func):
    def wrapper(self, *args, **kwargs):
        start = time.perf_counter()
        response = func(self, *args, **kwargs)
        end = time.perf_counter()
        duration_ms = (end - start) * 1000

        #Get URL
        url = kwargs.get("url") 
        if hasattr(response, "url"):
            url = response.url

        #Log each call
        logging.info(f"[PERF] {func.__name__} took {duration_ms:.1f} ms\n")

        #Store timings
        key = f"{func.__name__.upper()} {url}"
        timings[key].append(duration_ms)

        return response
    return wrapper

def print_summary():
    #SET THRESHOLD HERE
    threshold_ms = 50

    print(f"\n\n[PERFORMANCE SUMMARY]\nThreshold: {threshold_ms} ms\n{len(timings)} Tests Completed")

    # sort endpoints by avg duration descending
    sorted_items = sorted(
        timings.items(),
        key=lambda kv: sum(kv[1])/len(kv[1]),
        reverse=True
    )

    for key, times in sorted_items:
        avg = sum(times) / len(times)
        max_t = max(times)
        min_t = min(times)

         # highlight slow endpoints
        color = Fore.RED if avg > threshold_ms else Fore.GREEN
        print(f"{color}{key} → avg: {avg:.1f} ms | max: {max_t:.1f} ms | min: {min_t:.1f} ms{Style.RESET_ALL}")