---
name: provision-account
description: Provision or invite a user account in a specified environment and tenant. Use for creating demo, internal-testing or customer accounts, checking tenant access, or resending an initial invitation. Reuse the project's verified provisioning tool and runbook; verify identity-provider membership and application role before emailing access instructions.
argument-hint: "<email> [environment] [tenant] [role]"
---

# Provision Account

Create usable access, not just an identity-provider account. Reuse existing tooling; do not build a provisioning script or change application code.

## Resolve the request

- Resolve repository, environment, tenant, exact email and intended role from the request and conversation. Ask only for unresolved decisions that change access; never infer tenant from an email domain or website hostname.
- Read repository guidance and the project-local account/invitation runbook before running commands. For Kubera, read `~/.omp/agent/kubera.md` and follow its verified Cloud Commander/Cognito/SES recipe. Keep AWS coordinates, credentials and company-specific commands there, not in this skill.
- Provision only when explicitly requested. A question about account access is read-only. Creating an account does not authorize changing another account's tenant, elevating an existing role, resetting a password or granting unrelated access.
- Use the documented internal-testing role default only for explicitly requested internal test accounts. Customer roles require their intended least-privilege access; never apply an internal super-admin default to customers.

## 1. Inspect first

1. Verify the intended cloud profile/account and discover the environment's identity pool using the runbook. Do not fall back to another profile or environment after an authentication failure.
2. Look up the exact email in the identity provider. Inspect any existing identity's enabled/status fields, tenant memberships and application user/role.
3. List the target tenant's roles and confirm the intended role exists.

If the identity already has the intended access, do not recreate it. If it belongs to a different tenant, do not move it or add another tenant group by inference: use a separately requested email alias. Some systems select the first group, so multiple tenant memberships may be ambiguous.

## 2. Provision once

- Use the existing project command that creates the identity, tenant membership and application user with the intended role. An identity-provider account alone is incomplete.
- Create only if absent. If the command fails partway, inspect which pieces exist and repair only the missing pieces through supported tooling and authorized access; do not blindly rerun creation. Stop for permission if repair would change existing access or credentials.
- Capture command stdout/stderr privately when it can contain temporary passwords or secrets. Report only sanitized status; never print credentials, paste them in chat, or save them to skill files.
- A successful creation exit code is not verification. Read back the enabled account, exact tenant membership and application database user/role. Verify identity linkage where the tooling exposes it.
- If any access check fails, do not send an invitation claiming the account is ready.

## 3. Invite after verification

- Follow the runbook's invitation mechanism. Kubera's Cloud Commander suppresses the invitation; Cognito `RESEND` sends it and replaces the initially generated temporary password.
- For a newly created account, send its initial invitation after verification. For an existing account, resend only when requested and its status permits an initial invitation, such as `FORCE_CHANGE_PASSWORD`; do not reset a confirmed user's password.
- Send the environment/tenant sign-in URL separately if the provider's invitation omits it. Include the exact username and first-login password-change requirement, not the password.
- Observe the invitation/email command results. Provider acceptance proves the send was accepted, not inbox delivery or a successful first login. If sending fails, report the verified account state and exact invitation blocker; do not recreate the account.

## Deliver

Return at most three short bullets:

- Account email, environment, tenant and verified role.
- Sign-in URL, invitation acceptance and required first-login action; state that inbox delivery is unconfirmed unless independently observed.
- Any blocker and whether existing accounts were changed.

Do not perform another real account creation merely to test this skill. Verify the skill's installation/loading without mutations; verify each requested account through the live identity and application access checks above.
