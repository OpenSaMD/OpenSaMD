# Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd

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
import urllib.request
from typing import Union

from rai._paths import RAI_DATA


def example_head_and_neck(
    data_dir: Union[str, pathlib.Path] = RAI_DATA / "HNSCC-01-0201"
):
    data_dir = pathlib.Path(data_dir)
    data_dir.mkdir(exist_ok=True, parents=True)

    repo_url = "https://github.com/RadiotherapyAI/data-tcia-hnscc-part-3"
    commit_hash = "9a78da8ff52d60bed629b55f1076338005732480"
    study_path = "HNSCC-01-0201/10-21-2002-RT%20SIMULATION-79781"

    download_url_root = f"{repo_url}/raw/{commit_hash}/{study_path}"

    structure_url = f"{download_url_root}/1.000000-91247/1-1.dcm"
    structure_path = data_dir / "1-1.dcm"

    image_filenames = [f"1-{item:03d}.dcm" for item in range(1, 177)]

    image_urls = [
        f"{download_url_root}/2.000000-47027/{filename}" for filename in image_filenames
    ]
    image_paths = [data_dir / filename for filename in image_filenames]

    urls_to_download = [structure_url] + image_urls
    paths_to_save_to = [structure_path] + image_paths

    processes: list[multiprocessing.Process] = []

    for url, path in zip(urls_to_download, paths_to_save_to):
        if path.exists():
            continue

        p = multiprocessing.Process(
            target=urllib.request.urlretrieve, kwargs={"url": url, "filename": path}
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    return image_paths, structure_path
