import copycontents
import os


def main():
    ROOT_DIR = os.path.abspath(os.curdir)
    print(ROOT_DIR)
    STATIC_DIR = os.path.join(ROOT_DIR, "static")
    print(STATIC_DIR)
    PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
    print(PUBLIC_DIR)

    copycontents.copy(STATIC_DIR, PUBLIC_DIR)
main()
