rule Suspicious_Domain
{
    strings:
        $evil = "evil.com"
        $malware = "malware-domain.net"

    condition:
        any of them
}
