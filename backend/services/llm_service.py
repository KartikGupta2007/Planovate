# ============================================
# OWNER: Person 4 – LLM Integration
# ============================================

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
from typing import Any

import requests

from . import cache, constants

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, llm_config: dict[str, str] | None = None) -> None:
        cfg = llm_config or {}
        # User-provided values override .env values
        self.provider = (cfg.get("provider") or os.getenv("LLM_PROVIDER", "")).strip().lower()
        self.api_key = (cfg.get("api_key") or "").strip()
        self.model = (cfg.get("model") or "").strip()
        self.timeout = float(os.getenv("LLM_TIMEOUT", "30"))

    def enabled(self) -> bool:
        return self.provider in {"openai", "ollama", "generic", "gemini"}

    def get_location_multipliers(
        self, location: str
    ) -> tuple[dict[str, float] | None, str | None]:
        if not self.enabled():
            return None, "LLM disabled; using base rates for pricing."

        cache_key = f"pricing:{location.strip().lower()}"
        cached = cache.get(cache_key)
        if isinstance(cached, dict):
            return cached, "Used cached location multipliers."

        prompt = (
            "Return JSON only. Provide pricing multipliers for home renovation "
            "in the given Indian city compared to average Indian rates. "
            "All base rates are in Indian Rupees (INR). "
            "Keys: paint, labor, flooring, lighting, repair. "
            "Values are multipliers like 1.05 (above average) or 0.85 (below average). "
            "For example, Mumbai would have higher multipliers than a tier-3 city. "
            f"Location: {location}, India."
        )
        response = self._request_json(prompt)
        if not isinstance(response, dict):
            return None, "LLM unavailable; using base rates for pricing."

        multipliers = {
            key: float(response.get(key, 1.0)) for key in constants.LLM_MULTIPLIER_KEYS
        }
        multipliers = self._clamp_multipliers(multipliers)
        cache.set(cache_key, multipliers, ttl_seconds=24 * 3600)
        cache.flush()
        return multipliers, "Applied LLM location multipliers."

    def rewrite_explanations(
        self, tasks: list[dict[str, Any]], diff_vector: dict[str, float]
    ) -> tuple[dict[str, str] | None, str | None]:
        if not self.enabled():
            return None, None

        cache_key = f"explain:{self._hash_tasks(tasks, diff_vector)}"
        cached = cache.get(cache_key)
        if isinstance(cached, dict):
            return cached, "Used cached LLM explanations."

        payload = [{"task": t.get("task"), "why": t.get("why")} for t in tasks]
        prompt = (
            "Rewrite the 'why' text for each task to be more human-readable. "
            "Preserve the facts. Return JSON only as an array of {task, why}. "
            f"Input: {json.dumps(payload)}"
        )
        response = self._request_json(prompt)
        if not isinstance(response, list):
            return None, None

        mapping: dict[str, str] = {}
        for entry in response:
            if not isinstance(entry, dict):
                continue
            task = entry.get("task")
            why = entry.get("why")
            if isinstance(task, str) and isinstance(why, str):
                mapping[task] = why

        if mapping:
            cache.set(cache_key, mapping, ttl_seconds=6 * 3600)
            cache.flush()
            return mapping, "Applied LLM explanations."

        return None, None

    def _clamp_multipliers(self, multipliers: dict[str, float]) -> dict[str, float]:
        clamped: dict[str, float] = {}
        for key, value in multipliers.items():
            try:
                value = float(value)
            except (TypeError, ValueError):
                value = 1.0
            clamped[key] = min(max(value, 0.6), 1.6)
        return clamped

    def _hash_tasks(self, tasks: list[dict[str, Any]], diff_vector: dict[str, float]) -> str:
        payload = {
            "tasks": [
                {
                    "task": t.get("task"),
                    "priority": t.get("priority"),
                    "diff_value": t.get("diff_value"),
                }
                for t in tasks
            ],
            "diff_vector": diff_vector,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _request_json(self, prompt: str) -> Any | None:
        messages = [
            {
                "role": "system",
                "content": "You are a service that returns JSON only with no extra text.",
            },
            {"role": "user", "content": prompt},
        ]

        for attempt in range(2):
            if attempt == 1:
                messages.append(
                    {
                        "role": "system",
                        "content": "Return valid JSON only. No markdown, no commentary.",
                    }
                )
            try:
                content = self._call_provider(messages)
            except Exception as exc:
                logger.warning("LLM call failed (attempt %d): %s", attempt + 1, exc)
                content = ""
            parsed = self._parse_json(content)
            if parsed is not None:
                return parsed
        return None

    def _call_provider(self, messages: list[dict[str, str]]) -> str:
        if self.provider == "openai":
            return self._call_openai(messages)
        if self.provider == "gemini":
            return self._call_gemini(messages)
        if self.provider == "ollama":
            return self._call_ollama(messages)
        if self.provider == "generic":
            return self._call_generic(messages)
        return ""

    def _call_openai(self, messages: list[dict[str, str]]) -> str:
        api_key = self.api_key or os.getenv("OPENAI_API_KEY", "")
        model = self.model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not api_key:
            return ""

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.2,
        }
        response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def _call_gemini(self, messages: list[dict[str, str]]) -> str:
        api_key = self.api_key or os.getenv("GEMINI_API_KEY", "")
        model = self.model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        if not api_key:
            return ""

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
            f":generateContent?key={api_key}"
        )

        # Combine all messages into a single prompt for Gemini
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }

        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        # Extract text from Gemini response
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
        return ""

    def _call_ollama(self, messages: list[dict[str, str]]) -> str:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = self.model or os.getenv("OLLAMA_MODEL", "llama3.1")
        url = f"{base_url.rstrip('/')}/api/chat"
        payload = {"model": model, "messages": messages, "stream": False}
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")

    def _call_generic(self, messages: list[dict[str, str]]) -> str:
        url = os.getenv("GENERIC_LLM_URL", "")
        api_key = self.api_key or os.getenv("GENERIC_LLM_KEY", "")
        if not url:
            return ""

        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {"prompt": prompt}
        response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            if "content" in data:
                return str(data["content"])
            if "text" in data:
                return str(data["text"])
        return ""

    def _parse_json(self, content: str) -> Any | None:
        if not content:
            return None

        # Strip markdown code fences (Gemini often returns ```json ... ```)
        cleaned = re.sub(r"```(?:json)?\s*", "", content).strip()
        cleaned = cleaned.rstrip("`").strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        start_obj = cleaned.find("{")
        end_obj = cleaned.rfind("}")
        start_arr = cleaned.find("[")
        end_arr = cleaned.rfind("]")

        if start_obj != -1 and end_obj != -1 and end_obj > start_obj:
            snippet = cleaned[start_obj : end_obj + 1]
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                return None
        if start_arr != -1 and end_arr != -1 and end_arr > start_arr:
            snippet = cleaned[start_arr : end_arr + 1]
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                return None
        return None


def get_llm_client(llm_config: dict[str, str] | None = None) -> LLMClient:
    return LLMClient(llm_config=llm_config)
