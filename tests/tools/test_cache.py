import json
import os
import time

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
    cm.clear_all()


def test_clear():
    cm = CacheManager(".cache/")
    cm.clear_all()


def test_get_cm():
    @cache(key="abc1")
    def my_calc1():
        return np.random.randn(5)

    cm = get_cachemanager_for(my_calc1)
    assert cm is not None


def test_remote_cache():
    path_config = "config.json"
    if not os.path.exists(path_config):
        return

    with open(path_config, "r") as handle:
        config = json.load(handle)

    if "accesskey" not in config or len(config["accesskey"]) < 1:
        return

    accesskey = config["accesskey"]
    secretkey = config["secretkey"]
    base = config["base"]
    endpoint = config["endpoint"] if "endpoint" in config else None

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
    cm.clear_all()
