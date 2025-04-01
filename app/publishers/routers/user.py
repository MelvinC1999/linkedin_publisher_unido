import requests
from app.core.config import settings

def get_user_info():
    try:
        headers = {
            "Authorization": f"Bearer {settings.LINKEDIN_ACCESS_TOKEN}",
            "Linkedin-Version": "202503"
        }

        response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)

        if response.status_code == 200:
            data = response.json()
            user_id = data.get("sub")
            return {
                "user_urn": f"urn:li:person:{user_id}"
            }
        else:
            return {
                "error": f"Error {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {"error": str(e)}