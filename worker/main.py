from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import time

from fetchers.rss_fetcher import fetch_jobs  
from diff.comparator import filter_new_items
from db.postgres import SessionLocal, Alert, User
from service.email_sender import send_email

load_dotenv()


def should_run(alert):
    now = datetime.now(timezone.utc)

    if alert.last_checked_at is None:
        return True

    delta = now - alert.last_checked_at

    if alert.frequency == "daily":
        return delta >= timedelta(days=1)
    elif alert.frequency == "weekly":
        return delta >= timedelta(weeks=1)
    elif alert.frequency == "monthly":
        return delta >= timedelta(days=30)

    return True


def build_subject(alert):
    return f"New job alerts for: {alert.query}"


def build_body(items):
    lines = []

    for item in items:
        lines.append(f"💼 {item['title']}")
        lines.append(f"🏢 {item['company']}")
        lines.append(f"📍 {item['location']}")
        lines.append(f"🔗 Apply here: {item['link']}")
        lines.append("")

    return "\n".join(lines)


def dedupe(items):
    seen = set()
    unique = []

    for item in items:
        if item["id"] not in seen:   
            seen.add(item["id"])
            unique.append(item)

    return unique


def run_worker():
    print("\n=== NotifyX Job Worker Started ===\n")

    db = SessionLocal()

    try:
        alerts = db.query(Alert).filter(Alert.is_active == True).all()
        print(f"Found {len(alerts)} active alerts.\n")

        for alert in alerts:
            if not should_run(alert):
                print(f"Skipping Alert #{alert.id} (not due)")
                continue

            print(f"\nProcessing Alert #{alert.id} -> {alert.query}")

            #  FETCH JOBS ONLY
            items = fetch_jobs(alert.query)
            print(f"Jobs fetched: {len(items)}")

            #  REMOVE DUPLICATES
            items = dedupe(items)
            print(f"After dedupe: {len(items)}")

            user = db.query(User).filter(User.id == alert.user_id).first()
            if not user:
                print(f"No user found for ID {alert.user_id}")
                continue

            now = datetime.now(timezone.utc)

            #  HANDLE EMPTY
            if not items:
                print(" No jobs found → skipping")

                alert.last_checked_at = now
                db.commit()
                continue

            #  FIRST TIME
            if alert.last_checked_at is None:
                print("📨 First time → sending email")

                send_email(
                    user.email,
                    build_subject(alert),
                    build_body(items)
                )
                print(f"Email sent to {user.email}")

            else:
                print("Checking for new jobs...")

                new_items = filter_new_items(items, alert.last_checked_at)

                print(f"New jobs found: {len(new_items)}")

                if new_items:
                    send_email(
                        user.email,
                        build_subject(alert),
                        build_body(new_items)
                    )
                    print(f"📨 Email sent to {user.email}")
                else:
                    print("No new jobs → skipping email")

            #  UPDATE TIME (IMPORTANT)
            latest_time = max(item["published_at"] for item in items)
            alert.last_checked_at = latest_time

            db.commit()

    except Exception as e:
        print(" Worker error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    while True:
        run_worker()
        time.sleep(60)