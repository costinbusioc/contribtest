# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import sys
import json
import logging

from jinja2 import FileSystemLoader, Environment

log = logging.getLogger(__name__)


'''
    Creates a directory if it doesn't exist.
    In case the output will need to be written in a new directory,
    that directory needs to be created.

    @input: folder_name
    @return: -
'''
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
        except:
            print('Can not create output folder')
            sys.exit()


'''
    Provides the .rst files paths in the current directory that can be used
    in order to generate html files.

    @input: current directory
    @output: path to the .rst files
'''
def list_files(input_folder):
    for name in os.listdir(input_folder):
        base, ext = os.path.splitext(name)

        # Check for right file extension
        if ext != '.rst':
            continue

        yield os.path.join(input_folder, name)


'''
    Reads an rst file and provides the metadata and content for the
    curent file.

    @input: path to file
    @output: metadata, content
'''
def read_metadata_content(input_file):
    # Build metadata json object
    raw_metadata = ""
    metadata = None

    for line in input_file:

        # End of metadata details found, content starts with the next line
        if line.strip() == '---':

            # If no metadata processed, return a blank json object
            metadata = json.loads(raw_metadata) if raw_metadata else None
            break

        raw_metadata += line

    # Build content string
    content = ""
    for line in input_file:
        content += line

    # Blank lines are not relevant in rst files
    content = content.strip()

    return metadata, content


'''
    Open file by accessing the path to the file and returns
    the metadata and the content

    @input: file_path
    @output: metadata, content
'''
def read_rst_file(file_path):
    with open(file_path, 'r') as f:
        return read_metadata_content(f)


'''
    Write html page to a file.

    @input: output_file, html code
    @return: -
'''
def write_output(output_file, html):
    with open(output_file, "w") as f:
        f.write(html)


'''
    Generate website from static files.
    
    @input: directory where the website is stored
    @output: -
'''
def generate_site(input_folder, output_folder):
    log.info("Generating site from %r", input_folder)

    # Create the jinja2 environment from the html files stored locally
    jinja_env = Environment(loader=FileSystemLoader(input_folder + 'layout'),
                            lstrip_blocks=True, trim_blocks=True)

    for file_path in list_files(input_folder):

        # Process current file and obtain the needed template
        metadata, content = read_rst_file(file_path)
        if metadata is None:
            continue

        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)

        # Render data using the template
        data = dict(metadata, content=content)
        html = template.render(data)

        # Write the result in an html file
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = os.path.join(output_folder, file_name + '.html')
        write_output(output_file, html)
        log.info("Writing %r with template %r", file_name, template_name)


def main(input_folder, output_folder):
    create_folder(output_folder)
    generate_site(input_folder, output_folder)


if __name__ == '__main__':
    logging.basicConfig()

    if len(sys.argv) < 3:
        print("Run like this: ./generate.py test/source output")
        sys.exit()

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    main(input_folder, output_folder)
