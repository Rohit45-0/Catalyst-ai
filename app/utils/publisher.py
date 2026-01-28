import os
import requests
import json
from typing import Dict, Any, Optional
from pathlib import Path

class SocialMediaPublisher:
    """
    Handles automated posting to various social media platforms via their APIs.

    Supported Platforms:
    - LinkedIn (UGC Post API) with automatic token refresh
    - Meta (Facebook/Instagram Graph API)
    - Medium (Post API)
    """

    def __init__(self):
        """Initialize with API tokens from environment variables."""
        # LinkedIn - with automatic token refresh support
        self.linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.linkedin_refresh_token = os.getenv("LINKEDIN_REFRESH_TOKEN")
        self.linkedin_person_id = os.getenv("LINKEDIN_PERSON_ID")
        self.linkedin_org_id = os.getenv("LINKEDIN_ORGANIZATION_ID")

        # Meta
        self.meta_access_token = os.getenv("META_ACCESS_TOKEN")
        self.meta_page_id = os.getenv("META_PAGE_ID")
        self.instagram_id = os.getenv("INSTAGRAM_BUSINESS_ID")

        # Medium
        self.medium_token = os.getenv("MEDIUM_INTEGRATION_TOKEN")
        self.medium_user_id = os.getenv("MEDIUM_USER_ID")

        # LinkedIn credentials for token refresh
        self.linkedin_client_id = os.getenv("LINKEDIN_CLIENT_ID", "77entx67zq9zwo")
        self.linkedin_client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")

    def _refresh_linkedin_token(self) -> bool:
        """
        Automatically refresh LinkedIn access token using refresh token.
        No user interaction needed!
        """
        if not self.linkedin_refresh_token:
            print("  ⚠️ No refresh token available. Cannot auto-refresh.")
            return False

        try:
            print("  🔄 Access token expired. Refreshing automatically...")
            url = "https://www.linkedin.com/oauth/v2/accessToken"
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.linkedin_refresh_token,
                "client_id": self.linkedin_client_id,
                "client_secret": self.linkedin_client_secret
            }
            response = requests.post(url, data=data)

            if response.status_code == 200:
                token_data = response.json()
                new_token = token_data.get("access_token")

                if new_token:
                    self.linkedin_token = new_token

                    # Update .env file
                    env_path = Path(".env")
                    if env_path.exists():
                        content = env_path.read_text()
                        if "LINKEDIN_ACCESS_TOKEN=" in content:
                            content = content.replace(
                                [line for line in content.split("\n") if line.startswith("LINKEDIN_ACCESS_TOKEN=")][0],
                                f"LINKEDIN_ACCESS_TOKEN={new_token}"
                            )
                        else:
                            content += f"\nLINKEDIN_ACCESS_TOKEN={new_token}"
                        env_path.write_text(content)

                    print(f"  ✅ Token refreshed successfully!")
                    return True
            else:
                print(f"  ❌ Failed to refresh token: {response.text}")
                return False
        except Exception as e:
            print(f"  ❌ Error refreshing token: {str(e)}")
            return False

    def _upload_linkedin_image(self, image_path: str) -> Optional[str]:
        """
        Upload image to LinkedIn and return the asset URN for posting.

        Multi-step process:
        1. Register upload with LinkedIn
        2. Get upload URL
        3. Upload binary image data
        4. Return asset URN
        """
        if not image_path or not os.path.exists(image_path):
            print(f"  ⚠️ Image not found: {image_path}")
            return None

        try:
            print(f"  [*] Uploading image to LinkedIn...")

            # Step 1: Register the upload
            register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
            headers = {
                "Authorization": f"Bearer {self.linkedin_token}",
                "Content-Type": "application/json"
            }

            register_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:organization:{self.linkedin_org_id}",
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }

            response = requests.post(register_url, json=register_payload, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"  [!] Registration failed ({response.status_code})")
                print(f"      Error: {response.text[:200]}")
                return None

            register_data = response.json()
            print(f"  [DEBUG] Registration response keys: {register_data.keys()}")

            # Extract upload URL - handle different response formats
            upload_url = None
            asset_id = None

            if "value" in register_data:
                value = register_data["value"]
                asset_id = value.get("asset")

                # Try to get upload URL from uploadMechanism
                upload_mechanism = value.get("uploadMechanism", {})
                if upload_mechanism:
                    # Try different possible keys
                    mech_key = "com.linkedin.digitalmedia.uploading.AssetUploadHttpPutUploadMechanism"
                    if mech_key in upload_mechanism:
                        upload_url = upload_mechanism[mech_key].get("uploadUrl")
                    else:
                        # Try to get first available upload mechanism
                        for key, val in upload_mechanism.items():
                            if isinstance(val, dict) and "uploadUrl" in val:
                                upload_url = val["uploadUrl"]
                                break

            if not upload_url or not asset_id:
                print(f"  [!] Missing upload URL or asset ID")
                print(f"      Asset ID: {asset_id}")
                print(f"      Upload URL: {upload_url}")
                return None

            print(f"  [+] Got upload URL, uploading image...")

            # Step 2: Upload the image binary
            with open(image_path, "rb") as img_file:
                image_data = img_file.read()

            print(f"  [*] Image size: {len(image_data)} bytes")

            put_headers = {
                "Content-Type": "image/jpeg"
            }

            put_response = requests.put(upload_url, data=image_data, headers=put_headers, timeout=30)

            if put_response.status_code not in [200, 201]:
                print(f"  [!] Upload failed ({put_response.status_code})")
                print(f"      Error: {put_response.text[:200]}")
                return None

            print(f"  [+] Image uploaded successfully!")
            print(f"  [*] Asset ID: {asset_id}")
            return asset_id

        except Exception as e:
            print(f"  ❌ Image upload error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def post_to_linkedin(self, title: str, content: str, hashtags: list, image_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Post content to LinkedIn with optional image.

        Auto-refreshes token on 401 error.
        """
        if not self.linkedin_token:
            return {"status": "error", "message": "LinkedIn token not configured"}

        try:
            # Prepare content
            text = f"{title}\n\n{content}"
            if hashtags:
                text += "\n\n" + " ".join([f"#{tag.lstrip('#')}" for tag in hashtags])

            # Remove special Unicode characters (keep ASCII only)
            text = text.encode('ascii', 'ignore').decode('ascii')
            # Convert smart quotes to regular quotes
            text = text.replace('"', '"').replace('"', '"').replace("'", "'").replace("'", "'")

            url = "https://api.linkedin.com/v2/ugcPosts"
            headers = {
                "Authorization": f"Bearer {self.linkedin_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }

            payload = {
                "author": f"urn:li:organization:{self.linkedin_org_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            # Add image if provided
            if image_path:
                asset_id = self._upload_linkedin_image(image_path)
                if asset_id:
                    payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                    payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                        {
                            "status": "READY",
                            "media": asset_id
                        }
                    ]
                else:
                    print("  ⚠️ Image upload failed, posting without image...")

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 401:
                # Token expired, try to refresh
                if self._refresh_linkedin_token():
                    # Retry with new token
                    headers["Authorization"] = f"Bearer {self.linkedin_token}"
                    response = requests.post(url, json=payload, headers=headers)

            if response.status_code in [200, 201]:
                post_id = response.headers.get("X-RestLi-Id", "unknown")
                print(f"  [+] LinkedIn post published! ID: {post_id}")
                return {
                    "status": "success",
                    "message": "Post published to LinkedIn",
                    "data": {"id": post_id}
                }
            else:
                print(f"  [!] Failed to post to LinkedIn: {response.status_code}")
                print(f"      Response: {response.text}")
                return {
                    "status": "error",
                    "message": f"LinkedIn API error: {response.status_code}",
                    "details": response.text
                }

        except Exception as e:
            error_msg = f"LinkedIn posting error: {str(e)}"
            print(f"  ❌ {error_msg}")
            return {"status": "error", "message": error_msg}

    def post_to_meta(self, caption: str, hashtags: list, image_url: Optional[str] = None) -> Dict[str, Any]:
        """Post to Meta (Facebook/Instagram)."""
        if not self.meta_access_token or not self.meta_page_id:
            return {"status": "error", "message": "Meta credentials not configured"}

        try:
            text = caption
            if hashtags:
                text += "\n\n" + " ".join([f"#{tag.lstrip('#')}" for tag in hashtags])

            url = f"https://graph.instagram.com/{self.meta_page_id}/media"
            params = {"access_token": self.meta_access_token}

            payload = {"caption": text}
            if image_url:
                payload["image_url"] = image_url

            response = requests.post(url, json=payload, params=params)

            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "message": "Post published to Meta",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Meta API error: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {"status": "error", "message": f"Meta posting error: {str(e)}"}

    def post_to_medium(self, title: str, content: str, tags: list) -> Dict[str, Any]:
        """Post to Medium blog platform."""
        if not self.medium_token or not self.medium_user_id:
            return {"status": "error", "message": "Medium credentials not configured"}

        try:
            url = f"https://api.medium.com/v1/users/{self.medium_user_id}/posts"
            headers = {
                "Authorization": f"Bearer {self.medium_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "title": title,
                "content": content,
                "contentFormat": "markdown",
                "publishStatus": "public",
                "tags": tags[:5]  # Medium allows max 5 tags
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "message": "Post published to Medium",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Medium API error: {response.status_code}",
                    "details": response.text
                }
        except Exception as e:
            return {"status": "error", "message": f"Medium posting error: {str(e)}"}
