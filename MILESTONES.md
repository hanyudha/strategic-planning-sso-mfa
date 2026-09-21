# Project Milestones

## Workflow Rule
Work on exactly one milestone at a time.

For every milestone:
1. Gather/produce the required evidence.
2. Analyze it.
3. Draft the milestone output.
4. Review inconsistencies and unsupported assumptions.
5. Lock the milestone.
6. Only then proceed.

Never silently rewrite a locked milestone because of a later idea. If a locked decision must change, record a change request and its rationale.

---

## M0 — Scope & Baseline Definition
**Status: LOCKED**

### Locked decisions
- Course: Perencanaan Stratejik
- Object: existing university SSO
- Existing condition: SSO operational, MFA not yet implemented
- Main focus: strategic development of existing SSO toward MFA integration
- Main framework: Ward & Peppard
- Main outputs: IS Strategy, IT Strategy, IS/IT Management Strategy, portfolio, roadmap
- Zero Trust: not the primary scope
- Greenfield SSO: out of scope
- Detailed MFA implementation: out of scope

---

## M1 — Organizational Context
**Status: LOCKED**

### Objectives
Establish factual organizational context before performing strategic analysis.

### Collect
- Organization profile
- Relevant business/service functions
- SSO users
- User categories
- Digital services using SSO
- Stakeholders
- Organizational ownership/management of SSO
- Relevant policies/SOPs
- Relevant strategic goals, if available

### Outputs
- Organizational Profile
- Stakeholder Map
- SSO Service Context
- Evidence Register
- Initial Problem Context

### Gate
Locked on 2026-09-21 as an organizational-context baseline. Open evidence gaps are documented in `M1_ORGANIZATIONAL_CONTEXT.md` and carried forward to later milestones where relevant.

---

## M2 — Current State SSO
**Status: LOCKED** (Locked on 2026-09-21)

### Collect
- SSO architecture
- Identity provider
- Authentication mechanism
- Directory/user source
- Integrated applications
- Authentication flow
- Account lifecycle
- Administrative roles
- Logging/auditing
- Existing security controls

### Outputs
- Current State Architecture
- Current State Inventory
- Authentication Flow
- Current State Findings

---

## M3 — Internal Business Environment
**Status: LOCKED** (Locked on 2026-09-21)

### Analyze
- Business/service processes affected by authentication
- User needs
- Stakeholder needs
- Organizational processes
- Security/service requirements
- Pain points

### Possible tools
- Value Chain
- Stakeholder Analysis
- Process Analysis

Use only methods that are justified by the available evidence.

---

## M4 — External Business Environment
**Status: LOCKED** (Locked on 2026-09-21)

### Analyze
- Regulatory context
- Security expectations
- Digital-service trends
- Remote access context
- External threats relevant to the business context
- Other environmental factors

### Possible tool
PESTEL, if sufficiently supported.

---

## M5 — Internal IS/IT Environment
**Status: LOCKED** (Locked on 2026-09-21)

### Analyze
- SSO technology
- Identity infrastructure
- Application integration
- Server/network components relevant to SSO
- Directory/database
- Monitoring/logging
- IT personnel and operational capability

---

## M6 — External IS/IT Environment
**Status: LOCKED** (Locked on 2026-09-21)

### Analyze
MFA technology landscape without selecting a product prematurely.

Potential technology families:
- TOTP
- Authenticator application
- Push authentication
- FIDO2
- Passkey
- Security key

Selection criteria must be derived from organizational requirements.

---

## M7 — SWOT & Strategic Issues
**Status: LOCKED** (Locked on 2026-09-21)

### Outputs
- SWOT
- Strategic alternatives where justified
- Strategic issues
- Prioritized strategic issues

MFA must emerge as a strategic response to the evidence, not as an unsupported predetermined conclusion.

---

## M8 — Gap Analysis
**Status: LOCKED** (Locked on 2026-09-21)

Compare:
- Current: SSO without MFA
- Target: SSO with appropriate MFA capability

Analyze gaps in:
- Technology
- Process
- Policy
- Governance
- People
- Monitoring
- User lifecycle
- Risk/control

---

## M9 — Strategy Formulation
**Status: LOCKED** (Locked on 2026-09-21)

Produce:
- IS Strategy
- IT Strategy
- IS/IT Management Strategy

Each strategy must trace back to identified gaps and strategic issues.

---

## M10 — Target Architecture
**Status: LOCKED** (Locked on 2026-09-21)

Produce a conceptual target architecture for SSO + MFA.

Do not over-specify products unless the analysis has justified them.

---

## M11 — Strategic Portfolio
**Status: LOCKED** (Locked on 2026-09-21)

Use McFarlan Strategic Grid or another justified portfolio approach.

Map existing and proposed applications/capabilities based on documented strategic/operational contribution.

---

## M12 — Strategic Initiatives & Roadmap
**Status: LOCKED** (Locked on 2026-09-21)

Produce:
- initiatives
- priorities
- dependencies
- sequencing
- timeline
- implementation phases
- risks

---

## M13 — KPI & Strategic Measurement
**Status: LOCKED** (Locked on 2026-09-21)

Produce measurable strategic indicators covering:
- MFA adoption
- authentication security
- user coverage
- service availability
- incidents
- governance/process compliance
- other evidence-supported outcomes

---

## M14 — Final Strategic Plan
**Status: LOCKED** (Locked on 2026-09-21)

Integrate all locked outputs into the final academic deliverable.
