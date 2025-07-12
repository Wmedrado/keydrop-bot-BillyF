import logging
from collections import deque
from typing import Dict, List, Optional


class ProxyManager:
    """Manage a rotating pool of proxies and track failures."""

    def __init__(self, proxies: Optional[List[str]] = None, timeout: int = 30):
        self.logger = logging.getLogger(__name__)
        self.proxies = deque(proxies or [])
        self.assigned: Dict[int, str] = {}
        self.failures: Dict[str, int] = {}
        self.timeout = timeout

    def get_proxy(self, tab_id: int) -> Optional[str]:
        """Return a proxy for a tab, assigning a new one if necessary."""
        proxy = self.assigned.get(tab_id)
        if proxy:
            return proxy

        for _ in range(len(self.proxies)):
            candidate = self.proxies.popleft()
            if candidate not in self.assigned.values():
                self.assigned[tab_id] = candidate
                self.proxies.append(candidate)
                self.logger.info("Proxy %s assigned to tab %s", candidate, tab_id)
                return candidate
            self.proxies.append(candidate)

        if self.proxies:
            proxy = self.proxies[0]
            self.assigned[tab_id] = proxy
            self.logger.warning(
                "Reusing proxy %s for tab %s (pool exhausted)", proxy, tab_id
            )
            return proxy

        self.logger.warning("No proxies available for tab %s", tab_id)
        return None

    def report_failure(self, tab_id: int, reason: str = "") -> Optional[str]:
        """Mark the current proxy as failed and assign a new one."""
        proxy = self.assigned.pop(tab_id, None)
        if proxy:
            self.failures[proxy] = self.failures.get(proxy, 0) + 1
            self.logger.warning(
                "Proxy %s failed on tab %s: %s", proxy, tab_id, reason
            )
        return self.get_proxy(tab_id)

    def release_proxy(self, tab_id: int):
        """Release proxy when a tab is closed."""
        self.assigned.pop(tab_id, None)

    def failure_stats(self) -> Dict[str, int]:
        return dict(self.failures)
