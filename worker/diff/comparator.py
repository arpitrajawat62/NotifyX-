from datetime import datetime

def filter_new_items(items, last_checked_at: datetime):

    if last_checked_at is None:
        return items

    new_items = []

    for item in items:
        published_at = item["published_at"]

        if published_at > last_checked_at:
            new_items.append(item)
        
    return new_items