from playwright.sync_api import Page
import json

def analyze_performance(page: Page) -> dict:

    print("Worker: Analizando performance...")
    try:
        timing_json = page.evaluate("() => JSON.stringify(window.performance.timing.toJSON())")
        timing = json.loads(timing_json)
        
        if timing.get('loadEventEnd', 0) == 0:
            timing['loadEventEnd'] = timing.get('domComplete', timing.get('navigationStart', 0))

        load_time_ms = timing['loadEventEnd'] - timing['navigationStart']
        
        # API de Resource Timing
        resources_json = page.evaluate("() => JSON.stringify(window.performance.getEntriesByType('resource'))")
        resources = json.loads(resources_json)
        
        num_requests = len(resources)
        
        total_size_kb = sum(
            r.get('transferSize', 0) for r in resources
        ) / 1024
        
        return {
            "load_time_ms": load_time_ms if load_time_ms > 0 else -1,
            "total_size_kb": round(total_size_kb, 2),
            "num_requests": num_requests
        }
    except Exception as e:
        print(f"Worker Error: Falló al analizar performance: {e}")
        return {"error": f"Error al analizar performance: {e}"}