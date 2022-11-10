# RAi, machine learning solutions in radiotherapy
# Copyright (C) 2021-2022 Radiotherapy AI Holdings Pty Ltd

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Example data download utilities"""

import multiprocessing
import pathlib
import urllib.parse
import urllib.request
from typing import List, NamedTuple, Union

from rai._paths import RAI_DATA


class DownloadedExamplePaths(NamedTuple):
    """The paths returned by each of the example download functions."""

    image_paths: List[pathlib.Path]
    structure_path: pathlib.Path
    data_license_path: pathlib.Path
    data_readme_path: pathlib.Path
    rai_license_path: pathlib.Path


def lctsc_example(
    data_dir: Union[str, pathlib.Path] = RAI_DATA / "LCTSC"
) -> DownloadedExamplePaths:
    """Downloads an example dataset from the 2017 Lung CT Segmentation
    Challenge.

    <https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=24284539>

    Parameters
    ----------
    data_dir : Union[str, pathlib.Path], optional
        The directory used for downloading the data.

    Returns
    -------
    image_paths: List[pathlib.Path]
    structure_path: pathlib.Path
    data_license_path: pathlib.Path
    data_readme_path: pathlib.Path
    rai_license_path: pathlib.Path

    """
    data_dir = pathlib.Path(data_dir)

    repo = "RadiotherapyAI/data-tcia-lctsc"
    commit_hash = "641f0a5d17e62e7a5fa63452d62aaeb22b91fc22"
    study_path = "LCTSC-Test-S3-102/11-08-2004-LEFT%20LUNG-11520"

    relative_structure_path = "1.000000-.simplified-02503/1-1.dcm"
    relative_image_paths = [
        f"1.000000-95635/1-{item:03d}.dcm" for item in range(1, 211)
    ]

    license_filename = "LICENSE"
    readme_filename = "README.md"

    return _github_images_and_structure_download(
        data_dir,
        repo,
        commit_hash,
        study_path,
        relative_structure_path,
        relative_image_paths,
        license_filename,
        readme_filename,
    )


def hnscc_example(
    data_dir: Union[str, pathlib.Path] = RAI_DATA / "HNSCC"
) -> DownloadedExamplePaths:
    """Downloads an example dataset from the TCIA HNSCC dataset.

    <https://wiki.cancerimagingarchive.net/display/Public/HNSCC>

    Parameters
    ----------
    data_dir : Union[str, pathlib.Path], optional
        The directory used for downloading the data.

    Returns
    -------
    image_paths: List[pathlib.Path]
    structure_path: pathlib.Path
    data_license_path: pathlib.Path
    data_readme_path: pathlib.Path
    rai_license_path: pathlib.Path

    """
    data_dir = pathlib.Path(data_dir)

    repo = "RadiotherapyAI/data-tcia-hnscc-part-3"
    commit_hash = "9a78da8ff52d60bed629b55f1076338005732480"
    study_path = "HNSCC-01-0201/10-21-2002-RT%20SIMULATION-79781"

    relative_structure_path = "1.000000-91247/1-1.dcm"
    relative_image_paths = [
        f"2.000000-47027/1-{item:03d}.dcm" for item in range(1, 177)
    ]

    license_filename = "license.html"
    readme_filename = "README.md"

    return _github_images_and_structure_download(
        data_dir,
        repo,
        commit_hash,
        study_path,
        relative_structure_path,
        relative_image_paths,
        license_filename,
        readme_filename,
    )


def deepmind_example(
    data_dir: Union[str, pathlib.Path] = RAI_DATA / "deepmind"
) -> DownloadedExamplePaths:
    """Downloads an example dataset from the deepmind dataset.

    <https://github.com/deepmind/tcia-ct-scan-dataset>

    Parameters
    ----------
    data_dir : Union[str, pathlib.Path], optional
        The directory used for downloading the data.

    Returns
    -------
    image_paths: List[pathlib.Path]
    structure_path: pathlib.Path
    data_license_path: pathlib.Path
    data_readme_path: pathlib.Path
    rai_license_path: pathlib.Path

    """
    data_dir = pathlib.Path(data_dir)

    repo = "RadiotherapyAI/data-tcia-deepmind"
    commit_hash = "61fd2525f9880c8b201758f43c773e515572be92"
    study_path = "0522c0659"

    relative_structure_path = "RS.dcm"
    relative_image_paths = [f"CT-{item:03d}.dcm" for item in range(165)]

    license_filename = "LICENSE"
    readme_filename = "README.md"

    return _github_images_and_structure_download(
        data_dir,
        repo,
        commit_hash,
        study_path,
        relative_structure_path,
        relative_image_paths,
        license_filename,
        readme_filename,
    )


def _github_images_and_structure_download(
    data_dir: pathlib.Path,
    repo: str,
    commit_hash: str,
    study_path: str,
    relative_structure_path: str,
    relative_image_paths: List[str],
    license_filename: str,
    readme_filename: str,
):
    repo_url = f"https://github.com/{repo}"

    download_url_root = f"{repo_url}/raw/{commit_hash}"
    license_url = f"{download_url_root}/{license_filename}"
    readme_url = f"{download_url_root}/{readme_filename}"
    data_license_path = data_dir / license_filename
    data_readme_path = data_dir / readme_filename

    study_url_root = f"{download_url_root}/{study_path}"
    resolved_study_path = data_dir / urllib.parse.unquote(study_path)

    structure_url = f"{study_url_root}/{relative_structure_path}"
    structure_path = resolved_study_path / relative_structure_path

    image_urls = [f"{study_url_root}/{path}" for path in relative_image_paths]
    image_paths = [resolved_study_path / path for path in relative_image_paths]

    rai_license_path = RAI_DATA / "LICENSE"
    rai_license_url = (
        "https://raw.githubusercontent.com/RadiotherapyAI/rai/main/LICENSE"
    )

    urls_to_download = [
        structure_url,
        license_url,
        readme_url,
        rai_license_url,
    ] + image_urls
    paths_to_save_to = [
        structure_path,
        data_license_path,
        data_readme_path,
        rai_license_path,
    ] + image_paths

    _multiprocess_download(urls_to_download, paths_to_save_to)

    return DownloadedExamplePaths(
        image_paths,
        structure_path,
        data_license_path,
        data_readme_path,
        rai_license_path,
    )


def _multiprocess_download(
    urls_to_download: List[str], paths_to_save_to: List[pathlib.Path]
):
    processes: List[multiprocessing.Process] = []

    for url, path in zip(urls_to_download, paths_to_save_to):
        # TODO: Utilise stored hashes to verify
        if path.exists():
            continue

        path.parent.mkdir(exist_ok=True, parents=True)

        p = multiprocessing.Process(
            target=urllib.request.urlretrieve, kwargs={"url": url, "filename": path}
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
