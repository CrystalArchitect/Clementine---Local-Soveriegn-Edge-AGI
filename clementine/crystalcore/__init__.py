"""
CrystalCore — the sovereign companion framework.

CrystalCore is the engine: layered memory, semantic recall, profiles,
personality, and a model connection — everything a sovereign companion
needs. That model normally runs on the same machine and nothing leaves it;
where it does not, a consent gate asks first and an append-only, hash-chained
audit log records what happened either way.

Clementine is the first persona who lives on it (and the default one
shipped here). Your human may rename her; the framework doesn't mind.
"""

from .audit import AuditLog
from .companion import BASE_PROMPT, Clementine
from .consent import (ConsentGate, ConsentRefused, Request, Verdict,
                      destination_of, terminal_asker)
from .memory import Memory, Personality
from .profiles import (PROFILES_DIR, delete_profile, list_profiles,
                       profile_dir, profile_meta)

# The framework name for the companion class, for those who prefer it.
Companion = Clementine

__version__ = "0.8.0"

__all__ = [
    "Clementine", "Companion", "Personality", "Memory", "BASE_PROMPT",
    "PROFILES_DIR", "profile_dir", "list_profiles", "profile_meta",
    "delete_profile", "AuditLog", "ConsentGate", "ConsentRefused",
    "Request", "Verdict", "destination_of", "terminal_asker", "__version__",
]
