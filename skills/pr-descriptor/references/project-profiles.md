# Project Profiles

Select profiles from the changed files, runtime behavior, and deployment path. Combine profiles for mixed changes. Do not classify only from the repository name.

Apply the claim provenance and operational wording rules in [evidence-model.md](evidence-model.md) to every selected profile.

## Contents

- Backend and API
- Frontend and web UI
- CI/CD, Jenkins, and scripts
- Infrastructure and platform
- Database and data
- Library and SDK
- Dependency and security
- Documentation and configuration
- Test-only, generated, and mechanical changes
- Mixed and large changes
- Cross-profile risk triggers

## Backend and API

Detect this profile from controllers, handlers, services, workers, domain logic, protocols, schemas, and server configuration.

Emphasize:

- Behavior and failure-mode changes
- Request, response, event, or data contract changes
- Authorization, authentication, concurrency, caching, and retry effects
- Backward compatibility and consumer impact
- Unit, integration, contract, and end-to-end validation actually performed

Add `Impact` for externally observable behavior or operational effects. Add `Migration` only when a public contract or consumer requires a coordinated one-time transition.

## Frontend and web UI

Detect this profile from components, pages, styles, client state, browser code, templates, and frontend build configuration.

Emphasize:

- User-visible behavior and interaction changes
- Loading, empty, error, disabled, and permission states
- Responsive behavior, browser coverage, accessibility, and localization
- API integration or client-state changes
- Automated UI tests and manual browser checks actually performed

Add `Screenshots` when visual evidence exists or repository policy requires it. Add `Impact` for navigation, accessibility, or behavior changes.

## CI/CD, Jenkins, and scripts

Detect this profile from `Jenkinsfile`, pipeline libraries, workflow files, shell scripts, build tooling, packaging, and deployment automation.

Emphasize:

- Trigger, stage, agent, condition, artifact, and environment changes
- Script inputs, outputs, exit behavior, idempotency, and failure handling
- Credential or secret identifiers without exposing values
- Differences between pull request, branch, scheduled, and release execution
- Linting, syntax checks, dry runs, sandbox runs, and observed pipeline results

Add `Impact` for pipeline or artifact changes. Add `Deployment and Rollback` when the automation changes a release or production path.

## Infrastructure and platform

Detect this profile from Terraform, CloudFormation, Kubernetes, Helm, networking, IAM, observability, runtime manifests, and platform configuration.

Emphasize:

- Resources created, changed, replaced, or deleted
- Environment scope and blast radius
- Identity, access, network, secret reference, capacity, cost, and availability effects
- Plan, diff, policy, manifest, or deployment validation actually performed
- Apply order, drift, state, rollback, and recovery considerations

Add `Impact` and `Deployment and Rollback` for material changes. Add `Migration` for state moves, resource replacement, or consumer transition.

## Database and data

Detect this profile from schemas, migrations, stored procedures, queries, models, ETL, analytics jobs, and backfills.

Emphasize:

- Schema and data-shape changes
- Read/write compatibility during rollout
- Locking, transaction, volume, duration, and backfill effects
- Data correctness, reconciliation, performance, and rollback evidence
- Retention, privacy, and access implications when relevant

Add `Migration` and `Deployment and Rollback` for executable schema or data changes. Add `Impact` for compatibility or runtime effects.

## Library and SDK

Detect this profile from exported APIs, packages, shared modules, plugins, client libraries, and extension points.

Emphasize:

- Public API and behavior changes
- Source, binary, configuration, and semantic compatibility
- Consumer examples or affected call sites
- Deprecation and upgrade paths
- Package, cross-version, and integration validation actually performed

Add `Migration` for breaking or deprecating changes. Add `Impact` for consumer-visible behavior.

## Dependency and security

Detect this profile from manifests, lockfiles, vendored code, authentication, authorization, input handling, encryption, and security tooling.

Emphasize:

- Dependency or control being changed and the reason
- Relevant vulnerability, compatibility, and transitive effects
- Runtime, bundle, build, license, and platform impact
- Security checks, dependency diffs, scans, and regression validation actually performed
- Remaining risk or intentionally deferred work

Do not copy exploit details, credentials, private tokens, or unnecessary sensitive values. Add `Impact` for security or runtime effects and `Migration` for required consumer changes.

## Documentation and configuration

Detect this profile from documentation, examples, feature flags, application settings, and non-executable configuration.

Emphasize:

- Intended reader, operator, or consuming component
- Behavior changed by the configuration
- Defaults, precedence, environment scope, and compatibility
- Link, build, lint, parse, or rendered-output validation actually performed

Keep documentation-only descriptions minimal. Add `Deployment and Rollback` when configuration changes runtime behavior or release coordination, but do not add `Migration` for an ordinary configuration edit without a one-time cutover or consumer action.

## Test-only, generated, and mechanical changes

Detect this profile from isolated test changes, generated artifacts, formatting, renames, and automated refactors.

Emphasize:

- Intended invariant or newly covered behavior
- Generator, command, or mechanical transformation used
- Whether runtime behavior is intended to remain unchanged
- Review boundaries between generated and hand-written files

Add `Review Guide` when generated output or broad mechanical changes would obscure the meaningful diff.

## Mixed and large changes

Detect this profile when a PR combines multiple runtime or operational concerns, spans three or more project facets, requires ordered rollout, or is visually dominated by vendored, minified, generated, renamed, or deleted files.

Require:

- `Impact` when the change crosses authentication, security, runtime behavior, external contracts, logging, dependencies, or infrastructure boundaries
- `Deployment and Rollback` when configuration, manifests, runtime dependencies, migrations, or operational paths change
- `Review Guide` when reviewers need an ordered path through the meaningful source changes or when bulk assets obscure the hand-written diff
- One validation entry or explicit unverified status for each material concern group

Keep `Changes` at the concern level. Put only the highest-signal review entry points in `Review Guide`; do not attach a repeated file inventory to each concern. Separate vendored or minified dependency replacements from hand-written security and behavior changes.

Include exact endpoints, environment identifiers, mount paths, or configuration values only when their literal correctness is a review target. Otherwise describe their purpose and direct reviewers to the relevant configuration entry point.

## Cross-profile risk triggers

Require or strengthen conditional sections when any trigger applies:

- Require `Impact` for user-visible behavior, public contracts, permissions, performance, cost, availability, security, or compatibility
- Require `Migration` for schema, state, data, public API, one-time configuration cutovers, or consumer transitions; a configuration file change alone does not trigger it
- Require `Deployment and Rollback` for ordered rollout, runtime configuration, infrastructure, data changes, artifact publication, feature flags, or recovery work
- Require `Screenshots` for visible UI changes with available visual evidence
- Require `Review Guide` for large diffs, mixed concerns, generated files, vendor updates, or sequence-sensitive review
- Include `Related Issues` only for links or identifiers present in the available context
