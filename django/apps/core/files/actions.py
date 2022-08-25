from guardian.shortcuts import assign_perm, remove_perm,  get_objects_for_user

from .models import FileSet, Files

def _move_files_set(fs_main: FileSet, fs_sub: FileSet) -> bool:
    for f in Files.objects.filter(file_set__in=fs_sub):
        f.file_set = fs_main
        f.save()
    return True


def merge_sets(set_list: list) -> str:
    """
    to do merge sets both list must belong to the same set of groups
    """
    main_set_uuid = set_list[0]
    sub_sets_uuid = set_list[1:]
    fs_main = FileSet.objects.get(id__in=main_set_uuid)
    fs_sub = FileSet.objects.filter(id__in=sub_sets_uuid)
    _move_files_set(fs_main, fs_sub)
    return f"merged {sub_sets_uuid} with {main_set_uuid}"

def move_file_set_to_another_subscription(subscription, fs_id):
    fs = FileSet.objects.get(id=fs_id)
    fs.subscription = subscription
    fs.save()
    return fs

def assign_moderator_permissions(user, fs_id):
    fs = FileSet.objects.get(id=fs_id)
    assign_perm('can_moderate_files', user, fs)
    return user.has_perm('can_moderate_files', fs)

def remove_moderator_permissions(user, fs_id):
    fs = FileSet.objects.get(id=fs_id)
    remove_perm('can_moderate_files', user, fs)
    return user.has_perm('can_moderate_files', fs)

def has_moderator_permissions(user, fs_id):
    fs = FileSet.objects.get(id=fs_id)
    return user.has_perm('can_moderate_files', fs)

def fetch_fileset_moderator_permissions(user):
    return get_objects_for_user(user, "can_moderate_files", FileSet.objects.all())
