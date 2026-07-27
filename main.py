"""Mock LMS SCIM API toolkit for testing and development."""

import logging
import os
import re
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)

TOKEN = os.getenv("SCIM_TOKEN")

if not TOKEN:
    log.critical("SCIM_TOKEN environment variable is not set")
    raise RuntimeError("SCIM_TOKEN environment variable is not set")

log.info("SCIM_TOKEN loaded successfully: %s (length=%d)", TOKEN, len(TOKEN))

security = HTTPBearer()

app = FastAPI(title="Mock LMS SCIM API")

users = [
    {
        "id": "1001",
        "userName": "alice.adams@example.com",
        "name": {"givenName": "Alice", "familyName": "Adams"},
        "displayName": "Alice Adams",
        "emails": [
            {"value": "alice.adams@example.com", "type": "work", "primary": True},
        ],
        "active": True,
        "roles": [{"value": "role-learner", "display": "Learner"}],
        "entitlements": [
            {
                "value": "catalog-general",
                "display": "General Training",
                "type": "Training Catalog",
            },
            {
                "value": "catalog-cybersecurity",
                "display": "Cybersecurity",
                "type": "Training Catalog",
            },
            {"value": "scope-self", "display": "Self", "type": "Organizational Scope"},
        ],
    },
    {
        "id": "1002",
        "userName": "bob.brown@example.com",
        "name": {"givenName": "Bob", "familyName": "Brown"},
        "displayName": "Bob Brown",
        "emails": [{"value": "bob.brown@example.com", "type": "work", "primary": True}],
        "active": True,
        "roles": [{"value": "role-training-manager", "display": "Training Manager"}],
        "entitlements": [
            {
                "value": "catalog-general",
                "display": "General Training",
                "type": "Training Catalog",
            },
            {
                "value": "catalog-leadership",
                "display": "Leadership",
                "type": "Training Catalog",
            },
            {
                "value": "scope-direct-reports",
                "display": "Direct Reports",
                "type": "Organizational Scope",
            },
            {
                "value": "report-completion",
                "display": "Completion Reports",
                "type": "Reporting Access",
            },
            {
                "value": "report-compliance",
                "display": "Compliance Reports",
                "type": "Reporting Access",
            },
        ],
    },
    {
        "id": "1003",
        "userName": "carol.clark@example.com",
        "name": {"givenName": "Carol", "familyName": "Clark"},
        "displayName": "Carol Clark",
        "emails": [
            {"value": "carol.clark@example.com", "type": "work", "primary": True},
        ],
        "active": True,
        "roles": [{"value": "role-course-creator", "display": "Course Creator"}],
        "entitlements": [
            {
                "value": "catalog-hr",
                "display": "Human Resources",
                "type": "Training Catalog",
            },
            {
                "value": "scope-department",
                "display": "Department",
                "type": "Organizational Scope",
            },
        ],
    },
    {
        "id": "1004",
        "userName": "david.davis@example.com",
        "name": {"givenName": "David", "familyName": "Davis"},
        "displayName": "David Davis",
        "emails": [
            {"value": "david.davis@example.com", "type": "work", "primary": True},
        ],
        "active": True,
        "roles": [
            {"value": "role-compliance-manager", "display": "Compliance Manager"},
        ],
        "entitlements": [
            {
                "value": "catalog-cybersecurity",
                "display": "Cybersecurity",
                "type": "Training Catalog",
            },
            {
                "value": "scope-global",
                "display": "Global",
                "type": "Organizational Scope",
            },
            {
                "value": "report-compliance",
                "display": "Compliance Reports",
                "type": "Reporting Access",
            },
            {
                "value": "report-certification",
                "display": "Certification Reports",
                "type": "Reporting Access",
            },
        ],
    },
    {
        "id": "1005",
        "userName": "erin.evans@example.com",
        "name": {"givenName": "Erin", "familyName": "Evans"},
        "displayName": "Erin Evans",
        "emails": [
            {"value": "erin.evans@example.com", "type": "work", "primary": True},
        ],
        "active": True,
        "roles": [{"value": "role-auditor", "display": "Auditor"}],
        "entitlements": [
            {
                "value": "scope-global",
                "display": "Global",
                "type": "Organizational Scope",
            },
            {
                "value": "report-completion",
                "display": "Completion Reports",
                "type": "Reporting Access",
            },
            {
                "value": "report-compliance",
                "display": "Compliance Reports",
                "type": "Reporting Access",
            },
            {
                "value": "report-certification",
                "display": "Certification Reports",
                "type": "Reporting Access",
            },
            {
                "value": "report-users",
                "display": "User Reports",
                "type": "Reporting Access",
            },
        ],
    },
    {
        "id": "1006",
        "userName": "frank.foster@example.com",
        "name": {"givenName": "Frank", "familyName": "Foster"},
        "displayName": "Frank Foster",
        "emails": [
            {"value": "frank.foster@example.com", "type": "work", "primary": True},
        ],
        "active": True,
        "roles": [{"value": "role-lms-admin", "display": "LMS Administrator"}],
        "entitlements": [
            {
                "value": "scope-global",
                "display": "Global",
                "type": "Organizational Scope",
            },
            {
                "value": "report-executive",
                "display": "Executive Dashboards",
                "type": "Reporting Access",
            },
        ],
    },
]

lms_roles = [
    {
        "id": "role-learner",
        "displayName": "Learner",
        "description": "Standard employee access to assigned training.",
    },
    {
        "id": "role-instructor",
        "displayName": "Instructor",
        "description": "Deliver courses and manage assigned classes.",
    },
    {
        "id": "role-course-creator",
        "displayName": "Course Creator",
        "description": "Create and modify LMS course content.",
    },
    {
        "id": "role-training-manager",
        "displayName": "Training Manager",
        "description": "Assign training and review employee completion.",
    },
    {
        "id": "role-compliance-manager",
        "displayName": "Compliance Manager",
        "description": "Manage compliance-related training.",
    },
    {
        "id": "role-auditor",
        "displayName": "Auditor",
        "description": "Read-only access to training and compliance information.",
    },
    {
        "id": "role-lms-admin",
        "displayName": "LMS Administrator",
        "description": "Full administrative access to the LMS.",
    },
]

training_catalogs = [
    {
        "id": "catalog-general",
        "displayName": "General Training",
        "description": "Standard employee training catalog.",
    },
    {
        "id": "catalog-cybersecurity",
        "displayName": "Cybersecurity",
        "description": "Security awareness and technical security training.",
    },
    {
        "id": "catalog-leadership",
        "displayName": "Leadership",
        "description": "Management and leadership courses.",
    },
    {
        "id": "catalog-hr",
        "displayName": "Human Resources",
        "description": "Human Resources training catalog.",
    },
    {
        "id": "catalog-finance",
        "displayName": "Finance",
        "description": "Finance and accounting training.",
    },
    {
        "id": "catalog-it",
        "displayName": "IT Technical",
        "description": "Technical IT training.",
    },
]

organizational_scopes = [
    {
        "id": "scope-self",
        "displayName": "Self",
        "description": "Access only the user's own training records.",
    },
    {
        "id": "scope-direct-reports",
        "displayName": "Direct Reports",
        "description": "Access training records for direct reports.",
    },
    {
        "id": "scope-department",
        "displayName": "Department",
        "description": "Access training records for the user's department.",
    },
    {
        "id": "scope-business-unit",
        "displayName": "Business Unit",
        "description": "Access training records across a business unit.",
    },
    {
        "id": "scope-global",
        "displayName": "Global",
        "description": "Access training records for the entire organization.",
    },
]

reporting_access = [
    {
        "id": "report-completion",
        "displayName": "Completion Reports",
        "description": "View training completion reports.",
    },
    {
        "id": "report-compliance",
        "displayName": "Compliance Reports",
        "description": "View compliance status reports.",
    },
    {
        "id": "report-certification",
        "displayName": "Certification Reports",
        "description": "View certification and expiration reports.",
    },
    {
        "id": "report-users",
        "displayName": "User Reports",
        "description": "View individual user training histories.",
    },
    {
        "id": "report-executive",
        "displayName": "Executive Dashboards",
        "description": "View executive-level training analytics.",
    },
]


def validate_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> HTTPAuthorizationCredentials:
    """Validate the bearer token provided in the Authorization header."""
    if credentials.credentials != TOKEN:
        log.warning(
            "Authentication failed: received token length=%d",
            len(credentials.credentials),
        )

        raise HTTPException(status_code=401, detail="Invalid bearer token")

    log.debug("Bearer token authentication successful")

    return credentials

auth_creds = Annotated[HTTPAuthorizationCredentials, Depends(validate_token)]

@app.get("/")
def root() -> dict:
    """Root endpoint for health check."""
    return {"service": "Mock LMS SCIM API", "status": "running"}

@app.get("/scim/v2/Users")
def get_users(
    _credentials: auth_creds,
    filtered: Annotated[str | None, Query()] = None,
    start_index: Annotated[int, Query(alias="startIndex")] = 1,
    count: Annotated[int, Query(ge=1)] = 100,
) -> dict:
    """Get a list of users with optional filtering and pagination."""
    filtered_users = users

    if filtered:
        match = re.match(r'userName\s+eq\s+"([^"]+)"', filtered, re.IGNORECASE)

        if match:
            username = match.group(1)

            filtered_users = [
                user for user in users if user["userName"].lower() == username.lower()
            ]

    start = start_index - 1
    end = start + count

    paged_users = filtered_users[start:end]

    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(filtered_users),
        "startIndex": start_index,
        "itemsPerPage": len(paged_users),
        "Resources": paged_users,
    }

@app.get("/scim/v2/Users/{user_id}")
def get_user(
    user_id: str,
    _credentials: auth_creds,
) -> dict:
    """Get a specific user by ID."""
    user = next((user for user in users if user["id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.get("/scim/v2/ResourceTypes")
def get_resource_types(
    _credentials: auth_creds,
) -> dict:
    """Get a list of resource types."""
    resources = [
        {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
            "id": "User",
            "name": "User",
            "endpoint": "/Users",
            "description": "LMS Users",
            "schema": "urn:ietf:params:scim:schemas:core:2.0:User",
        },
        {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
            "id": "LMSRole",
            "name": "LMS Role",
            "endpoint": "/Roles",
            "description": "LMS application roles",
            "schema": "urn:okta:scim:schemas:core:1.0:Role",
        },
        {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
            "id": "TrainingCatalog",
            "name": "Training Catalog",
            "endpoint": "/TrainingCatalogs",
            "description": "LMS training catalog access",
            "schema": "urn:okta:scim:schemas:core:1.0:Entitlement",
        },
        {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
            "id": "OrganizationalScope",
            "name": "Organizational Scope",
            "endpoint": "/OrganizationalScopes",
            "description": "Scope of users and training records accessible to the user",
            "schema": "urn:okta:scim:schemas:core:1.0:Entitlement",
        },
        {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:ResourceType"],
            "id": "ReportingAccess",
            "name": "Reporting Access",
            "endpoint": "/ReportingAccess",
            "description": "LMS reporting permissions",
            "schema": "urn:okta:scim:schemas:core:1.0:Entitlement",
        },
    ]

    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(resources),
        "startIndex": 1,
        "itemsPerPage": len(resources),
        "Resources": resources,
    }

@app.get("/scim/v2/Roles")
def get_roles(
    _credentials: auth_creds,
) -> dict:
    """Get a list of LMS roles."""
    resources = []

    for role in lms_roles:
        resources.append({"schemas": ["urn:okta:scim:schemas:core:1.0:Role"], **role})

    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(resources),
        "startIndex": 1,
        "itemsPerPage": len(resources),
        "Resources": resources,
    }

def entitlement_response(items: list, entitlement_type: str):
    """Generate a SCIM response for entitlements (training catalogs, organizational scopes, reporting access)."""
    resources = []

    for item in items:
        resources.append(
            {
                "schemas": ["urn:okta:scim:schemas:core:1.0:Entitlement"],
                "id": item["id"],
                "displayName": item["displayName"],
                "type": entitlement_type,
                "description": item["description"],
            },
        )

    return {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
        "totalResults": len(resources),
        "startIndex": 1,
        "itemsPerPage": len(resources),
        "Resources": resources,
    }

@app.get("/scim/v2/TrainingCatalogs")
def get_training_catalogs(
    _credentials: auth_creds,
) -> dict:
    """Get a list of training catalogs."""
    return entitlement_response(training_catalogs, "Training Catalog")

@app.get("/scim/v2/OrganizationalScopes")
def get_organizational_scopes(
    _credentials: auth_creds,
) -> dict:
    """Get a list of organizational scopes."""
    return entitlement_response(organizational_scopes, "Organizational Scope")

@app.get("/scim/v2/ReportingAccess")
def get_reporting_access(
    _credentials: auth_creds,
) -> dict:
    """Get a list of reporting access entitlements."""
    return entitlement_response(reporting_access, "Reporting Access")
