from rest_access_policy import AccessPolicy

"""
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.

    If you define any other method, you must add its name to the allow/deny list
"""

class BaunitViewSetAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": "authenticated",
            "effect": "allow",
        },
    ]
