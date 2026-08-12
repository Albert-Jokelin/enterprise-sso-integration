# Implementation Plan: Enterprise SSO Integration

## Overview
Prove you can pass an enterprise security review: standards-based auth (OAuth2, SAML), automated user lifecycle (SCIM), and role enforcement across tenants.

## Phase 1 — Happy Path
- `oauth2/`: implement the Authorization Code flow against a real IdP (Auth0/Okta/Keycloak dev tenant) — login redirect, callback, token exchange, `/me` endpoint.
- `rbac/`: define a `Role` enum and a `require_role()` FastAPI dependency; protect one endpoint per role.
- Ship: a user can log in via OAuth2 and hit a role-protected endpoint.

## Phase 2 — Hardening
- `saml/`: add SP-initiated SAML login (python3-saml or similar) for IdPs that don't support OAuth2 — map SAML assertions to the same internal user/role model as OAuth2.
- `scim/`: implement SCIM 2.0 `/Users` and `/Groups` endpoints (GET/POST/PATCH/DELETE) so an IdP can auto-provision/deprovision users; write the mapping from SCIM group membership to internal roles.
- `oauth2/`: validate and cache JWKS, handle token refresh and expiry correctly.
- Add audit logging for every login, role change, and SCIM operation.

## Phase 3 — Production-Grade
- `rbac/`: support role scoping *per tenant* (a user can be admin in tenant A, viewer in tenant B) — tie into the multi-tenant project's `TenantContext` if reused.
- `scim/`: handle bulk operations and partial-failure semantics per the SCIM spec; add idempotency for retried provisioning calls.
- Add a security regression test: token replay, expired token, tampered JWT, SCIM request without proper bearer token — all must fail closed.
- Document threat model and mitigations (this artifact is often what an enterprise security reviewer actually reads).

## Testing & Deployment
- Mock the IdP in tests (e.g. a fake JWKS + signed test tokens) so `uv run pytest` doesn't depend on a live IdP.
- Add `.env.example` documenting required IdP client id/secret/issuer — never commit real secrets.
