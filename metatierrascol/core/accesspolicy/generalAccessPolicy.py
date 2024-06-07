from rest_access_policy import AccessPolicy

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
     
