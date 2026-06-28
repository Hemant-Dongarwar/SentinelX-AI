MITRE_DATABASE = {
    "T1059.001": {
        "name": "PowerShell",
        "tactic": "Execution",
        "risk_score": 9.5,
        "analysis": "Encoded PowerShell execution is commonly used by attackers to run malicious scripts while avoiding detection.",
        "recommendation": [
            "Inspect PowerShell command",
            "Check parent process",
            "Review Windows Event Logs",
            "Isolate host if suspicious"
        ]
    },

    "T1055": {
        "name": "Process Injection",
        "tactic": "Defense Evasion",
        "risk_score": 9.8,
        "analysis": "Process Injection allows malware to hide inside legitimate processes.",
        "recommendation": [
            "Inspect injected process",
            "Capture memory dump",
            "Run EDR scan"
        ]
    }
}


def analyze_alert(mitre_id: str):

    return MITRE_DATABASE.get(
        mitre_id,
        {
            "name": "Unknown",
            "tactic": "Unknown",
            "risk_score": 5,
            "analysis": "Unknown MITRE Technique",
            "recommendation": [
                "Manual Investigation Required"
            ]
        }
    )