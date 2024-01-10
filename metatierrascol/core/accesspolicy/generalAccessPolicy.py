from rest_access_policy import AccessPolicy

class AllowAny(AccessPolicy):
    statements = [
        {
            "action": ["*"],
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
            "action": ["<method:post>"],
            "principal": ["group:admin"],
            "effect": "allow"
        },

    ]

class Allow_AuthenticatedSafeMethodsAndPostMethods(AccessPolicy):
    statements = [
        {
            "action": ["<safe_methods>","<method:post>"],
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
     
