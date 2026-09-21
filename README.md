# Strategic Planning SSO + MFA

## Project
Perencanaan Stratejik — Strategic Information Systems / IS-IT Strategic Planning.

## Working Title
**Perencanaan Strategis Pengembangan Single Sign-On (SSO) Terintegrasi Multi-Factor Authentication (MFA) untuk Meningkatkan Keamanan Layanan Digital Perguruan Tinggi**

## Status
- Milestone M0 — Scope & Baseline Definition: **LOCKED**
- Milestone M1 — Organizational Context: **LOCKED**
- Next milestone: **M2 — Current State SSO**
- Workflow: one milestone at a time; review and lock before proceeding.

## Core Case
The case concerns an existing university SSO that is already operational but does not yet use MFA.

This is a **strategic planning** project, not a greenfield SSO implementation project.

## Primary Framework
Ward & Peppard strategic planning framework.

The reference material describes four environmental perspectives:
1. Internal Business Environment
2. External Business Environment
3. Internal IS/IT Environment
4. External IS/IT Environment

The expected strategic outputs are:
- IS Strategy
- IT Strategy
- IS/IT Management Strategy
- Application/capability portfolio
- Implementation roadmap

## Working Principle
Do not jump directly to technology selection. Establish:
Current State -> Analysis -> Strategic Issues -> Gap -> Strategy -> Target State -> Portfolio -> Roadmap -> KPI.

## Scope Fence
### In scope
- Existing SSO
- Authentication
- MFA
- Identity and access management directly related to SSO
- SSO-integrated applications
- Authentication security
- Relevant user lifecycle
- MFA technology landscape
- Governance, policy, management, architecture, roadmap and KPI

### Out of scope
- Full Zero Trust Architecture
- Full SOC/SIEM program
- General endpoint security
- General network security
- Disaster recovery as a standalone topic
- Building a new SSO from zero
- Detailed coding or implementation of MFA
- Product-specific configuration
- Full enterprise architecture of the university

### Future direction only
Zero Trust, passwordless authentication, adaptive/risk-based authentication, FIDO2/passkey may be discussed as future directions when supported by the analysis, but are not the main scope.

## Repository Rule
This repository is the source of truth for the academic assignment. Keep assumptions, evidence, decisions, and locked milestones explicit.
