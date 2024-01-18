"""A simple Gramps Web API Client."""

from typing import Optional, Tuple
from urllib.parse import urlencode

import requests

API_PREFIX = "/api"
ENDPOINT_TOKEN = "/token/"
ENDPOINT_PEOPLE = "/people/"
ENDPOINT_EVENTS = "/events/"
ENDPOINT_PLACES = "/places/"
PAGE_SIZE = 200


class API:
    """API."""

    def __init__(
        self,
        host: str = "http://127.0.0.1:5555",
        basic_auth: Optional[Tuple[str, str]] = None,
    ):
        """Inititalize self."""
        self.host = host.rstrip("/")
        if basic_auth:
            self.user, self.password = basic_auth
        else:
            raise ValueError("basic_auth is required")
        self._access_token = ""
        self._refresh_token = ""

    def _endpoint_url(self, endpoint: str):
        """Build a full URL for the given endpoint."""
        return f"{self.host}{API_PREFIX}{endpoint}"

    def _fetch_tokens(self):
        """Fetch tokens."""
        res = requests.post(
            self._endpoint_url(ENDPOINT_TOKEN),
            json={"username": self.user, "password": self.password},
        )
        res.raise_for_status()
        data = res.json()
        self._access_token = data["access_token"]
        self._refresh_token = data["refresh_token"]

    @property
    def _auth_header(self):
        """return the auth header."""
        return {"Authorization": f"Bearer {self._access_token}"}

    def _get(self, endpoint: str):
        """Get data from a protected URL."""
        if not self._access_token:
            self._fetch_tokens()
        url = self._endpoint_url(endpoint)
        res = requests.get(url, headers=self._auth_header)
        res.raise_for_status()
        data = res.json()
        return data

    def _put(self, endpoint: str, data):
        """Put data to a protected URL."""
        if not self._access_token:
            self._fetch_tokens()
        url = self._endpoint_url(endpoint)
        res = requests.put(url, headers=self._auth_header, json=data)
        res.raise_for_status()
        data = res.json()
        return data

    def _post(self, endpoint: str, data):
        """Post data to a protected URL."""
        if not self._access_token:
            self._fetch_tokens()
        url = self._endpoint_url(endpoint)
        res = requests.post(url, headers=self._auth_header, json=data)
        res.raise_for_status()
        data = res.json()
        return data

    def _get_object(self, object_endpoint: str, handle: str):
        """Get a single object."""
        if not handle:
            raise ValueError("handle is required")
        endpoint = f"{object_endpoint}{handle}"
        return self._get(endpoint)

    def _put_object(self, object_endpoint: str, handle: str, data):
        """Put a single object."""
        if not handle:
            raise ValueError("handle is required")
        endpoint = f"{object_endpoint}{handle}"
        return self._put(endpoint, data)

    def _iter_objects(self, object_endpoint: str, **kwargs):
        """Iterate over objects."""
        page = 1
        while True:
            endpoint = f"{object_endpoint}?pagesize={PAGE_SIZE}&page={page}"
            for key, value in kwargs.items():
                if not isinstance(value, str):
                    value = urlencode(value)
                endpoint += f"&{key}={value}"
            data = self._get(endpoint)
            if not len(data):
                break
            for obj in data:
                yield obj
            page += 1

    def _update_object(self, object_endpoint: str, handle: str, data):
        """Update an object."""
        old_data = self._get_object(object_endpoint, handle)
        new_data = {**old_data, **data}
        return self._put_object(object_endpoint, handle, new_data)

    def get_person(self, handle: str):
        """Get a single person."""
        return self._get_object(ENDPOINT_PEOPLE, handle)

    def get_event(self, handle: str):
        """Get a single event."""
        return self._get_object(ENDPOINT_EVENTS, handle)

    def get_place(self, handle: str):
        """Get a single place."""
        return self._get_object(ENDPOINT_PLACES, handle)

    def iter_people(self, **kwargs):
        """Iterate over people."""
        return self._iter_objects(ENDPOINT_PEOPLE, **kwargs)

    def iter_events(self, **kwargs):
        """Iterate over events."""
        return self._iter_objects(ENDPOINT_EVENTS, **kwargs)

    def iter_places(self, **kwargs):
        """Iterate over places."""
        return self._iter_objects(ENDPOINT_PLACES, **kwargs)

    def update_person(self, handle: str, data):
        """Update a person."""
        return self._update_object(ENDPOINT_PEOPLE, handle, data)

    def update_event(self, handle: str, data):
        """Update an event."""
        return self._update_object(ENDPOINT_EVENTS, handle, data)

    def update_place(self, handle: str, data):
        """Update a place."""
        return self._update_object(ENDPOINT_PLACES, handle, data)

    def create_person(self, data):
        """Create a person."""
        return self._post(ENDPOINT_PEOPLE, data)

    def create_event(self, data):
        """Create ab event."""
        return self._post(ENDPOINT_EVENTS, data)

    def create_place(self, data):
        """Create a place."""
        return self._post(ENDPOINT_PLACES, data)
