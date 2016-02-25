from django.core.exceptions import ObjectDoesNotExist
from lmblife.settings import (AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_DEFAULT_SITE, AWS_BUCKET_USER_ARCHIVE, )
from boto.s3.connection import S3Connection, Key
from django.core.files.base import ContentFile
from datetime import datetime
import mimetypes


def make_org_s3_initial_directory_names(university_name, university_id):
    org_root = '{}_{}_root/'.format(university_name, university_id)
    org_wiki_root = '{}{}_{}_wiki/'.format(org_root, university_name, university_id)
    org_image_root = '{}{}_{}_image/'.format(org_root, university_name, university_id)
    return dict({'org_wiki_root': org_wiki_root, 'org_image_root': org_image_root, })


def make_image_filename(key_prefix, file_extension):
    """
        For now, append timestamp only for image file name, because article name is unique
        :param file_extension: file extension
        :return: return file name with timestamp as suffix
    """
    if file_extension:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        filename = 'image_' + timestamp + '.' + file_extension
        return key_prefix + filename
    else:
        raise Exception('invalid image file type !')


def make_org_bucket_name(university):
    return university.university_name + '-' + university.pk


def make_feature_name(feature):
    return 'feature_' + feature.feature_name


def make_post_name():
    pass    # TODO : implement this after post model done


class S3Storage:
    def __init__(self, bucket_name=None):
        self.connection = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
        self.bucket = self.get_bucket(bucket_name)

    def is_file_exist(self, key_name):
        if self.bucket.get_key(key_name):
            return True
        return False

    def upload_validator(self, key_name, is_new):
        if is_new and self.is_file_exist(key_name):
            raise Exception('key %s already exist !' % key_name)
        return True

    def get_bucket(self, bucket_name=None):
        if not bucket_name:
            return None
        self.bucket = self.connection.lookup(bucket_name)
        if not self.bucket:
            raise ObjectDoesNotExist('Bucket : %s Does not exist !' % bucket_name)
        return self.bucket

    def get_default_site_bucket(self):
        """
        Get LMB default bucket
        """
        return self.get_bucket(AWS_BUCKET_DEFAULT_SITE)

    def get_user_bucket(self):
        """
        Get Customer bucket
        """
        return self.get_bucket(AWS_BUCKET_USER_ARCHIVE)

    def get_sub_keys(self, prefix, suffix='/', marker=''):
        """
        List all specific keys by prefix, default only for one level
        :param prefix: key prefix
        :param suffix: default '/' means only one level
        :param marker: for paging usage
        :return: a list of keys that handles paging
        """
        keys = self.bucket.list(prefix=prefix, delimiter=suffix, marker=marker)
        key_name_list = [key_name.name for key_name in keys]
        return key_name_list

    def get_sub_keys_with_spec(self, prefix, spec=None, suffix='/', marker=''):
        """
        Call get_sub_keys() and loop to check if list of keys end with specific string
        :param prefix:
        :param spec: Type: String, check keys if end with specific string
        :param suffix:
        :param marker:
        :return: list of Key Prefix objects, None if request key does not exist
        """
        key_list = self.get_sub_keys(prefix, suffix, marker)
        if not spec:
            return key_list
        result_key_list = []
        for key in key_list:
            if str(key.name).endswith(spec):
                result_key_list.append(key)
        return result_key_list

    def _upload_file(self, file, key_name, content_type, is_wiki=False):
        new_key = self.bucket.new_key(key_name)
        new_key.set_metadata('Content-Type', content_type)
        if is_wiki:
            new_key.set_contents_from_string(file)
        else:
            new_key.set_contents_from_file(file)

    def upload_image(self, file, key_prefix):
        # fixme : check key_prefix end with '/'
        filename = str(file)
        content_type = mimetypes.guess_type(filename)[0]
        # check if file is image
        if content_type:
            (file_type, file_extension) = str(content_type).split('/')
            if file_type == 'image':
                key_name = make_image_filename(key_prefix, file_extension)
                self._upload_file(file, key_name, content_type)
                return key_name
        else:
            raise Exception('Invalid file type : Not a image!')

    def upload_wiki(self, file, new_key, old_key=None):
        """
        Failed to save if:
            1. old_key is None and new_key already exist
            2. old_key has value and old_key not equals to new_key and new_key already exist
        """
        if (old_key is None or (old_key and old_key != new_key)) and self.is_file_exist(new_key):
            return None
        if old_key and self.is_file_exist(old_key):
            self.delete_file(old_key)
        self._upload_file(file, new_key, 'text/plain', True)
        return new_key

    def download_file_as_string(self, key_name):
        target_key = self.bucket.get_key(key_name)
        if target_key is not None:
            return target_key.get_contents_as_string()
        return None

    def download_file_as_file(self, key_name):
        file_content = self.download_file_as_string(key_name)
        if file_content is not None:
            return ContentFile(file_content)
        return None

    def delete_file(self, key_name):
        target_key = self.bucket.get_key(key_name)
        if target_key:
            target_key.delete()

    def create_bucket(self, bucket_name):
        # return new created bucket
        return self.connection.create_bucket(bucket_name)
