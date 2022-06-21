import hashlib
import json
import marshal
import os
import shutil
import time

import pandas as pd


def calculate_or_cache(
    fn_calculate,
    force_calc=False,
    clear_cache=False,
    path_base_cache="~/.cache/analysisnotebook/",
):
    assert callable(fn_calculate)
    name_calculation = fn_calculate.__name__
    name_cache_meta = "cache-meta.json"
    bytes_calculation = marshal.dumps(fn_calculate.__code__)
    m = hashlib.sha256()
    m.update(bytes_calculation)
    code_calculation = m.hexdigest()

    res = None

    path_base_cache = os.path.join(
        os.path.expanduser(path_base_cache), name_calculation
    )
    path_meta = os.path.join(path_base_cache, name_cache_meta)
    if not os.path.exists(path_base_cache):
        os.makedirs(path_base_cache)
    elif not force_calc and os.path.exists(path_meta):
        meta_full = None
        with open(path_meta) as handle_meta:
            meta_full = json.load(handle_meta)

        meta = None
        if "caches" in meta_full:
            for cache in meta_full["caches"]:
                if cache["code_calculation"] == code_calculation:
                    meta = cache

        if meta is not None and "format" in meta and "keys" in meta:
            print(f"Cache hit for {name_calculation}")
            path_hd5 = os.path.join(path_base_cache, meta["path"])
            if meta["format"] == "single":
                res = pd.read_hdf(path_hd5, key=meta["keys"])
            elif meta["format"] == "list":
                res = [pd.read_hdf(path_hd5, key=k) for k in meta["keys"]]
            elif meta["format"] == "dict":
                res = {
                    meta["keys"][k_hash]: pd.read_hdf(path_hd5, key=k_hash)
                    for k_hash in meta["keys"]
                }

    if clear_cache:
        shutil.rmtree(path_base_cache)

    if res is None:
        # (Re-)calculate result
        time_calc_start = time.time()
        res = fn_calculate()
        time_calc_end = time.time()

        if clear_cache:
            return res

        format_res = (
            "single"
            if isinstance(res, pd.DataFrame)
            else "list"
            if type(res) == list
            else "dict"
            if type(res) == dict
            else "unknown"
        )

        # "main" if format_res == "single" else [i for i in enumerate(res)] if format_res == "list" else [k for k in res.keys()] if format_res == "dict" else None
        name_hd5 = "result_cache.hd5"
        path_hd5 = os.path.join(path_base_cache, name_hd5)
        res_keys = None
        if format_res == "single":
            res_keys = "main"
            res.to_hdf(path_hd5, key=res_keys)
        elif format_res == "list":
            res_keys = [i for i in enumerate(res)]
            for k, df in zip(res_keys, res):
                df.to_hdf(path_hd5, key=k)
        elif format_res == "dict":
            res_keys = {
                "key" + hashlib.sha256(str.encode(k)).hexdigest(): k for k in res.keys()
            }
            for k_hash in res_keys:
                k = res_keys[k_hash]
                res[k].to_hdf(path_hd5, key=k_hash)

        # Store cache
        meta_info = {
            "version": 1.0,
            "code_calculation": code_calculation,
            "timings": {
                "cache_creation": time.time(),
                "calc_start": time_calc_start,
                "calc_end": time_calc_end,
            },
            "format": format_res,
            "path": name_hd5,
            "keys": res_keys,
        }

        meta = {}
        if os.path.exists(path_meta):
            with open(path_meta) as handle_meta:
                meta = json.load(handle_meta)
        if "caches" not in meta:
            meta["caches"] = []
        meta["caches"].append(meta_info)
        with open(path_meta, "w+") as handle_write_meta:
            json.dump(meta, handle_write_meta)

    return res
