"""Anthropic OAuth → subscription-billed API key exchange.

Reuses the Claude Code / Claude CLI auth session. Requires `org:create_api_key`
scope on the OAuth token. If the current Claude Code token lacks this scope,
re-auth:  `claude auth logout && claude auth login`

Falls back to `ANTHROPIC_API_KEY` (API-credit-billed) if the exchange fails.
"""

from __future__ import annotations

import os

import httpx

EXCHANGE_URL = "https://api.anthropic.com/api/oauth/claude_cli/create_api_key"


class ExchangeError(RuntimeError):
    pass


def exchange_oauth_for_api_key(oauth_token: str, *, name: str = "workbank-drift-2026") -> str:
    """Returns a subscription-billed API key (sk-ant-api03-*) from a Claude-CLI OAuth token."""
    r = httpx.post(
        EXCHANGE_URL,
        headers={
            "Authorization": f"Bearer {oauth_token}",
            "Content-Type": "application/json",
        },
        json={"name": name},
        timeout=30,
    )
    if r.status_code >= 400:
        raise ExchangeError(f"{r.status_code}: {r.text[:300]}")
    data = r.json()
    key = data.get("api_key") or data.get("key")
    if not key:
        raise ExchangeError(f"unexpected response: {data}")
    return key


def resolve_anthropic_key() -> tuple[str, str]:
    """Returns (api_key, billing_mode). billing_mode in {'subscription', 'api'}."""
    oauth = os.environ.get("ANTHROPIC_OAUTH_TOKEN")
    if oauth:
        try:
            return exchange_oauth_for_api_key(oauth), "subscription"
        except ExchangeError as e:
            print(f"[oauth] exchange failed: {e}; falling back to API key")

    api = os.environ.get("ANTHROPIC_API_KEY")
    if not api:
        raise RuntimeError(
            "No Anthropic credentials. Set ANTHROPIC_OAUTH_TOKEN "
            "(preferred, subscription-billed) or ANTHROPIC_API_KEY."
        )
    return api, "api"
