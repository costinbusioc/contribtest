import os

from generate import *
from unittest import mock, TestCase


class TestGenerate(TestCase):

    '''
        Open three content files for testing functionalities.
    '''
    def open_content_files(self, mode):
        file1 = open('content1.txt', mode)
        file2 = open('content2.txt', mode)
        file3 = open('content3.txt', mode)

        return file1, file2, file3

    '''
    	Delete the files when the tests end.
    '''
    def delete_content_files(self):
        os.remove("content1.txt")
        os.remove("content2.txt")
        os.remove("content3.txt")

    '''
    	Create three content files for testing functionalities.
    '''
    def create_content_files(self):
        metadata = '''{"title": "Contact us!", "layout": "base.html"}
		---
		'''

        content1 = '''Write an email to contact@example.com.'''
        content2 = '''

		Write an email to contact@example.com.'''

        content3 = '''


		Write an email to contact@example.com.


		'''

        file1, file2, file3 = self.open_content_files('w')
        file1.write(metadata + content1)
        file2.write(metadata + content2)
        file3.write(metadata + content3)
        file1.close()
        file2.close()
        file3.close()

    '''
    	Check that the output folder will be created by mocking the call.
    '''
    @mock.patch('generate.generate_site')
    @mock.patch('generate.create_folder')
    def test_output_folder_created(self, create_folder_mock, generate_site_mock):
        main(None, 'my_test_output')

        assert create_folder_mock.called
        assert generate_site_mock.called

    '''
    	Check that the not relevant files (according to the rst documentation)
    	are not taken into account. If the content section starts or ends with
    	blank lines, those will be removed.
    '''
    def test_blank_lines_removed(self):
        self.create_content_files()

        file1, file2, file3 = self.open_content_files('r')

        m1, c1 = read_metadata_content(file1)
        m2, c2 = read_metadata_content(file2)
        m3, c3 = read_metadata_content(file3)

        file1.close()
        file2.close()
        file3.close()
        self.delete_content_files()

        assert c1 == c2 == c3

    '''
    	Check that if no metadata details are provided, no output file is created.
    '''
    @mock.patch('generate.write_output')
    def test_no_output_file_for_empty(self, write_output_mock):
        write_output_mock.return_value = False

        generate_site('test\\source\\unittest', None)
        assert not write_output_mock.called

    '''
    	Check that for each rst file in our current working environment,
    	a call to write the corresponding html file was made.
    '''
    @mock.patch('generate.write_output')
    def test_create_output_files(self, write_output_mock):
        write_output_mock.return_value = False

        generate_site('test\\source\\', 'output')
        assert write_output_mock.call_count == 2
