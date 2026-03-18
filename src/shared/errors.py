from __future__ import annotations


class EPCError(Exception):
    """Base exception for EPC system errors."""


class SchemaValidationError(EPCError):
    """Raised when message/config schema validation fails."""


class StandardsComplianceError(EPCError):
    """Raised when standard applicability or citation integrity fails."""


class CriticalRedFlagError(EPCError):
    """Raised when a critical red flag requires immediate stop."""


class StateTransitionError(EPCError):
    """Raised for invalid orchestrator state transitions."""


class ConsensusError(EPCError):
    """Raised when MAKER consensus cannot be reached."""
