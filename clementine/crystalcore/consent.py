"""
CrystalCore consent: nothing leaves without agreement.

The hard part of a consent gate in a *companion* is not strictness, it is
tolerability. Asking permission for every sentence would make her unusable,
and a gate people click through without reading protects nobody. So the rule
here is drawn where it actually means something:

  * Talking to a model on this machine is what she is for. It is recorded,
    not interrupted.
  * Talking to a model somewhere else is a different act. It needs a yes,
    and without one the answer is no.

Fail-closed, deliberately: if no way to ask exists, a remote call is refused
rather than allowed. A gate that opens when the doorman is absent is a door.

Refusals are recorded as carefully as approvals. A log of only the things
that succeeded would flatter the system instead of describing it.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]", "0.0.0.0"}


def destination_of(url: str) -> str:
    """"local" for this machine, otherwise the hostname being contacted."""
    host = (urlparse(url).hostname or "").lower()
    return "local" if host in LOCAL_HOSTS else (host or "unknown")


@dataclass
class Request:
    """What is about to happen, in terms a person can judge."""
    service: str        # "chat" | "embed" | "summary" | "reflect"
    url: str
    model: str
    chars: int = 0      # size of what would be sent, not its content

    @property
    def destination(self) -> str:
        return destination_of(self.url)

    @property
    def is_local(self) -> bool:
        return self.destination == "local"

    def describe(self) -> str:
        where = "this machine" if self.is_local else self.destination
        return (f"{self.service} → {where} using {self.model} "
                f"({self.chars} characters)")


@dataclass
class Verdict:
    approved: bool
    reason: str = ""
    remember: bool = False


class ConsentRefused(Exception):
    """Raised instead of making the call. Carries a human-readable reason."""

    def __init__(self, request: Request, reason: str):
        self.request = request
        self.reason = reason
        super().__init__(reason)


class ConsentGate:
    """Decides, records, and remembers — in that order."""

    def __init__(self, audit=None, asker=None, allow_local: bool = True):
        """
        audit       — an AuditLog, or None to decide without recording
        asker       — callable(Request) -> Verdict, for remote destinations.
                      None means there is no way to ask, so remote is refused.
        allow_local — local calls proceed without interruption (still audited).
                      Set False to require a yes for everything.
        """
        self.audit = audit
        self.asker = asker
        self.allow_local = allow_local
        self._session_ok: set[str] = set()

    def _key(self, request: Request) -> str:
        return f"{request.service}:{request.destination}"

    def check(self, request: Request) -> Verdict:
        """Decide without recording. Useful for showing state in a UI."""
        if request.is_local and self.allow_local:
            return Verdict(True, "local")
        if self._key(request) in self._session_ok:
            return Verdict(True, "approved earlier this session")
        if self.asker is None:
            # Reasons are lowercase fragments: callers compose them into a
            # sentence, and the destination is already named there.
            return Verdict(False, "nothing here is set up to ask your permission")
        verdict = self.asker(request)
        if verdict.approved and verdict.remember:
            self._session_ok.add(self._key(request))
        return verdict

    def require(self, request: Request) -> None:
        """Decide and record. Raises ConsentRefused rather than proceeding."""
        verdict = self.check(request)
        if self.audit is not None:
            self.audit.record(
                request.service,
                request.destination,
                "allowed" if verdict.approved else "refused",
                model=request.model,
                chars=request.chars,
                reason=verdict.reason or None,
            )
        if not verdict.approved:
            raise ConsentRefused(request, verdict.reason or "Consent refused.")


def terminal_asker(request: Request) -> Verdict:
    """Ask on the console. For clementine.py, where a human is watching."""
    print(f"\n  Clementine wants to send: {request.describe()}")
    print(f"  This leaves this machine and goes to {request.destination}.")
    try:
        answer = input("  Allow? [y]es / [a]lways this session / [N]o: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return Verdict(False, "no answer given")
    if answer in {"a", "always"}:
        return Verdict(True, "approved for this session", remember=True)
    if answer in {"y", "yes"}:
        return Verdict(True, "approved once")
    return Verdict(False, "declined at the consent gate")
