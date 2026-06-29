import re
import uuid
from datetime import datetime

_TRANSLIT_MAP = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "i", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "",
    "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya", "і": "i", "ї": "yi",
    "є": "ye", "ґ": "g",
}

def slugify(text: str) -> str:

    text = text.lower().strip()
    text = "".join(_TRANSLIT_MAP.get(ch, ch) for ch in text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or uuid.uuid4().hex[:8]

def generate_order_number() -> str:

    date_part = datetime.utcnow().strftime("%Y%m%d")
    rand_part = uuid.uuid4().hex[:6].upper()
    return f"ORD-{date_part}-{rand_part}"
