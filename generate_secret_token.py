import secrets
import base64
from pathlib import Path
random_bytes = secrets.token_bytes(64)
token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')

token_path = Path(__file__).parent / "reset-session-token-secret.txt"

if token_path.exists():
    print("reset-session-token-secret.txt already exists. Skipping creation.")
    exit(-1)

with open(token_path, "w") as f:
    f.write(token)
print(f"Successfully generated secret token in {token_path}.")