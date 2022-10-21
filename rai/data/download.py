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

import multiprocessing
import pathlib
import urllib.parse
import urllib.request
from typing import List, Union

from rai._paths import RAI_DATA


def hnscc_example(data_dir: Union[str, pathlib.Path] = RAI_DATA / "HNSCC"):
    data_dir = pathlib.Path(data_dir)

    repo = "RadiotherapyAI/data-tcia-hnscc-part-3"
    commit_hash = "9a78da8ff52d60bed629b55f1076338005732480"
    study_path = "HNSCC-01-0201/10-21-2002-RT%20SIMULATION-79781"

    relative_structure_path = "1.000000-91247/1-1.dcm"
    relative_image_paths = [
        f"2.000000-47027/1-{item:03d}.dcm" for item in range(1, 177)
    ]

    image_paths, structure_path = _github_images_and_structure_download(
        data_dir,
        repo,
        commit_hash,
        study_path,
        relative_structure_path,
        relative_image_paths,
    )

    return image_paths, structure_path


def deepmind_example(data_dir: Union[str, pathlib.Path] = RAI_DATA / "deepmind"):
    data_dir = pathlib.Path(data_dir)

    repo = "RadiotherapyAI/data-tcia-deepmind"
    commit_hash = "61fd2525f9880c8b201758f43c773e515572be92"
    study_path = "0522c0659"

    relative_structure_path = "RS.dcm"
    relative_image_paths = [f"CT-{item:03d}.dcm" for item in range(165)]

    image_paths, structure_path = _github_images_and_structure_download(
        data_dir,
        repo,
        commit_hash,
        study_path,
        relative_structure_path,
        relative_image_paths,
    )

    return image_paths, structure_path


def _github_images_and_structure_download(
    data_dir: pathlib.Path,
    repo: str,
    commit_hash: str,
    study_path: str,
    relative_structure_path: str,
    relative_image_paths: List[str],
):
    repo_url = f"https://github.com/{repo}"

    download_url_root = f"{repo_url}/raw/{commit_hash}/{study_path}"
    resolved_study_path = data_dir / urllib.parse.unquote(study_path)

    structure_url = f"{download_url_root}/{relative_structure_path}"
    structure_path = resolved_study_path / relative_structure_path

    image_urls = [f"{download_url_root}/{path}" for path in relative_image_paths]
    image_paths = [resolved_study_path / path for path in relative_image_paths]

    urls_to_download = [structure_url] + image_urls
    paths_to_save_to = [structure_path] + image_paths

    _multiprocess_download(urls_to_download, paths_to_save_to)

    return image_paths, structure_path


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
