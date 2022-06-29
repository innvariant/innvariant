import os
import uuid

from unittest.mock import patch

import pytest

from innvariant.tools import CacheManager


def test_instantiate():
    path_base = f"test-base-path-{str(uuid.uuid4())}"
    CacheManager(path_base)


def side_effect_raise_permission_error(path):
    raise PermissionError("Access Denied.")


@patch("s3fs.S3FileSystem.open", side_effect=open)
@patch("s3fs.S3FileSystem.ls", side_effect=os.listdir)
@patch("s3fs.S3FileSystem.exists", side_effect=os.path.exists)
def test_instantiate_with_s3fs_success(mock_s3fs_exists, mock_s3fs_ls, mock_s3fs_open):
    uid = str(uuid.uuid4())
    path_base_local = f"fixtures/local/test-base-path-{uid}"
    path_base_remote = f"fixtures/remote/test-base-path-{uid}"
    os.makedirs(path_base_remote)

    CacheManager(
        path_base_local,
        access_key="my-key",
        secret_key="my-secret",
        path_remote_base=path_base_remote,
        endpoint="http://localhost/",
    )

    os.removedirs(path_base_local)
    os.removedirs(path_base_remote)


@patch("s3fs.S3FileSystem.open", side_effect=open)
@patch("s3fs.S3FileSystem.ls", side_effect=side_effect_raise_permission_error)
def test_instantiate_with_s3fs_without_permission(mock_s3fs_ls, mock_s3fs_open):
    uid = str(uuid.uuid4())
    path_base_local = f"fixtures/local/test-base-path-{uid}"
    path_base_remote = f"fixtures/remote/test-base-path-{uid}"
    os.makedirs(path_base_remote)

    with pytest.warns(UserWarning) as recorded_warnings:
        CacheManager(
            path_base_local,
            access_key="my-key",
            secret_key="my-secret",
            path_remote_base=path_base_remote,
            endpoint="http://localhost/",
        )

    assert "Access Denied" in str(recorded_warnings[0].message)

    os.removedirs(path_base_local)
    os.removedirs(path_base_remote)
