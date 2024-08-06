from rest_access_policy import AccessPolicy
from core.commonlibs import generalModule

"""
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.

    If you define any other method, you must add its name to the allow/deny list
"""

class BaunitViewSetAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["create"],
            "principal": "authenticated",
            "effect": "allow"
        },
        {
            "action": ["retrieve","update", "partial_update", "list", "get_created_by_user_baunits"],
            "principal": "authenticated",
            "effect": "allow",
            "condition_expression": ["(user_must_be_creator:nada or user_must_be_admin:nada)"]
        },
    ]

    def user_must_be_creator(self, request, view, action, field: str) -> bool:
        creado_por=request.data.get('creado_por','')
        #print('user_must_be_creator', creado_por, creado_por == request.user.username)
        return creado_por == request.user.username
    
    def user_must_be_admin(self, request, view, action, field: str) -> bool:
        #print('user_must_be_admin', generalModule.isAdministrator(request))
        return generalModule.isAdministrator(request)