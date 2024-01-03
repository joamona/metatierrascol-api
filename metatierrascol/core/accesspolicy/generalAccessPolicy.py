from rest_access_policy import AccessPolicy

class AllowAuthenticatedSafeMethods(AccessPolicy):
    statements = [
        {
            "action": ["<safe_methods>"],
            "principal": "authenticated",
            "effect": "allow"
        },

    ]

class AllowAdminPostMethods(AccessPolicy):
    statements = [
        {
            "action": ["<method:post>"],
            "principal": ["group:admin"],
            "effect": "allow"
        },
    ]