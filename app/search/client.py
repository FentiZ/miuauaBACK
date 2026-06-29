from typing import Optional
from elasticsearch import Elasticsearch, NotFoundError, RequestError

from app.search.config import ES_HOSTS, ES_USERNAME, ES_PASSWORD, ES_CA_CERT, PRODUCT_MAPPING

_client: Optional[Elasticsearch] = None

def get_es_client() -> Optional[Elasticsearch]:
    global _client
    if _client is not None:
        return _client
    try:
        kwargs: dict = {"hosts": ES_HOSTS}
        if ES_USERNAME and ES_PASSWORD:
            kwargs["basic_auth"] = (ES_USERNAME, ES_PASSWORD)
        if ES_CA_CERT:
            kwargs["ca_certs"] = ES_CA_CERT
        _client = Elasticsearch(**kwargs)
        if not _client.ping():
            _client = None
    except Exception:
        _client = None
    return _client

def ensure_index(index: str) -> bool:
    client = get_es_client()
    if client is None:
        return False
    try:
        if not client.indices.exists(index=index):
            client.indices.create(index=index, body=PRODUCT_MAPPING)
        return True
    except RequestError:
        return False

def ensure_all_indices(indices: dict) -> None:
    for index in indices.values():
        ensure_index(index)
