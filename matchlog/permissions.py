from rest_framework import permissions


class IsHistoricallySafe(permissions.IsAuthenticatedOrReadOnly):
  def has_object_permission(self, request, view, obj):
    if not super().has_object_permission(request, view, obj):
      return False

    if request.method == "POST":
      return True

    if not obj.owner == request.user:
      return False

    past_objs = obj.__class__.objects.order_by("-created")
    is_most_recent = not past_objs.exists() or past_objs[0].id == obj.id

    if request.method == "DELETE":
      return is_most_recent

    return False
