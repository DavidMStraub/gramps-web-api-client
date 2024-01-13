# Gramps Web API Client


A simple Python client based on `requests` for interacting with a [Gramps Web API](https://github.com/gramps-project/gramps-webapi/) server.

## Warning

This is an experimental project for advanced users. The goal is to allow powerful batch operations on Gramps objects via the API. But only use it if you know what you are doing &ndash; you can easily break your Gramps database with this tool!

## Quick start

First, instantiate the API instance:

```python
from gramps_web_api_client import API

api = API(
    host="https://my-gramps-web-instance.com",
    basic_auth("my_user", "my_password")
)
```

Methods currently implemented:


| Method  | description |
| ------------- | ------------- |
| `api.iter_people()`  | Generator iterating over people  |
| `api.iter_events()`  | Generator iterating over events  |
| `api.iter_places()`  | Generator iterating over places  |
| `api.get_person(handle)`  | Get a single person by handle  |
| `api.get_event(handle)`  | Get a single event by handle  |
| `api.get_place(handle)`  | Get a single place by handle  |
| `api.update_person(handle, data)`  | Update a single person  |
| `api.update_event(handle, data)`  | Update a single event  |
| `api.update_place(handle, data)`  | Update a single place |
| `api.create_person(data)`  | Create a new person  |
| `api.create_event(data)`  | Create a new evebt  |
| `api.create_place(data)`  | GCreateet a new place  |


In all cases, `data` are dictionaries for JSON objects following the Gramps Web API conventions.

## Examples

Removing all citations from an existing person:

```python
api.update_person("somehandle", {"citation_list": []})
```

In this example, all other properties of the person (except citations) will remain the same.

Creating a new place:

```python
api.create_place({
    "name": {
        "_class": "PlaceName",
        "value": "Gotham City"
    }
})
```

Iterating over people and adding a citation if a condition is satisfied:

```python
for person in api.iter_people():
    try:
        surname = person["primary_name"]["surname_list"][0]["surname"]
    except (KeyError, IndexError):
        continue
    if surname == "Garner":
        api.update_person(
            person["handle"],
            {"citation_list": person["citation_list"] + ["some_citation_handle"]}
        )    
```