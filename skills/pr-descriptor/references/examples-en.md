# English PR Examples

Use these fictional examples to calibrate structure and tone. Do not copy their facts or validation results into a real PR.

## Contents

- Backend/API
- Frontend/Web
- CI/CD/Jenkins
- Infrastructure/IaC
- Database/Migration
- Library/Dependency
- Mixed/Security and Operations

## Backend/API

Evidence: Fetching an order without a selected shipping address returns `500`; unit and API integration tests pass after the fix.

```markdown
Title: Fix order lookup when no shipping address is selected

## Summary

Fixed the `500` response returned when an order has no selected shipping address. The response mapper now returns order details regardless of whether optional shipping data is present.

## Changes

- Add null-safe mapping for the selected shipping address
- Add response coverage for orders without shipping data
- Preserve the existing error response for invalid order IDs

## Validation

- `./gradlew test`
- API integration test confirming a `200` response without shipping data

## Impact

- Remove the error response seen by API consumers for orders without shipping data
```

## Frontend/Web

Evidence: The search results page adds an empty state and keyboard focus styling; component tests and a manual Chrome check were completed.

```markdown
Title: Improve search empty states and keyboard navigation

## Summary

Added an actionable empty state when a search returns no results. Improved focus styling so keyboard users can identify the active result card.

## Changes

- Show guidance and a filter reset action when no results are available
- Apply `:focus-visible` styling to result cards
- Add component coverage for empty states and keyboard navigation

## Validation

- `npm test -- SearchResults`
- Manual: verified keyboard navigation and filter reset in Chrome

## Impact

- Provide a recovery path for searches with no results
- Improve focus visibility during keyboard navigation

## Screenshots

- Search empty state attached
- Result card keyboard focus state attached
```

## CI/CD/Jenkins

Evidence: The `Jenkinsfile` and deployment shell script changed so production deployment runs only on release branches. `shellcheck` and Jenkins Replay passed, but no official deployment or rollback procedure was supplied.

```markdown
Title: Restrict production deployment to release branches

## Summary

Restricted the production deployment stage to release branches. Pull request and regular branch builds now bypass the production deployment script.

## Changes

- Add a release branch condition to the production deployment stage
- Validate required arguments in the deployment shell script
- Log when the deployment stage is skipped by branch policy

## Validation

- `shellcheck scripts/deploy.sh`
- Jenkins Replay confirming deployment is skipped for pull request builds
- Jenkins Replay confirming deployment is entered for a release branch

## Impact

- Limit production deployment triggers to release branches

## Deployment and Rollback

- Recommended deployment: apply through the shared pipeline revision and verify the condition in the next release build
- Recommended rollback: restore the previous pipeline revision if the condition misbehaves
```

## Infrastructure/IaC

Evidence: Terraform changes move application subnets to a dedicated NAT gateway; formatting, validation, and the staging plan pass. Production has not been applied, and no official rollback procedure was confirmed.

```markdown
Title: Isolate application subnet traffic through a dedicated NAT gateway

## Summary

Moved application subnet egress to a dedicated NAT gateway. This reduces the blast radius of failures in the shared gateway and allows the application network path to be managed independently.

## Changes

- Add a dedicated NAT gateway and route for application subnets
- Remove references to the shared gateway route
- Add monitoring for gateway health and error rate

## Validation

- `terraform fmt -check`
- `terraform validate`
- Staging `terraform plan` confirming gateway creation and route replacement
- Production apply not run

## Impact

- Change outbound routing for application subnets
- Increase infrastructure cost through an additional NAT gateway

## Deployment and Rollback

- Recommended deployment: create the gateway, switch routes, and verify outbound connectivity
- Recommended rollback: restore the shared gateway route before removing the new gateway
```

## Database/Migration

Evidence: A nullable column is added first, followed by the application deployment and a backfill; migration tests and a staging backfill completed successfully.

```markdown
Title: Add order channel tracking with a staged backfill

## Summary

Added `order_channel` to identify the path used to create each order. The rollout preserves compatibility by adding a nullable column before deploying writers and backfilling existing rows.

## Changes

- Add nullable `orders.order_channel`
- Record the channel for newly created orders
- Add a batch backfill for existing orders

## Validation

- Migration test passed
- Staging backfill reconciled across 100,000 rows

## Impact

- Slightly increase order storage and batch processing time

## Migration

- Step 1: add the nullable column
- Step 2: deploy application writers
- Step 3: backfill existing data
- Step 4: verify missing values before considering a constraint

## Deployment and Rollback

- Confirmed deployment: apply schema, application, and backfill changes in order
- Recommended rollback: stop new column usage before stopping the backfill
```

## Library/Dependency

Evidence: HTTP retry parameters move into a configuration object while the old overload remains deprecated; the supported runtime matrix passes.

```markdown
Title: Consolidate HTTP client retry configuration

## Summary

Consolidated retry parameters into a `RetryPolicy` configuration object. Existing overloads remain available for compatibility while new consumers gain a single retry configuration path.

## Changes

- Add the public `RetryPolicy` configuration object
- Deprecate the existing retry overload
- Add a compatibility adapter from legacy parameters
- Update consumer examples and API documentation

## Validation

- `./gradlew test`
- Supported JDK compatibility matrix passed

## Impact

- Preserve behavior for existing consumers
- Change the preferred retry configuration for new consumers

## Migration

- Keep the existing overload until the next major release
- Recommend `RetryPolicy` for new integrations
```

## Mixed/Security and Operations

Evidence: A large web application PR replaces LDAP with SSO, adds structured file logging and a Kubernetes mount, and upgrades vulnerable browser dependencies. Manual SSO validation reached the final application landing, but no runtime logging or UI regression evidence is available. Rollback can restore the previous application artifact and manifest, and a security issue and paired PR were supplied.

```markdown
Title: Adopt SSO and strengthen operational logging and browser dependency security

## Summary

Replaced LDAP authentication with SSO to meet the current security requirements and structured the operational logging path. Upgraded vulnerable browser dependencies and adjusted related output handling so the authentication and web security changes can ship together.

## Changes

### Authentication

- Route unauthenticated requests through the SSO flow
- Create the application session from the callback response
- Re-enter SSO authentication after logout

### Logging and Platform

- Move application logging to structured file output
- Add request context to MDC
- Add the manifest and runtime option for pod-specific log paths

### Dependency Security

- Upgrade vulnerable jQuery and jQuery UI versions
- Adjust JSP output handling for the updated browser dependencies

## Validation

- Authentication — Manual: verified callback handling, session creation, and final application landing
- Logging and Platform — Not verified from the available evidence: pod file creation and rotation
- Dependency Security — Not verified from the available evidence: UI regression and DAST rerun

## Impact

- Change the user authentication entry point and session creation flow
- Change the operational log format and pod-specific storage path
- Introduce possible compatibility effects across screens using the shared browser dependencies

## Deployment and Rollback

- Recommended deployment: release the manifest and application artifact together, then verify the SSO callback and pod log creation in order
- Confirmed rollback: restore the previous application artifact and manifest

## Review Guide

1. Review the authentication interceptor and callback session handling
2. Review the logging configuration and request context injection
3. Review manifest volume and runtime option changes
4. Review hand-written JSP changes before vendored and minified dependency files

## Related Issues

- SAFE-0000
- Paired PR: `example/service#100`
```
