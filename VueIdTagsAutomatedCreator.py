import os
import re
import uuid
import shutil

def add_unique_id(html_string):
    def replace_tag(match):
        tag = match.group(0)
        if 'id=' not in tag and 'id =' not in tag:
            unique_id = str(uuid.uuid4())
            if tag.endswith('/>'):
                return tag[:-2] + f' id="{match.group(2)}_{unique_id}"/>'
            else:
                return tag[:-1] + f' id="{match.group(2)}_{unique_id}">'
        return tag

    pattern = re.compile(r'(<)(\w+)([^>])*?>')
    modified_html = re.sub(pattern, replace_tag, html_string)
    return modified_html

def main():
    project_path = os.walk(r'src/')
    output_dir = 'src_updated/'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for path, subdirs, files in project_path:
        path = path + '/'
        # print(path, subdirs, files)
        if not os.path.exists(output_dir + path):
            os.mkdir(output_dir + path)
        for filename in files:
            input_file_path = path + filename
            output_file_path = output_dir + path + filename
            if filename.endswith('.vue'):
                # print(path + '/' + vuefile)
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    file_content = file_content.replace('=>', '||||')
                modified_html = add_unique_id(file_content)
                modified_html = modified_html.replace('||||', '=>')
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(modified_html)
                print(f"ID tags added to vue file: {output_file_path}")
            else:
                shutil.copy(input_file_path, output_file_path)
if __name__ == '__main__':
    main()