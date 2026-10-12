"""Curated, immutable upstream OSS references for MNIN Bridge Pro.

The GitHub app connects ChatGPT to an owned repository. A URL in this catalog
does NOT connect a third-party repository as a ChatGPT plugin, authorize its
code, install its binaries, or guarantee a zero-cost hosted service.
"""
from __future__ import annotations

import re

TOOLS = (
    {
        "id": "playwright", "repository": "microsoft/playwright",
        "url": "https://github.com/microsoft/playwright", "license": "Apache-2.0",
        "purpose": "Captured browser QA, 21 responsive viewports, console errors",
        "domains": ["browser", "responsive", "functional", "fr_ar_rtl"],
        "package": "playwright", "execution": "EXISTING_LOCAL_RUNNER",
    },
    {
        "id": "axe_core", "repository": "dequelabs/axe-core",
        "url": "https://github.com/dequelabs/axe-core", "license": "MPL-2.0",
        "purpose": "Rule-based accessibility violations in local browser QA",
        "domains": ["accessibility", "browser", "fr_ar_rtl"],
        "package": "axe-core", "execution": "IN_MANUAL_BROWSER_QA_CODE",
    },
    {
        "id": "html_validate", "repository": "html-validate/html-validate",
        "url": "https://github.com/html-validate/html-validate", "license": "MIT",
        "purpose": "Offline HTML structure validation",
        "domains": ["html", "accessibility", "quality"],
        "package": "html-validate", "execution": "IN_MANUAL_BROWSER_QA_WORKFLOW",
    },
    {
        "id": "lighthouse", "repository": "GoogleChrome/lighthouse",
        "url": "https://github.com/GoogleChrome/lighthouse", "license": "Apache-2.0",
        "purpose": "Measured performance and best practices on an approved local page",
        "domains": ["performance", "seo", "browser"],
        "package": "lighthouse", "execution": "PLANNED_NOT_INSTALLED",
    },
    {
        "id": "svgo", "repository": "svg/svgo",
        "url": "https://github.com/svg/svgo", "license": "MIT",
        "purpose": "SVG optimization on an isolated copy, originals preserved",
        "domains": ["assets", "svg", "design"],
        "package": "svgo", "execution": "PLANNED_NOT_INSTALLED",
    },
    {
        "id": "sharp", "repository": "lovell/sharp",
        "url": "https://github.com/lovell/sharp", "license": "Apache-2.0",
        "purpose": "Inspect raster image metadata and generate opt-in derivatives only",
        "domains": ["assets", "performance", "images"],
        "package": "sharp", "execution": "PLANNED_NOT_INSTALLED",
    },
    {
        "id": "wordpress_cs", "repository": "WordPress/WordPress-Coding-Standards",
        "url": "https://github.com/WordPress/WordPress-Coding-Standards",
        "license": "MIT",
        "purpose": "Review PHP theme/plugin conventions with PHPCS and Composer",
        "domains": ["wordpress", "php", "security", "quality"],
        "package": "wp-coding-standards/wpcs", "execution": "PLANNED_NO_PHP_SOURCES",
    },
    {
        "id": "prettier", "repository": "prettier/prettier",
        "url": "https://github.com/prettier/prettier", "license": "MIT",
        "purpose": "Consistent HTML/CSS/JavaScript formatting (check mode)",
        "domains": ["html", "css", "quality", "design"],
        "package": "prettier", "execution": "PLANNED_NOT_INSTALLED",
    },
)

_TOOL_MAP = {item["id"]: item for item in TOOLS}
DOMAIN = re.compile(r"^[a-z][a-z0-9_]{0,35}$")


def catalog_open_source_tools(domain: str = "") -> dict:
    """List vetted public upstreams without asserting deployment or account linkage."""
    if not isinstance(domain, str) or len(domain) > 36 or (domain and not DOMAIN.fullmatch(domain)):
        raise ValueError("Invalid domain")
    selected = [dict(item) for item in TOOLS if not domain or domain in item["domains"]]
    return {
        "version": "0.7.0",
        "count": len(selected),
        "available_domains": sorted({d for item in TOOLS for d in item["domains"]}),
        "upstreams": selected,
        "user_github_integration": "Use separately authorized GitHub app",
        "upstream_chatgpt_plugins_connected_by_this_catalog": 0,
        "remote_installations_performed": 0,
        "note": "GitHub OSS is reusable through explicit dependency builds, CI and file review, not automatically connected as a native ChatGPT plugin. Licenses require compliance.",
    }


def open_source_pipeline(mission: str) -> dict:
    tasks = {
        "home_qa": ("html_validate", "playwright", "axe_core", "lighthouse"),
        "asset_quality": ("sharp", "svgo", "playwright"),
        "wordpress_development": ("wordpress_cs", "prettier", "playwright", "axe_core"),
        "bilingual_accessibility": ("html_validate", "playwright", "axe_core"),
    }
    if mission not in tasks:
        raise ValueError("Unknown mission. Choose home_qa, asset_quality, wordpress_development or bilingual_accessibility")
    stages = []
    for i, item_id in enumerate(tasks[mission], 1):
        tool = _TOOL_MAP[item_id]
        stages.append({
            "order": i,
            "tool": item_id,
            "repository": tool["url"],
            "purpose": tool["purpose"],
            "source_integration_state": tool["execution"],
            "executed_now": False,
            "test_result": "NON TESTÉ",
            "prerequisites": [
                "Authorized, locally checked-out source and approved test scope",
                "Explicit package installation in isolated environment if needed",
                "Actual runtime logs before reporting PASS",
            ],
        })
    return {
        "mission": mission,
        "steps": stages,
        "model_api_cost": 0,
        "requires_work_or_codex": False,
        "site_writes_allowed": False,
        "actual_execution": "PLAN_ONLY",
    }
