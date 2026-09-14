Case A

Recommend Birch provisionally: it is the only confirmed eligible vendor. On-premises deployment is mandatory, so price ranks vendors only after eligibility is established.

| Vendor | Price | Status | Evidence and implication |
|---|---:|---|---|
| Aster | 10 | Ineligible | Documentation explicitly says cloud-only, conflicting with the mandatory on-premises requirement. |
| Birch | 20 | Eligible | Technical documentation confirms on-premises support. |
| Cedar | 8 | Pending | Deployment documentation is absent; on-premises support is unknown. |

The unresolved question is whether Cedar supports on-premises deployment. No further sources are available, so this cannot be resolved from the supplied evidence. If support were confirmed, Cedar would become eligible and its lower price would make it the preferred option. Missing documentation does not establish incompatibility.

Case B

Recommend Cedar at 8. Price is the highest priority, its price is confirmed, and deployment is a preference rather than an eligibility requirement. Cloud-only deployment is acceptable.

| Price rank | Vendor | Price | Status | Deployment evidence and tradeoff |
|---|---|---:|---|---|
| 1 | Cedar | 8 | Eligible | Deployment is unknown; the on-premises preference cannot be confirmed. |
| 2 | Aster | 10 | Eligible | Documented cloud-only deployment does not satisfy the on-premises preference but is acceptable. |
| 3 | Birch | 20 | Eligible | Documented on-premises support satisfies the preference at the highest price. |

All three are eligible under the stated requirements. Cedar's deployment uncertainty remains material to the deployment preference, but does not change the recommendation when minimizing price is the highest priority and cloud-only is acceptable. No further sources are available to establish Cedar's deployment options.

Case C

Recommend Aster. Both vendors are confirmed eligible, and Aster is cheaper.

| Vendor | Price | Status | Evidence |
|---|---:|---|---|
| Aster | 10 | Eligible | Documented on-premises support meets the mandatory requirement. |
| Birch | 20 | Eligible | Documented on-premises support meets the mandatory requirement. |

Aster costs 10 less than Birch. There is no unresolved deployment question in the supplied facts affecting this recommendation.

Case D

[
  {
    "vendor": "Aster",
    "status": "ineligible",
    "reason": "On-premises deployment is mandatory, but documentation explicitly says cloud-only. Its price of 10 does not overcome this incompatibility."
  },
  {
    "vendor": "Birch",
    "status": "eligible",
    "reason": "Technical documentation confirms the mandatory on-premises support. At 20, Birch is the only confirmed eligible vendor and the provisional recommendation; Cedar could become preferred if its on-premises support were established."
  },
  {
    "vendor": "Cedar",
    "status": "pending",
    "reason": "Deployment documentation is absent, so mandatory on-premises support is unknown. No further sources are available to resolve it. At 8, Cedar would become the preferred eligible option if support were confirmed."
  }
]
