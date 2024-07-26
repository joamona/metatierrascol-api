from rest_access_policy import AccessPolicy

"""
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
"""
class AllowAdminOnly(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["group:admin"],
            "effect": "allow"
        }
    ]

class AllowAny(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": "*",
            "effect": "allow"
        }
    ]

class AllowAnySafeMethods(AccessPolicy):
    statements = [
        {
            "action": ["<safe_methods>"],
            "principal": "*",
            "effect": "allow"
        }
    ]

class AllowAuthenticatedSafeMethodsAdminPostMethods(AccessPolicy):
    statements = [
        {
            "action": ["<safe_methods>"],
            "principal": "authenticated",
            "effect": "allow"
        },
        {
            "action": ["*"],
            "principal": ["group:admin"],
            "effect": "allow"
        },

    ]

class AllowAnySafeMethodsAdminPostMethods(AccessPolicy):
    statements = [
        {
            "action": ["<safe_methods>"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["*"],
            "principal": ["group:admin"],
            "effect": "allow"
        },

    ]

class Allow_AuthenticatedSafeMethodsAndPostMethods(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": "authenticated",
            "effect": "allow"
        },
    ]

class AllowAuthenticatedSafeMethods(AccessPolicy):
     statements = [
        {
            "action": ["<safe_methods>"],
            "principal": "authenticated",
            "effect": "allow"
        },
    ]
     

class AllowAnyCreate_AdminRestOfOperations(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["list", "retrieve", "update","partial_update", "destroy", "list", "get_all"],
            "principal": ["group:admin"],
            "effect": "allow",
        },

    ]

class AllowOnlyModifyAndListToAdmin(AccessPolicy):
    statements = [
        {
            "action": ["create", "destroy"],
            "principal": "*",
            "effect": "deny",
        },
        {
            "action": ["list", "retrieve", "update","partial_update", "list"],
            "principal": ["group:admin"],
            "effect": "allow",
        },

    ]