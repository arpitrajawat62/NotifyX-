import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")


def fetch_jobs(query: str):
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": "1",
        "num_pages": "1"
    }

    print(f"\nFetching jobs for: {query}")

    try:
        response = requests.get(url, headers=headers, params=params)
        print("Status Code:", response.status_code)

        data = response.json()

        items = []

        for job in data.get("data", []):

            title = job.get("job_title")
            company = job.get("employer_name")
            location = job.get("job_city")
            link = job.get("job_apply_link")   
            job_id = job.get("job_id")

            print(f"✅ {title} at {company}")

            items.append({
                "id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "published_at": datetime.now(timezone.utc)
            })

        print(f"Total jobs fetched: {len(items)}")

        return items

    except Exception as e:
        print("🔥 Error:", e)
        return []