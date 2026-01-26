#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keepalive Daemon Thread
Pings dependent services in the background to keep them online.
"""

import threading
import time
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
KEEPALIVE_TARGETS = [
    {
        "name": "net-test",
        "url": "https://net-test.streamlit.app/",
        "interval_minutes": 30
    }
]

# Track if daemon has been started (singleton pattern)
_daemon_started = False
_daemon_lock = threading.Lock()


def ping_service(url: str, name: str) -> bool:
    """
    Ping a service URL to keep it alive.

    Args:
        url: The URL to ping
        name: Service name for logging

    Returns:
        True if successful, False otherwise
    """
    try:
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=60)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"[{timestamp}] Keepalive ping to {name}: Status {response.status_code}")
        return response.status_code == 200
    except ImportError:
        logger.warning("requests library not available for keepalive daemon")
        return False
    except Exception as e:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.warning(f"[{timestamp}] Keepalive ping to {name} failed: {e}")
        return False


def keepalive_worker(target: dict):
    """
    Worker function that runs in a daemon thread.
    Pings the target URL at the specified interval.

    Args:
        target: Dictionary with 'name', 'url', and 'interval_minutes'
    """
    name = target["name"]
    url = target["url"]
    interval_seconds = target["interval_minutes"] * 60

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"[{timestamp}] Keepalive daemon started for {name} (interval: {target['interval_minutes']} min)")

    # Initial ping
    ping_service(url, name)

    while True:
        time.sleep(interval_seconds)
        ping_service(url, name)


def start_keepalive_daemon():
    """
    Start the keepalive daemon thread(s) for all configured targets.
    Uses a singleton pattern to ensure only one daemon per target.
    Safe to call multiple times - will only start once.
    """
    global _daemon_started

    with _daemon_lock:
        if _daemon_started:
            return

        for target in KEEPALIVE_TARGETS:
            thread = threading.Thread(
                target=keepalive_worker,
                args=(target,),
                daemon=True,  # Daemon thread - won't block app shutdown
                name=f"keepalive-{target['name']}"
            )
            thread.start()

        _daemon_started = True
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"[{timestamp}] Keepalive daemon threads started")


def is_daemon_running() -> bool:
    """Check if the keepalive daemon has been started."""
    return _daemon_started
