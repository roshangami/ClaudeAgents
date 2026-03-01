"""
CVE Researcher Agent
----------------------------------
Give it a technology/library name and it searches the web for
recent CVEs, explains them, and tells you if your version is affected.
WebSearch tool 

Setup:
  pip install claude-agent-sdk
  export ANTHROPIC_API_KEY="your-key-here"

Run:
  python project4_cve_researcher.py
  
You'll be prompted to enter a technology and version.
"""

import asyncio
from claude_agent_sdk import ClaudeAgentOptions, query, TextBlock, AssistantMessage, ResultMessage


async def research_cves(technology: str, version: str = ""):
    print(f"\n🔎 CVE Research: {technology} {version}")
    print("=" * 60)

    print("🤖 Agent is searching the web for CVEs...\n")

    claud_agent_options = ClaudeAgentOptions(
        allowed_tools=["WebSearch"],
        tools=["WebSearch"],
        system_prompt="""
        You are a vulnerability researcher and threat intelligence analyst.
        You search for CVEs and security advisories and explain them clearly to security engineers.

        When researching CVEs:
        - Search NVD (nvd.nist.gov), CVE.org, and vendor advisories
        - Always include CVE IDs, CVSS scores, and affected versions
        - Explain attack vectors in plain English
        - Assess exploitability (is there a public PoC? Is it being exploited in the wild?)
        - Give clear, actionable remediation advice
        - Flag if the vulnerability is critical enough to warrant emergency patching

        Be thorough but concise. Security engineers are busy people.
        """,
        model="claude-haiku-4-5-20251001",
        permission_mode="acceptEdits"
    )

    version_context = version if version else "(any recent version)"

    prompt = f"""
    Please research recent CVEs and security vulnerabilities for:

    Technology: {technology}
    Version: {version_context}

    Steps:
    1. Search for recent CVEs affecting {technology} {version}
    2. Search for any active exploits or PoCs in the wild
    3. Check for security advisories from the vendor/maintainer
    4. Search for any patches or mitigations available

    Then produce a report with:

    ## CVE Research Report: {technology} {version}
    **Research Date:** Today

    ## Critical/High CVEs (Patch Immediately)
    For each:
    - CVE ID + link
    - CVSS Score + Vector
    - Affected Versions (is {version} affected? YES/NO)
    - What can an attacker do?
    - Is there a public exploit? (YES/NO/PoC available)
    - Fix: patch version or mitigation

    ## Medium CVEs (Patch in Next Cycle)
    (same format, brief)

    ## Low/Informational
    (brief summary only)

    ## Verdict for {technology} {version}
    - Overall risk level: CRITICAL / HIGH / MEDIUM / LOW
    - Recommended action: PATCH NOW / PATCH SOON / MONITOR / OK
    - Specific patch/upgrade recommendation

    ## Useful Links
    (NVD page, vendor advisory, changelog)
    
    """

    async for message in query(prompt=prompt, options=claud_agent_options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end=" ", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"\n\n✅ CVE Research Complete!")
            if message.usage:
                cost = message.usage.get("total_cost_usd", 0)
                print(f"💰 Cost: ${cost:.4f}")


def main():
    print("🔎 CVE Researcher Agent")
    print("=" * 60)

    technology = input("Enter technology/library name (e.g. Django, OpenSSL, Log4J): ").split()
    if not technology:
        print("❌ No technology entered.")
        return 
    
    version = input("Enter version (Optional, press Enter to skip): ").strip()

    asyncio.run(research_cves(technology, version))


if __name__ == "__main__":
    main()
