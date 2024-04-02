import copycontents
import os
import pagegenerator


def main():
    ROOT_DIR = os.path.abspath(os.curdir)
    STATIC_DIR = os.path.join(ROOT_DIR, "static")
    PUBLIC_DIR = os.path.join(ROOT_DIR, "public")

    copycontents.copycontents(STATIC_DIR, PUBLIC_DIR)
    template_path = os.path.join(ROOT_DIR, "template.html")

    pagegenerator.generate_pages_recursive(os.path.join(ROOT_DIR, "content"), template_path, PUBLIC_DIR)

main()