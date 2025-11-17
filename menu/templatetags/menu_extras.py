from decimal import Decimal
from urllib.parse import urlparse, urlunparse, urlencode, parse_qsl

from django import template

register = template.Library()


@register.filter(name='inr')
def inr(value):
    try:
        amount = Decimal(value)
    except Exception:
        return value
    return f"₹{amount:.2f}"


DEFAULT_IMG = (
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=60"
)


@register.filter(name='img_url')
def img_url(src):
    if not src:
        return DEFAULT_IMG

    try:
        parsed = urlparse(str(src))

        # If it's an unsplash page URL → convert it
        if "unsplash.com/photos" in parsed.geturl() and "images.unsplash.com" not in parsed.netloc:
            try:
                photo_id = parsed.path.split("/")[-1]  # extract ID
                # Convert page URL → direct image URL
                return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=60"
            except:
                return DEFAULT_IMG

        # If already a proper images.unsplash.com URL
        if "images.unsplash.com" in parsed.netloc:
            q = dict(parse_qsl(parsed.query))
            q.setdefault("auto", "format")
            q.setdefault("fit", "crop")
            q.setdefault("w", "800")
            q.setdefault("q", "60")
            parsed = parsed._replace(query=urlencode(q))
            return urlunparse(parsed)

        # If anything else → return original
        return src

    except Exception:
        return DEFAULT_IMG


