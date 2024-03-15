import os
import shutil
from markdown_blocks import markdown_to_html_node
# from pathlib import Path

dir_path_content = "./content"
template_path = "./template.html"
dir_path_static = "./static"
dir_path_public = "./public"


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path):
            if filename.endswith('.md'):
                # Generate the corresponding HTML file
                dest_path = os.path.join(dest_dir_path, filename.replace('.md', '.html'))
                generate_page(from_path, template_path, dest_path)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, filename)
            os.makedirs(new_dest_dir_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, new_dest_dir_path)

# def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
#     for filename in os.listdir(dir_path_content):
#         from_path = os.path.join(dir_path_content, filename)
#         dest_path = os.path.join(dest_dir_path, filename)
#         if os.path.isfile(from_path):
#             dest_path = Path(dest_path).with_suffix(".html")
#             generate_page(from_path, template_path, dest_path)
#         else:
#             generate_pages_recursive(from_path, template_path, dest_path)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")

def main():
    print("Deleting public dir...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public dir...")
    copy_files_recursive(dir_path_static, dir_path_public)
    print("Generating page...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )


main()
