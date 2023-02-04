from guardian.shortcuts import (
    assign_perm,
    remove_perm,
    get_objects_for_user,
    get_users_with_perms,
)

from .models import FileSet, Files, Subscriptions, User


def _move_files_set(fs_main: FileSet, fs_sub: FileSet) -> bool:
    """
    move files from one set to another
    """
    for f in Files.objects.filter(file_set__in=fs_sub):
        f.file_set = fs_main
        f.save()
    return True


def merge_sets(set_list: list) -> str:
    """
    to do merge sets both list must belong to the same set of groups
    """
    if len(set_list) < 2:
        return "cannot merge sets since defined sets are less than 2"
    main_set_uuid = set_list[0]
    sub_sets_uuid = set_list[1:]
    fs_main = FileSet.objects.get(id__in=main_set_uuid)
    fs_sub = FileSet.objects.filter(id__in=sub_sets_uuid)
    _move_files_set(fs_main, fs_sub)
    return f"merged {sub_sets_uuid} with {main_set_uuid}"


def move_file_set_to_another_subscription(
    subscription: Subscriptions, fs_id: str
) -> FileSet:
    """
    move fileset from one subscription to another
    """
    fs = FileSet.objects.get(id=fs_id)
    fs.subscription = subscription
    fs.save()
    return fs


def assign_moderator_permissions(user, fs_id: str, fs: FileSet = None) -> bool:
    """
    assign user moderator permissions to a fileset
    """
    if fs is None:
        fs = FileSet.objects.get(id=fs_id)
    assign_perm("can_moderate_files", user, fs)
    return fs.has_moderator_access(user)


def remove_moderator_permissions(user: User, fs_id: str, fs: FileSet = None) -> bool:
    """
    remove user moderator permissions from a fileset
    """
    # if fileset is None default using fs_id
    if fs is None:
        fs = FileSet.objects.get(id=fs_id)
    remove_perm("can_moderate_files", user, fs)
    return fs.has_moderator_access(user)


def fetch_fileset_moderator_permissions(user) -> FileSet:
    """
    retrieves users which has moderator permissions for a fileset
    """
    return get_objects_for_user(user, "can_moderate_files", FileSet.objects.all())


def add_moderator_permission_to_moderators(fs: FileSet, moderator: User) -> None:
    """
    apply moderator permissions to a fileset
    """
    for moderator in fs.moderators.all():
        assign_moderator_permissions(moderator, str(fs.id))


def reset_moderator_permissions(fs) -> None:
    """
    remove or reset permissions for a fileset
    """
    moderators = fs.moderators.all()
    users_with_perm = get_users_with_perms(fs)
    # remove users
    for u in users_with_perm.exclude(id__in=moderators):
        remove_moderator_permissions(u, fs_id=str(fs.id), fs=fs)
