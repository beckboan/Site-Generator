import copycontents
import os
import pagegenerator


def main():
    ROOT_DIR = os.path.abspath(os.curdir)
    print(ROOT_DIR)
    STATIC_DIR = os.path.join(ROOT_DIR, "static")
    print(STATIC_DIR)
    PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
    print(PUBLIC_DIR)

    copycontents.copycontents(STATIC_DIR, PUBLIC_DIR)

    pagegenerator.generate_page(os.path.join(ROOT_DIR, "content", "index.md"), os.path.join(ROOT_DIR, "template.html"), os.path.join(PUBLIC_DIR, "index.html"))

main()
