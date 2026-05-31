# src/domain/entities/__init__.py

# ── base ─────────────────────────────────────────────────────────────────────
from src.domain.entities.base import BaseModel

# ── tenant & store ────────────────────────────────────────────────────────────
from src.domain.entities.tenant import Tenant
from src.domain.entities.store import Store

# ── auth junction tables (must come before User and Role) ─────────────────────
from src.domain.entities.auth.user_role import user_roles
from src.domain.entities.auth.role_permission import role_permissions
from src.domain.entities.auth.user_permission import user_permissions

# ── auth entities ─────────────────────────────────────────────────────────────
from src.domain.entities.auth.permission import Permission
from src.domain.entities.auth.role import Role
from src.domain.entities.auth.session import Session
from src.domain.entities.auth.personal_access_token import PersonalAccessToken
from src.domain.entities.auth.password_reset_token import PasswordResetToken
from src.domain.entities.auth.email_verification_token import EmailVerificationToken
from src.domain.entities.auth.admin_invite_token import AdminInviteToken

# ── user (after Role — User.roles references Role) ────────────────────────────
from src.domain.entities.user import User

# ── customer ──────────────────────────────────────────────────────────────────
from src.domain.entities.customer.customer import Customer
from src.domain.entities.customer.customer_profile import CustomerProfile

# ── product ───────────────────────────────────────────────────────────────────
from src.domain.entities.product.product_category import ProductCategory
from src.domain.entities.product.product import Product
from src.domain.entities.product.customer_product import CustomerProduct
from src.domain.entities.product.brand import Brand

# ── inventory ─────────────────────────────────────────────────────────────────
from src.domain.entities.inventory.stock_movement import StockMovement
from src.domain.entities.inventory.stock_alert import StockAlert

# ── sales ─────────────────────────────────────────────────────────────────────
from src.domain.entities.sales.sale import Sale
from src.domain.entities.sales.sale_item import SaleItem

# ── subscription ──────────────────────────────────────────────────────────────
from src.domain.entities.subscription.subscription_plan import SubscriptionPlan
from src.domain.entities.subscription.feature import Feature
from src.domain.entities.subscription.plan_feature import PlanFeature
from src.domain.entities.subscription.subscription import Subscription
from src.domain.entities.subscription.subscription_feature import SubscriptionFeature

# ── employee ──────────────────────────────────────────────────────────────────
from src.domain.entities.employee.employee_profile import EmployeeProfile
from src.domain.entities.employee.employee_attendance import EmployeeAttendance
from src.domain.entities.employee.employee_payroll import EmployeePayroll
from src.domain.entities.employee.leave_application import LeaveApplication

# ── ml ────────────────────────────────────────────────────────────────────────
from src.domain.entities.ml.product_forecast import ProductForecast

# ── alerts ────────────────────────────────────────────────────────────────────
from src.domain.entities.alerts.worker_alert import WorkerAlert
from src.domain.entities.alerts.alert_rule import AlertRule

# ── operational ───────────────────────────────────────────────────────────────
from src.domain.entities.operational.setting import Setting
from src.domain.entities.operational.notification import Notification
from src.domain.entities.operational.document import Document
from src.domain.entities.operational.audit_log import AuditLog
from src.domain.entities.operational.ai_telemetry import AITelemetry
from src.domain.entities.operational.chatbot_memory import ChatbotMemory

# ── documents ─────────────────────────────────────────────────────────────────
from src.domain.entities.document.file_access_token import FileAccessToken


__all__ = [
    "BaseModel",
    "Tenant", "Store",
    "user_roles", "role_permissions", "user_permissions",
    "Permission", "Role",
    "Session", "PersonalAccessToken", "PasswordResetToken",
    "EmailVerificationToken", "AdminInviteToken",
    "User",
    "Customer", "CustomerProfile",
    "ProductCategory", "Product", "CustomerProduct", "Brand",
    "StockMovement", "StockAlert",
    "Sale", "SaleItem", 
    "SubscriptionPlan", "Feature", "PlanFeature",
    "Subscription", "SubscriptionFeature",
    "EmployeeProfile", "EmployeeAttendance",
    "EmployeePayroll", "LeaveApplication",
    "ProductForecast",
    "WorkerAlert", "AlertRule",
    "Setting", "Notification", "Document",
    "AuditLog", "AITelemetry", "ChatbotMemory",
    "FileAccessToken",
]