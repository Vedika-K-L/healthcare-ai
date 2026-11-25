from __future__ import annotations

import os
from typing import Any
from urllib.parse import urljoin

import requests


class APIError(RuntimeError):
    """A safe, user-displayable API error."""


class HealthBridgeAPI:
    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.token = token

    @classmethod
    def from_environment(cls, token: str | None = None) -> "HealthBridgeAPI":
        return cls(os.getenv("HEALTHBRIDGE_API_URL", "http://127.0.0.1:4000/api"), token)

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = urljoin(self.base_url, path.lstrip("/"))
        try:
            response = requests.request(
                method,
                url,
                headers={**self._headers(), **kwargs.pop("headers", {})},
                timeout=20,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise APIError(
                "HealthBridge could not reach its API. Check the API URL and confirm the service is running."
            ) from exc

        try:
            payload = response.json()
        except ValueError:
            payload = {}

        if not response.ok:
            message = payload.get("message") if isinstance(payload, dict) else None
            raise APIError(message or f"The HealthBridge API returned an error ({response.status_code}).")
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Any:
        return self.request("PATCH", path, **kwargs)

    def download(self, path: str) -> tuple[bytes, str]:
        url = urljoin(self.base_url, path.lstrip("/"))
        try:
            response = requests.get(url, headers=self._headers(), timeout=30)
        except requests.RequestException as exc:
            raise APIError("The private file could not be reached. Please try again.") from exc
        if not response.ok:
            try:
                message = response.json().get("message")
            except (ValueError, AttributeError):
                message = None
            raise APIError(message or "The private file could not be downloaded.")
        disposition = response.headers.get("content-disposition", "")
        filename = "healthbridge-document"
        if "filename=" in disposition:
            filename = disposition.split("filename=", 1)[1].strip('" ')
        return response.content, filename

    def health(self) -> dict[str, Any]:
        return self.get("/health")


def configured_api_url(secrets: Any | None = None) -> str:
    if secrets is not None:
        try:
            value = secrets.get("HEALTHBRIDGE_API_URL")
            if value:
                return str(value)
        except Exception:
            pass
    return os.getenv("HEALTHBRIDGE_API_URL", "http://127.0.0.1:4000/api")
