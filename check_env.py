import os
from dotenv import load_dotenv

load_dotenv()
mock_setting = os.getenv("USE_MOCK_AGENTS")
brave_key = os.getenv("BRAVE_API_KEY")

with open("env_check.txt", "w") as f:
    f.write(f"USE_MOCK_AGENTS: {mock_setting}\n")
    f.write(f"BRAVE_API_KEY: {'Set' if brave_key else 'Missing'}\n")
