import os
import re
import zipfile
import argparse
from collections import defaultdict
from io import BytesIO
import time
import sys
from datetime import datetime


def search_files(path, exclude_patterns):
    class_dict = defaultdict(list)

    for root, dirs, files in os.walk(path):
        if exclude_patterns:
            dirs[:] = [d for d in dirs if not any(re.match(pattern, d) for pattern in exclude_patterns)]
            files = [f for f in files if not any(re.match(pattern, f) for pattern in exclude_patterns)]

        for file in files:
            if file.endswith('.jar') or file.endswith('.war'):
                file_path = os.path.join(root, file)
                print(f'Searching in {file_path}')
                update_class_dict(file_path, class_dict)

    return class_dict

def update_class_dict(file_path, class_dict):
    def process_jar(jar_bytes, file_path):
        with zipfile.ZipFile(jar_bytes, 'r') as zfile:
            for name in zfile.namelist():
                if name.endswith('.class'):
                    class_name = name.replace('/', '.')
                    class_dict[class_name].append(file_path)
                elif name.endswith('.jar'):
                    nested_jar = BytesIO(zfile.read(name))
                    process_jar(nested_jar, f"{file_path}/{name}")

    with open(file_path, 'rb') as f:
        jar_bytes = BytesIO(f.read())

    process_jar(jar_bytes, file_path)

def generate_html_report(class_dict, template_path, output_file, execution_params, start_time):
    with open(template_path, 'r') as f:
        html_template = f.read()

    table_rows_by_class = ''
    table_rows_by_file = ''

    # Group by class
    for class_name, jar_files in class_dict.items():
        if len(jar_files) > 1:
            jar_files_list = '<br>'.join(jar_files)
            table_rows_by_class += f'<tr><td>{class_name}</td><td>{jar_files_list}</td></tr>'

    # Group by file
    file_dict = defaultdict(set)
    for class_name, jar_files in class_dict.items():
        if len(jar_files) > 1:
            for jar_file in jar_files:
                file_dict[jar_file].add(class_name)

    for file_name, classes in file_dict.items():
        class_list = '<br>'.join(classes)
        table_rows_by_file += f'<tr><td>{file_name}</td><td>{class_list}</td></tr>'

    generation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    execution_time = round(time.time() - start_time, 2)

    filled_html = html_template.replace('{table_rows_by_class}', table_rows_by_class) \
                               .replace('{table_rows_by_file}', table_rows_by_file) \
                               .replace('{generation_time}', generation_time) \
                               .replace('{execution_params}', ' '.join(execution_params)) \
                               .replace('{execution_time}', str(execution_time))

    with open(output_file, 'w') as f:
        f.write(filled_html)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the .jar and .war files containing classes in a directory.')
    parser.add_argument('--dir', required=True, help='The directory path to search in.')
    parser.add_argument('--exclude', action='append', help='A regex pattern to exclude directories/files. Can be provided multiple times.')
    parser.add_argument('--output', default='report.html', help='The output HTML report file.')
    args = parser.parse_args()

    directory_path = args.dir
    exclude_patterns = args.exclude if args.exclude else []
    output_file = args.output

    start_time = time.time()

    class_dict = search_files(directory_path, exclude_patterns)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(script_dir, 'template.html')

    generate_html_report(class_dict, template_path, output_file, sys.argv[1:], start_time)
    print(f"HTML report generated: {output_file}")

