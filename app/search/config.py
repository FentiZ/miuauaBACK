import os
from dotenv import load_dotenv

load_dotenv()

ES_HOSTS = os.getenv("ES_HOSTS", "http://localhost:9200").split(",")
ES_USERNAME = os.getenv("ES_USERNAME", "")
ES_PASSWORD = os.getenv("ES_PASSWORD", "")
ES_CA_CERT = os.getenv("ES_CA_CERT", "")

ES_INDICES = {
    "products_ua": os.getenv("ES_INDEX_PRODUCTS_UA", "products_ua"),
    "products_ru": os.getenv("ES_INDEX_PRODUCTS_RU", "products_ru"),
    "products_en": os.getenv("ES_INDEX_PRODUCTS_EN", "products_en"),
}

ES_DEFAULT_INDEX = os.getenv("ES_DEFAULT_INDEX", "products_ua")

PRODUCT_MAPPING = {
    "mappings": {
        "properties": {
            "id":                 {"type": "integer"},
            "name":               {"type": "text", "analyzer": "standard", "fields": {"keyword": {"type": "keyword"}}},
            "slug":               {"type": "keyword"},
            "description":        {"type": "text", "analyzer": "standard"},
            "short_description":  {"type": "text", "analyzer": "standard"},
            "price":              {"type": "float"},
            "old_price":          {"type": "float"},
            "sku":                {"type": "keyword"},
            "stock":              {"type": "integer"},
            "category_id":        {"type": "integer"},
            "category_name":      {"type": "keyword"},
            "category_slug":      {"type": "keyword"},
            "brand_id":           {"type": "integer"},
            "brand_name":         {"type": "keyword"},
            "brand_slug":         {"type": "keyword"},
            "rating_avg":         {"type": "float"},
            "reviews_count":      {"type": "integer"},
            "view_count":         {"type": "integer"},
            "is_new":             {"type": "boolean"},
            "is_top":             {"type": "boolean"},
            "is_active":          {"type": "boolean"},
            "discount_percent":   {"type": "integer"},
            "loyalty_partner":    {"type": "keyword"},
            "review_bonus_points":{"type": "integer"},
            "main_image":         {"type": "keyword", "index": False},
            "created_at":         {"type": "date"},
            "updated_at":         {"type": "date"},
        }
    },
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
    }
}
