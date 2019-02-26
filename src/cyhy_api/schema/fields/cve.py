import graphene


class Severity(graphene.Enum):
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class CVEField(graphene.ObjectType):
    id = graphene.String(
        required=True,
        description="The CVE ID assigned to this vulnerability or exposure.",
    )
    cvss_score = graphene.Float(
        required=True,
        description="The CVSS (Common Vulnerability Scoring System) score"
        " generated for this CVE.",
    )
    severity = Severity(
        description="The severity of the CVE calculated from the CVSS score."
    )

    class Meta:
        description = (
            "A CVE (Common Vulnerability and Exposures) is common"
            " identifier for publicly known cybersecurity vulnerabilities."
        )
