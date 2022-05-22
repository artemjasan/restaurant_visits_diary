import typing

from rest_framework import permissions, serializers
from rest_framework.request import Request


class PerActionMixinBase:
    # NOTE: DO NOT overwrite those attributes and methods, they are for type checkers only
    action: str
    request: Request

    get_serializer_class: typing.Callable


class PerActionPermissionClassMixin(PerActionMixinBase):
    """
    Adds to an inherited child property allowing to specify per action permissions.
    Does not exclude the usage of permission_classes in views.
    In case of using both, permission_classes will be applied to all other methods/actions.
    If permission_classes is not included in inherited view,
    default permission_classes specified in settings will be used.
    """

    permission_classes: list[permissions.BasePermission]  # Is for type checking

    action_permission_classes_mapping: dict[str, list[type[permissions.BasePermission]]] = {}

    def get_permissions(self) -> list[permissions.BasePermission]:
        return [
            permission()
            for permission in self.action_permission_classes_mapping.get(self.action, self.permission_classes)
        ]


class PerActionSerializerClassMixin(PerActionMixinBase):
    """
    Adds to an inherited child property allowing to specify per action serializer.
    Either serializer_class property should be present
    or get_serializer class should be overloaded in order for this mixin to properly function.
    """

    action_serializer_class_mapping: dict[str, serializers.BaseSerializer] = {}

    def get_serializer_class(self) -> t.Type[serializers.BaseSerializer]:
        return self.action_serializer_class_mapping.get(self.action, super().get_serializer_class())

