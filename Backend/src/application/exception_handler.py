# src/application/exception_handler.py
from __future__ import annotations


class DomainError(Exception):
    """Base for all domain errors."""
    def __init__(self, message: str, code: str = "domain_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class UserNotFoundError(DomainError):
    def __init__(self):
        super().__init__("User not found", "user_not_found")


class DuplicateEmailError(DomainError):
    def __init__(self):
        super().__init__("Email already registered", "duplicate_email")


class InvalidPasswordError(DomainError):
    def __init__(self):
        super().__init__("Current password is incorrect", "invalid_password")


class TokenExpiredError(DomainError):
    def __init__(self):
        super().__init__("Token has expired", "token_expired")


class TokenInvalidError(DomainError):
    def __init__(self):
        super().__init__("Invalid token", "token_invalid")


class RoleNotFoundError(DomainError):
    def __init__(self, slug: str):
        super().__init__(f"Role '{slug}' not found", "role_not_found")


class InactiveAccountError(DomainError):
    def __init__(self):
        super().__init__("Account is inactive", "inactive_account")

# ADDED: follows same DomainError pattern as all other exceptions
class TenantAccessError(DomainError):
    def __init__(self):
        super().__init__("Cannot manage users from another tenant", "tenant_access_denied")