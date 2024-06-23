# _folders_checked = False
# def _check_folders() -> None:
#     global _folders_checked
#     if _folders_checked:
#         return
#     from os.path import exists, isdir
#     from os import mkdir
#     dirs = [
#         "runtime",
#         "runtime/user-backgrounds",
#         "runtime/user-profile-pictures"
#     ]
#     for d in dirs:
#         if not exists(d) or not isdir(d):
#             mkdir(d)
#     _folders_checked = True

# _check_folders()

class User:

    pass