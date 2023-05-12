import os
import zipfile
import argparse
from collections import defaultdict
import json

def find_duplicate_classes(directory):
    jar_dict = defaultdict(lambda: {"classes": set(), "paths": set()})

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jar'):
                file_path = os.path.join(root, file)
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for name in zip_ref.namelist():
                        if name.endswith('.class'):
                            class_name = name.replace('/', '.').replace('.class', '')
                            jar_dict[file]["classes"].add(class_name)
                            jar_dict[file]["paths"].add(file_path)

    duplicate_jars = {jar_file: details for jar_file, details in jar_dict.items() if len(details["classes"]) > 1}
    return duplicate_jars

def generate_html_report(duplicate_jars, output_file):
    total_jars = len(duplicate_jars)
    total_classes = sum(len(details["classes"]) for details in duplicate_jars.values())
    total_jars_with_duplicates = len(duplicate_jars)

    summary = f"Total analyzed JARs: {total_jars}<br>" \
              f"Total analyzed classes: {total_classes}<br>" \
              f"Total JARs with some duplicated classes: {total_jars_with_duplicates}"

    if not duplicate_jars:
        table_rows = "<tr><td colspan='3'>No duplicate classes found.</td></tr>"
    else:
        table_rows = ""
        for jar_file, details in duplicate_jars.items():
            classes = "<br>".join(details["classes"])
            paths = "<br>".join(details["paths"])
            table_rows += f"""
            <tr>
                <td>{jar_file}</td>
                <td>{classes}</td>
                <td>{paths}</td>
            </tr>
            """

    with open("template.html", "r") as f:
        html_template = f.read()

    filled_template = html_template.replace("{summary}", summary).replace("{table_rows}", table_rows)

    with open(output_file, "w") as f:
        f.write(filled_template)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Find duplicate classes in JAR files.')
parser.add_argument('--dir', required=True, help='The directory path containing JAR files.')
parser.add_argument('--output', default='report.html', help='The output HTML report file.')
args = parser.parse_args()

# Generate HTML report
directory_path = args.dir
output_file = args.output

duplicate_jars = find_duplicate_classes(directory_path)
generate_html_report(duplicate_jars, output_file)
