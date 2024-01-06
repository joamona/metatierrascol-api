from rest_access_policy import AccessPolicy

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

class AllowAuthenticatedSafeMethodsAndPostMethods(AccessPolicy):
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
     
