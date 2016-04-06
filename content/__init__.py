import os
from content.s3_storage import S3Storage as S3, make_org_s3_initial_directory_names
from content.lmb_cache import LMBCache as Cache
from lmblife.settings import AWS_BUCKET_ORG_WIKI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_TEMPLATE_ROOT = os.path.join(BASE_DIR, 'templates/wiki')
