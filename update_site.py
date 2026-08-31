import os
import subprocess
from pathlib import Path

def update_gvf_website():
    repo_dir = Path.cwd()
    print(f"[GVF SITE AUTOMATION] Working in repository: {repo_dir}")

    # 1. Define index.html Footer
    footer_html = """
<!-- GVF DYNAMICS FOOTER -->
<footer style="background-color: #030712; color: #94a3b8; padding: 40px 20px; border-top: 1px solid #1e293b; font-family: sans-serif; text-align: center;">
  <div style="max-width: 1100px; margin: 0 auto;">
    <div style="margin-bottom: 20px; display: flex; justify-content: center; gap: 24px; flex-wrap: wrap; font-size: 15px;">
      <a href="https://gvfdynamics.com/privacy.html" style="color: #38bdf8; text-decoration: none; font-weight: 500;">Privacy Policy</a>
      <a href="https://gvfdynamics.com/terms.html" style="color: #38bdf8; text-decoration: none; font-weight: 500;">Terms of Service</a>
      <a href="https://github.com/GVF-Dynamics-LLC/GVF-Engine-Sim" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 500;">GitHub Open Core</a>
      <a href="https://polar.sh/gvfdynamics" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 500;">Enterprise SDK (Polar)</a>
      <a href="https://www.youtube.com/@GVFDynamics" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 500;">YouTube Channel</a>
    </div>
    <p style="font-size: 14px; color: #64748b; margin: 0;">
      © 2026 GVF Dynamics LLC. All rights reserved. | Hardware-Enforced AI Governance Microarchitecture
    </p>
  </div>
</footer>
</body>
"""

    # 2. Update index.html
    index_path = repo_dir / "index.html"
    if index_path.exists():
        content = index_path.read_text(encoding="utf-8")
        if "<!-- GVF DYNAMICS FOOTER -->" not in content:
            if "</body>" in content:
                content = content.replace("</body>", footer_html)
            else:
                content += footer_html
            index_path.write_text(content, encoding="utf-8")
            print("[SUCCESS] Appended footer links to index.html")
        else:
            print("[NOTICE] Footer links already exist in index.html")

    # 3. Create/Update terms.html
    terms_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Terms of Service - GVF Dynamics LLC</title>
  <style>
    body { background-color: #030712; color: #f8fafc; font-family: sans-serif; line-height: 1.6; padding: 40px 20px; max-width: 800px; margin: 0 auto; }
    h1 { color: #38bdf8; }
    h2 { color: #94a3b8; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }
    a { color: #38bdf8; text-decoration: none; }
  </style>
</head>
<body>
  <h1>Terms of Service</h1>
  <p><strong>Effective Date:</strong> August 31, 2026</p>

  <h2>1. Overview</h2>
  <p>Welcome to GVF Dynamics LLC ("GVF Dynamics", "we", "us"). By accessing <a href="https://gvfdynamics.com">gvfdynamics.com</a>, using our open-source simulation tools, or licensing our SDKs, you agree to these Terms of Service.</p>

  <h2>2. Intellectual Property</h2>
  <p>All proprietary hardware architectures, microarchitecture designs, trademarks, and documentation belong exclusively to GVF Dynamics LLC. Open-source evaluation repositories are made available under their respective open-source licenses.</p>

  <h2>3. Commercial Licensing</h2>
  <p>Commercial deployment, hardware integration, or enterprise SDK access requires a valid license tier issued via our official storefront at <a href="https://polar.sh/gvfdynamics" target="_blank">polar.sh/gvfdynamics</a>.</p>

  <h2>4. Contact</h2>
  <p>For inquiries regarding licensing or terms, please contact us via our official support channels at <a href="https://gvfdynamics.com">gvfdynamics.com</a>.</p>
</body>
</html>
"""
    terms_path = repo_dir / "terms.html"
    terms_path.write_text(terms_html, encoding="utf-8")
    print("[SUCCESS] Created terms.html")

    # 4. Create/Update privacy.html
    privacy_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy Policy - GVF Dynamics LLC</title>
  <style>
    body { background-color: #030712; color: #f8fafc; font-family: sans-serif; line-height: 1.6; padding: 40px 20px; max-width: 800px; margin: 0 auto; }
    h1 { color: #38bdf8; }
    h2 { color: #94a3b8; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }
    a { color: #38bdf8; text-decoration: none; }
  </style>
</head>
<body>
  <h1>Privacy Policy</h1>
  <p><strong>Effective Date:</strong> August 31, 2026</p>

  <h2>1. Data Collection</h2>
  <p>GVF Dynamics LLC collects basic analytical data when you visit <a href="https://gvfdynamics.com">gvfdynamics.com</a> or interact with our SDK portals.</p>

  <h2>2. Third-Party Services</h2>
  <p>License management and payment processing are securely handled by Polar (<a href="https://polar.sh/gvfdynamics" target="_blank">polar.sh</a>).</p>

  <h2>3. Contact</h2>
  <p>For privacy inquiries, reach us directly via <a href="https://gvfdynamics.com">gvfdynamics.com</a>.</p>
</body>
</html>
"""
    privacy_path = repo_dir / "privacy.html"
    privacy_path.write_text(privacy_html, encoding="utf-8")
    print("[SUCCESS] Updated privacy.html")

    # 5. Execute Git Commands Automatically
    print("\n[GIT AUTOMATION] Staging, committing, and pushing to GitHub Pages...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "feat: update site footer links, terms.html, and privacy.html"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("\n[LIVE DEPLOYMENT SUCCESS] Your website changes have been pushed to GitHub Pages!")
    except subprocess.CalledProcessError as e:
        print(f"[GIT ERROR] Failed to push changes: {e}")

if __name__ == "__main__":
    update_gvf_website()