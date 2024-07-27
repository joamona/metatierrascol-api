from rest_access_policy import AccessPolicy

"""
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.

    If you define any other method, you must add its name to the allow/deny list
"""

class DjangoAndAppUserViewsAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "*",
            "effect": "allow",
        },
        {
            "action": ["get_users", "get_users_of_group"],
            "principal": ["group:admin"],
            "effect": "allow",
        },

    ]

class DjangoGroupsViewsAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create","update","partial_update"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        {
            "action": ["list"],
            "principal": "authenticated",
            "effect": "allow",
        },

    ]

class AppSettingsViewsAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["group:admin"],
            "effect": "allow",
        }
    ]



