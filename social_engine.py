import os
import re
import sys
import requests
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# 1. Configuration & Initializations
# ---------------------------------------------------------------------------
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "gvf-dynamics-infrastructure")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
LINKEDIN_ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_ORGANIZATION_URN = os.environ.get("LINKEDIN_ORGANIZATION_URN")

SYSTEM_PROMPT = """
You are the Lead Developer Advocate at GVF Dynamics.
Write a deep technical, highly authoritative LinkedIn post about GVF Orchestrator Core.

Topic focus areas:
- Kahn's Algorithm for DAG dependency sorting in multi-agent execution.
- SHA-256 state deduplication to prevent context window bloating.
- Transactional sandboxing & dry-run rollbacks in Compute-In-Memory (CIM) edge devices.
- SemVer tool namespacing to avoid cross-agent function collisions.

Style Guidelines:
- Professional, engineering-focused tone (no fluff, no emoji spam).
- Include ASCII architectural diagrams or code snippet logic where appropriate.
- Focus on real multi-agent failure modes (infinite loops, race conditions, non-deterministic state).
- End with a call to action directing readers to inspect docs or perpetual developer licenses at www.gvfdynamics.com.
"""

# ---------------------------------------------------------------------------
# 2. Local Guardrail Security Scan
# ---------------------------------------------------------------------------
def run_security_guardrail(content: str) -> bool:
    print("\n[Guardrail] Scanning generated content for sensitive leak vectors...")
    
    secret_patterns = [
        r"AIzaSy[A-Za-z0-9_-]{33}",           # GCP API Keys
        r"sk-[A-Za-z0-9]{32,}",               # Generic Secret Keys
        r"AQ[A-Za-z0-9_-]{100,}",              # LinkedIn Access Tokens
        r"C:\\Users\\[A-Za-z0-9_-]+",          # Windows File Paths
        r"/home/[A-Za-z0-9_-]+",              # Linux Home Paths
        r"(?i)private_key|secret_key|passwd"  # Sensitive keyword tags
    ]

    for pattern in secret_patterns:
        if re.search(pattern, content):
            print(f"❌ [GUARDRAIL VIOLATION DETECTED]: Matched pattern '{pattern}'")
            return False

    print("✅ [GUARDRAIL PASSED]: Zero secrets, path exposures, or state leaks detected.")
    return True

# ---------------------------------------------------------------------------
# 3. Content Generation via Modern Gen AI Client (Gemini 2.5 Pro)
# ---------------------------------------------------------------------------
def generate_technical_post(topic: str) -> str:
    print(f"[Vertex AI] Generating technical post for topic: '{topic}'...")
    
    # Initialize the modern unified Client configured for Vertex AI
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    
    prompt = f"{SYSTEM_PROMPT}\n\nToday's Specific Topic: {topic}"
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1024,
            temperature=0.3,
            top_p=0.8
        )
    )
    
    return response.text

# ---------------------------------------------------------------------------
# 4. LinkedIn API Publishing Engine
# ---------------------------------------------------------------------------
def publish_to_linkedin(post_body: str) -> dict:
    if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_ORGANIZATION_URN:
        raise ValueError("Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_ORGANIZATION_URN environment variables.")

    url = "https://api.linkedin.com/v2/posts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": LINKEDIN_ORGANIZATION_URN,
        "commentary": post_body,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    print(f"\n[LinkedIn API] Dispatching post payload to {LINKEDIN_ORGANIZATION_URN}...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("🚀 [SUCCESS]: Technical post successfully published to LinkedIn!")
        return response.json()
    else:
        print(f"❌ [LinkedIn API Error] ({response.status_code}): {response.text}")
        response.raise_for_status()

# ---------------------------------------------------------------------------
# 5. Pipeline Execution Entrypoint
# ---------------------------------------------------------------------------
def main():
    topic = "Deterministic Cycle Prevention in Multi-Agent Pipelines via Kahn's Algorithm"
    
    try:
        post_content = generate_technical_post(topic)
        print("\n--- GENERATED POST DRAFT ---")
        print(post_content)
        print("----------------------------\n")

        passed_guardrail = run_security_guardrail(post_content)
        if not passed_guardrail:
            print("🚨 Execution aborted. Generated content did not meet security specifications.")
            sys.exit(1)

        if os.environ.get("EXECUTE_PUBLISH", "false").lower() == "true":
            publish_to_linkedin(post_content)
        else:
            print("ℹ️ EXECUTE_PUBLISH flag set to false. Dry-run execution complete.")

    except Exception as e:
        print(f"❌ Pipeline Execution Failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()