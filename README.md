<div align="center">

# 📚 cortex-xdr-client

**Typed Python client for the Cortex XDR API · alerts · endpoints · incidents · scripts · XQL**

Glovo's fork of [`ebarti/cortex-xdr-client`](https://github.com/ebarti/cortex-xdr-client): a small,
synchronous wrapper that signs each request with a Cortex XDR API key and parses the reply into
pydantic models. It is not a service or a CLI, this fork isn't published to PyPI, and it covers
only the calls listed under [Supported Cortex XDR APIs](#supported-cortex-xdr-apis), not the whole
Cortex API.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![Poetry](https://img.shields.io/badge/Poetry-poetry--core-60A5FA?logo=poetry&logoColor=white)](pyproject.toml)
[![requests](https://img.shields.io/badge/requests-2.x-blue)](pyproject.toml)
[![pydantic](https://img.shields.io/badge/pydantic-1.x-E92063?logo=pydantic&logoColor=white)](pyproject.toml)
<br/>
[![Version](https://img.shields.io/badge/version-2.0.4-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Test files](https://img.shields.io/badge/test_files-1-informational)](tests)
[![Fork of](https://img.shields.io/badge/fork_of-ebarti%2Fcortex--xdr--client-lightgrey?logo=github)](https://github.com/ebarti/cortex-xdr-client)

</div>

---

## Table of contents

- [Overview](#overview)
- [Build & local development](#build--local-development)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Security & data handling](#security--data-handling)
- [Repository layout](#repository-layout)
- [Contributing & conventions](#contributing--conventions)
- [Glossary](#glossary)
- [Ownership & support](#ownership--support)

---

## Overview

A Python client for the [Cortex XDR API](https://cortex-panw.stoplight.io/docs/cortex-xdr/axpm6b98x4p18-cortex-xdr-api-overview).
You build an [`Authentication`](cortex_xdr_client/api/authentication.py) from an API key and its ID,
pass it with your tenant **FQDN** to [`CortexXDRClient`](cortex_xdr_client/client.py), and call
methods on one attribute per API group (`client.alerts_api`, `client.endpoints_api`, …).

Each method POSTs to `https://api-<fqdn>/public_api/v1/<group>/<call>` (`v2` for `get_alerts_v2`),
([`base_api.py`](cortex_xdr_client/api/base_api.py)), with a default timeout of `(10, 60)` seconds
set in [`client.py`](cortex_xdr_client/client.py).
A non-2xx reply raises `requests.HTTPError`. On success most methods return a pydantic model
from [`api/models/`](cortex_xdr_client/api/models); XQL calls return a `dict` and `download_file`
returns raw bytes.

> [!WARNING]
> **PyPI's `cortex-xdr-client` is upstream's package, not this fork.** None of this fork's tags
> (`v1.9.0`, `v2.0.0`–`v2.0.4`) were published there. PyPI's 2.0.0 was uploaded on 2026-09-29 from
> upstream's own `v2.0.0` tag, which is a different commit. To get this fork's code, pin a git tag
> (see [Use it from another project](#use-it-from-another-project)).

| | |
|---|---|
| **Language / build** | Python `^3.9` · Poetry ([`pyproject.toml`](pyproject.toml)) |
| **HTTP** | `requests` `^2.26.0`, synchronous |
| **Models** | `pydantic` `^1.8.2` (v1 API, `parse_obj`) |
| **Version** | `2.0.4` in [`pyproject.toml`](pyproject.toml); latest tag `v2.0.4` |
| **Upstream** | [`ebarti/cortex-xdr-client`](https://github.com/ebarti/cortex-xdr-client) |
| **Fork additions** | Audits API (PR #1), `get_alerts_v2` (PR #2), type-hint fixes for older Python versions |
| **Used by** | `Glovo/logharvester` and `Glovo/overwatch-soar` pin git tag `v2.0.4`. `Glovo/overwatch` and `Glovo/cyber-defense-automations` depend on PyPI `^1.8.7`, which is upstream's package |

### Supported Cortex XDR APIs

These are the Cortex XDR **Prevent & Pro** APIs the client supports. Each method name links to the
Cortex docs for that call. ✦ marks calls this fork added.

| API group · attribute | Method | Cortex call |
|---|---|---|
| Alerts · `alerts_api` | [`get_alerts`](https://cortex-panw.stoplight.io/docs/cortex-xdr/813e387002342-get-all-alerts) | `alerts/get_alerts_multi_events` (v1) |
| | [`get_alerts_v2`](https://cortex-panw.stoplight.io/docs/cortex-xdr/a9873334620ed-get-alerts-multi-events-v2) ✦ | `alerts/get_alerts_multi_events` (v2), with sort |
| Audits · `audits_api` | [`get_audit_management_logs`](https://cortex-panw.stoplight.io/docs/cortex-xdr/091d0d8b7d283-get-audit-management-log) ✦ | `audits/management_logs` |
| Downloads · `download_api` | [`download_file`](https://cortex-panw.stoplight.io/docs/cortex-xdr/2932f29d2ccdd-file-retrieval-details) | `download/<file_api_value>` |
| Endpoints · `endpoints_api` | [`get_all_endpoints`](https://cortex-panw.stoplight.io/docs/cortex-xdr/89535019b740f-get-all-endpoints) | `endpoints/get_endpoints` |
| | [`get_endpoint`](https://cortex-panw.stoplight.io/docs/cortex-xdr/b149d40bd4c51-get-endpoint) | `endpoints/get_endpoint` |
| | [`isolate_endpoints`](https://cortex-panw.stoplight.io/docs/cortex-xdr/9c730a966cdd8-isolate-endpoints) | `endpoints/isolate` |
| | [`unisolate_endpoints`](https://cortex-panw.stoplight.io/docs/cortex-xdr/c719336adb46b-unisolate-endpoints) | `endpoints/unisolate` |
| | [`scan_endpoints`](https://cortex-panw.stoplight.io/docs/cortex-xdr/2e666ee0be1c6-scan-endpoints) · `scan_all_endpoints` | `endpoints/scan` |
| | [`set_endpoint_alias`](https://cortex-panw.stoplight.io/docs/cortex-xdr/c1ff89fa71c74-set-an-endpoint-alias) | `endpoints/update_agent_name` |
| | [`retrieve_file`](https://cortex-panw.stoplight.io/docs/cortex-xdr/08b1ba9fcfae0-retrieve-file) | `endpoints/file_retrieval` |
| | [`quarantine_file`](https://cortex-panw.stoplight.io/docs/cortex-xdr/76e8cca7fcb2e-quarantine-files) | `endpoints/quarantine` |
| Incidents · `incidents_api` | [`get_incidents`](https://cortex-panw.stoplight.io/docs/cortex-xdr/a61eadc13dd54-get-all-incidents) | `incidents/get_incidents` |
| | [`get_incident_extra_data`](https://cortex-panw.stoplight.io/docs/cortex-xdr/5a2fff98016d5-get-extra-incident-data) | `incidents/get_incident_extra_data` |
| Indicators · `ioc_api` | [`insert_json`](https://cortex-panw.stoplight.io/docs/cortex-xdr/24e778d89726d-insert-simple-indicators-json) | `indicators/insert_jsons` |
| Response actions · `actions_api` | [`get_action_status`](https://cortex-panw.stoplight.io/docs/cortex-xdr/9782594f400c3-get-action-status) | `actions/get_action_status` |
| | [`get_file_retrieval_details`](https://docs-cortex.paloaltonetworks.com/r/Cortex-XDR/Cortex-XDR-API-Reference/File-Retrieval-Details) | `actions/file_retrieval_details` |
| Scripts · `scripts_api` | [`get_scripts`](https://cortex-panw.stoplight.io/docs/cortex-xdr/6c41fe0732805-get-scripts) | `scripts/get_scripts` |
| | [`get_script_metadata`](https://cortex-panw.stoplight.io/docs/cortex-xdr/52ea90b5f5c72-get-script-metadata) | `scripts/get_script_metadata` |
| | [`get_script_execution_status`](https://cortex-panw.stoplight.io/docs/cortex-xdr/28073c365903b-get-script-execution-status) | `scripts/get_script_execution_status` |
| | [`get_script_execution_results`](https://cortex-panw.stoplight.io/docs/cortex-xdr/fa2ca3b1ff49b-get-script-execution-results) | `scripts/get_script_execution_results` |
| | [`get_script_execution_result_files`](https://cortex-panw.stoplight.io/docs/cortex-xdr/0fb66ea9988ff-get-script-execution-result-files) | `scripts/get_script_execution_results_files` |
| | [`run_script`](https://cortex-panw.stoplight.io/docs/cortex-xdr/7223bea7d2bea-run-script) | `scripts/run_script` |
| | [`run_snippet_code_script`](https://cortex-panw.stoplight.io/docs/cortex-xdr/083859c8c6729-run-snippet-code-script) | `scripts/run_snippet_code_script` |
| XQL · `xql_api` | [`start_xql_query`](https://cortex-panw.stoplight.io/docs/cortex-xdr/ecc87ad01e173-start-an-xql-query) | `xql/start_xql_query` |
| | [`get_query_results`](https://cortex-panw.stoplight.io/docs/cortex-xdr/be3d47e8dce5a-get-xql-query-results) | `xql/get_query_results` |
| | [`get_query_results_stream`](https://cortex-panw.stoplight.io/docs/cortex-xdr/155abd6ca4b4d-get-xql-query-results-stream) | `xql/get_query_results_stream` (gzip) |

**`get_query_results`** returns the results inline when there are at most 1,000. Above that it
follows the `stream_id` and calls `get_query_results_stream` itself. It raises
`UnsuccessfulQueryStatusException` unless the query status is `SUCCESS`, and
`InvalidResponseException` when the reply lacks an expected key
([`exceptions.py`](cortex_xdr_client/api/models/exceptions.py)).

---

## Build & local development

> [!NOTE]
> **Prerequisites:** Python 3.9 or newer ([`pyproject.toml`](pyproject.toml) requires `^3.9`) and
> [Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer).
> No Cortex tenant or API key is needed to build or test.

```bash
git clone https://github.com/Glovo/cortex-xdr-client.git
cd cortex-xdr-client
poetry install                               # virtualenv with runtime + dev dependencies
poetry run python -m pytest tests/           # run the tests
poetry build                                 # sdist + wheel into dist/ (git-ignored)
```

### Use it from another project

Pin a tag of this repo, as `Glovo/logharvester` and `Glovo/overwatch-soar` do:

```toml
[tool.poetry.dependencies]
cortex-xdr-client = {git = "https://github.com/Glovo/cortex-xdr-client.git", rev = "v2.0.4"}
```

```python
from cortex_xdr_client.api.authentication import Authentication, AuthenticationType
from cortex_xdr_client.client import CortexXDRClient

auth = Authentication(api_key="<api-key>", api_key_id=<api-key-id>)   # Advanced key by default
# Standard key: Authentication(..., auth_type=AuthenticationType.STANDARD)
client = CortexXDRClient(auth=auth, fqdn="<tenant-fqdn>")             # client calls https://api-<tenant-fqdn>/...
incidents = client.incidents_api.get_incidents()
```

### Build logic

| Piece | Detail |
|---|---|
| Packaging | Poetry project, package `cortex_xdr_client`, build backend `poetry-core>=1.0.0` |
| Lock file | [`poetry.lock`](poetry.lock), generated by Poetry 1.5.1 (locks `requests` 2.32.3, `pydantic` 1.10.21, `pytest` 7.4.4) |
| Dev dependencies | `requests-mock` `^1.9.3`, `pytest` `^7.2.0`, `pytest-cov` `^4.0.0`, `pytest-mock` `^3.10.0` |
| API docs | Sphinx 5.3.0 + `sphinx-rtd-theme` via [`docs/requirements.txt`](docs/requirements.txt) and [`.readthedocs.yaml`](.readthedocs.yaml). [`docs/source/readme.rst`](docs/source/readme.rst) includes [`README.rst`](README.rst), not this file |
| Release | [`release.sh`](release.sh); see [Releasing](#releasing) |

> [!WARNING]
> **Python 3.8 no longer works.** `pyproject.toml` moved to `^3.9` in v2.0.4, and the models use
> `list[str]` (3.9+ syntax). But [`.python-version`](.python-version) and both workflows that run the
> tests still pin **3.8.12**, and `.readthedocs.yaml` pins 3.8. Use 3.9 or newer locally.

> [!NOTE]
> The public Read the Docs site, `cortex-xdr-client.readthedocs.io`, documents **upstream's** code
> (version 2.0.0, with modules this fork doesn't have, such as `cases_api`), not this fork.

---

## Testing

```bash
poetry run python -m pytest tests/           # all tests (CONTRIBUTING.md)
poetry run python -m pytest -v tests         # what the CI workflows run
```

- **1 test file**, [`tests/test_client.py`](tests/test_client.py), plus fixtures in
  [`tests/conftest.py`](tests/conftest.py).
- Tests make no network calls. The `requests_mock` fixture (from `requests-mock`) stubs each
  call's URL, built with `_get_url("<call>")`. `conftest.py` patches `Authentication.get_headers`
  and builds a client with a dummy key and FQDN. Canned Cortex replies live as fixtures in
  `conftest.py`.
- This fork's additions (`audits_api.get_audit_management_logs` and `alerts_api.get_alerts_v2`)
  have no tests yet.

---

## CI/CD

| Workflow | Trigger | Effect |
|---|---|---|
| [`python-test.yml`](.github/workflows/python-test.yml) | Push to `master` and any PR, only when `cortex_xdr_client/**`, `poetry.lock`, `pyproject.toml` or the workflow file change | `poetry install` + `pytest -v tests` on Python 3.8.12 |
| [`codeql-analysis.yml`](.github/workflows/codeql-analysis.yml) | Manual; push and PR to `master` touching `cortex_xdr_client/**`, `poetry.lock` or `pyproject.toml` (PRs also the workflow file) | CodeQL `security-extended` queries for Python |
| [`python-publish.yml`](.github/workflows/python-publish.yml) | Push of a `v*` tag | Tests, then `poetry version <tag>`, `poetry build` and `poetry publish` to PyPI with the `PYPI_API_TOKEN` secret |
| [`stale.yml`](.github/workflows/stale.yml) | Daily at 07:21 UTC | Marks issues and PRs stale after 30 days without activity; closes them 14 days later |

> [!NOTE]
> **None of these workflows has run in this fork.** As of 2026-10-29, the GitHub Actions API
> reports 0 workflows and 0 runs for `Glovo/cortex-xdr-client`. Run the tests locally before
> tagging. [`dependabot.yml`](.github/dependabot.yml) asks for daily pip updates; the Dependabot
> PRs in the history (#12–#133) came from upstream.

### Releasing

```bash
./release.sh 2.0.5    # checks out master, poetry version 2.0.5, commits "Bump to v2.0.5", pushes master, tags v2.0.5, pushes tags
```

Glovo tagged `v1.9.0` and `v2.0.0`–`v2.0.4` between 2025-01-27 and 2025-03-17, usually right after
a `chore: bump version` commit. Consumers pick up a release by changing the `rev` they pin.

---

## Security & data handling

> [!WARNING]
> **Replies contain personal data.** Alert and endpoint models carry user names, host names, and
> IP and MAC addresses ([`models/alerts.py`](cortex_xdr_client/api/models/alerts.py),
> [`models/endpoints.py`](cortex_xdr_client/api/models/endpoints.py)). Handle them like any other
> personal data.

**Auth model** ([`authentication.py`](cortex_xdr_client/api/authentication.py)):

| Key type | Headers sent on every call |
|---|---|
| `AuthenticationType.ADVANCED` (default) | `x-xdr-auth-id`, `x-xdr-nonce` (64 random characters), `x-xdr-timestamp` (ms), and `Authorization` = SHA-256 of key + nonce + timestamp |
| `AuthenticationType.STANDARD` | `x-xdr-auth-id` and `Authorization` = the raw API key |

- Several methods act on live endpoints: `isolate_endpoints`, `unisolate_endpoints`,
  `scan_endpoints`, `quarantine_file`, `retrieve_file`, `run_script` and `run_snippet_code_script`.
- **`scan_all_endpoints()`** sends `filters: "all"`, so it scans every endpoint in the tenant.

---

## Repository layout

```text
cortex-xdr-client/
├── cortex_xdr_client/          # ⭐ the library
│   ├── client.py               # CortexXDRClient: one attribute per API group
│   └── api/
│       ├── authentication.py   # Standard / Advanced API-key headers
│       ├── base_api.py         # URL building, HTTP call, raise_for_status
│       ├── *_api.py            # one module per API group (alerts, audits, endpoints, …)
│       └── models/             # pydantic response models, request filters, exceptions
├── tests/                      # pytest + requests-mock (1 test file + conftest.py)
├── docs/                       # Sphinx sources for Read the Docs (docs/build/ is git-ignored)
├── .github/
│   ├── workflows/              # test, CodeQL, PyPI publish, stale bot
│   ├── ISSUE_TEMPLATE/         # bug report template
│   ├── CODEOWNERS              # * → ebarti
│   └── dependabot.yml          # daily pip updates
├── pyproject.toml              # Poetry project: name, version, dependencies
├── poetry.lock                 # locked dependencies
├── release.sh                  # bump version, commit, tag, push
├── README.rst                  # earlier README; PyPI long description and Sphinx docs
└── CONTRIBUTING.md             # setup and test commands
```

---

## Contributing & conventions

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup and test commands.

1. **One class per API group.** Subclass `BaseAPI` in `cortex_xdr_client/api/<group>_api.py`,
   passing the Cortex group name (e.g. `"audits"`), and add it as an attribute in
   [`client.py`](cortex_xdr_client/client.py).
2. **Return pydantic models.** Add the response model under
   [`api/models/`](cortex_xdr_client/api/models) and parse with `parse_obj`. `pyproject.toml` keeps
   pydantic below 2, so use the v1 API.
3. **Stay on Python 3.9 syntax.** Commits from March 2025 back-ported type hints for older Python
   versions and swapped `enum.StrEnum` (3.11+) for `enum.Enum`.
4. **Bump the version with the change.** Bump `version` in `pyproject.toml`, then tag
   `v<version>`. Consumers pin the tag.
5. **Test every new call** in [`tests/test_client.py`](tests/test_client.py): stub its URL with
   `requests_mock` and add the canned reply as a fixture in `conftest.py`.
6. **Commit subjects** use Conventional Commit prefixes (`feat:`, `chore:`), as in this fork's
   history.
7. **Report bugs** with the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md), which asks
   for your Python version.

Ownership: [`.github/CODEOWNERS`](.github/CODEOWNERS) has one rule, `*` → `ebarti`.

---

## Glossary

| Term | Meaning |
|---|---|
| Cortex XDR | Palo Alto Networks' extended detection and response platform; this client calls its public API |
| FQDN | Your tenant's host name, passed to `CortexXDRClient`; the client adds the `api-` prefix |
| Standard / Advanced API key | Cortex key types. Standard sends the key as-is; Advanced sends a SHA-256 of key + nonce + timestamp |
| XQL | Cortex's query language; `xql_api` starts queries and fetches their results |
| IoC | Indicator of compromise; `ioc_api.insert_json` uploads them |
| Group action ID | ID returned by a response action, which you poll with `actions_api.get_action_status` |

---

## Ownership & support

- **Code owner:** `ebarti`, the only entry in [`.github/CODEOWNERS`](.github/CODEOWNERS). It's a
  personal account and the upstream author. No Glovo team is listed.
- **Glovo-side changes:** written by `lawiet47`, from 2025-01-27 to 2025-03-17 (git history).
- **Upstream:** [`ebarti/cortex-xdr-client`](https://github.com/ebarti/cortex-xdr-client).
