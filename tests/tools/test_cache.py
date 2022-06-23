import json
import os
import time
import warnings

import numpy as np

from innvariant.tools import CacheManager
from innvariant.tools import cache
from innvariant.tools import get_cachemanager_for


def test_dev():
    @cache(key="abc1")
    def my_calc1():
        return np.random.randn(5)

    @cache(key="abc2")
    def my_calc2(n: int):
        return np.random.randn(n)

    my_calc1()
    my_calc1()
    my_calc2(3)
    my_calc1()
    my_calc2(6)
    my_calc2(3)

    # Create initial cache
    start_first = time.time()
    for _ in range(100):
        my_calc2(_)
    end_first = time.time()

    # Access a second time
    start_second = time.time()
    for _ in range(100):
        my_calc2(_)
    end_second = time.time()

    assert end_first - start_first > end_second - start_second

    cm = get_cachemanager_for(my_calc1)
    cm.clear_local()


def test_clear():
    cm = CacheManager(".cache/")
    cm.clear_local()


def test_get_cm():
    @cache(key="abc1")
    def my_calc1():
        return np.random.randn(5)

    cm = get_cachemanager_for(my_calc1)
    assert cm is not None


def prepare_remote_test():
    path_config = "config.json"
    if not os.path.exists(path_config):
        warnings.warn("No test configuration file for S3FS found.")
        return None, None, None, None

    with open(path_config, "r") as handle:
        config = json.load(handle)

    if "accesskey" not in config or len(config["accesskey"]) < 1:
        warnings.warn("No valid configuration for S3FS found.")
        return None, None, None, None

    accesskey = config["accesskey"]
    secretkey = config["secretkey"]
    base = config["base"]
    endpoint = config["endpoint"] if "endpoint" in config else None

    return accesskey, secretkey, base, endpoint


def test_remote_cache():
    accesskey, secretkey, base, endpoint = prepare_remote_test()
    if accesskey is None:
        return

    @cache(
        key="abc1",
        s3_base=base,
        s3_access_key=accesskey,
        s3_secret_key=secretkey,
        s3_endpoint=endpoint,
    )
    def my_calc1():
        return np.random.randn(5)

    @cache(
        key="abc2",
        s3_base=base,
        s3_access_key=accesskey,
        s3_secret_key=secretkey,
        s3_endpoint=endpoint,
    )
    def my_calc2(n: int):
        return np.random.randn(n)

    my_calc1()
    my_calc1()
    my_calc2(3)
    my_calc1()
    my_calc2(6)

    cm = get_cachemanager_for(my_calc1)
    cm.clear_local()


def test_remote_clear_cache():
    accesskey, secretkey, base, endpoint = prepare_remote_test()
    if accesskey is None:
        return

    @cache(
        key="test_remote_clear_cache",
        s3_base=base,
        s3_access_key=accesskey,
        s3_secret_key=secretkey,
        s3_endpoint=endpoint,
    )
    def test_remote_clear_cache():
        return np.random.randn(5)

    test_remote_clear_cache()

    cm = get_cachemanager_for(test_remote_clear_cache)
    cm.clear_s3()
