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

from typing import List

import tensorflow as tf

from raicontours import Config


def create_model(cfg: Config):
    """Create autosegmentation tensorflow model"""

    image_input, masks_input = _create_inputs(cfg=cfg)

    base_model = _base_model(cfg=cfg)

    num_structures = len(cfg["structures"])
    empty_masks = tf.cast(0 * image_input[..., 0:1], dtype=tf.uint8)
    empty_masks = tf.repeat(empty_masks, num_structures, axis=-1)

    x = base_model(inputs=[image_input, empty_masks, tf.constant([False], dtype=bool)])
    starting_model = tf.keras.Model(inputs=image_input, outputs=x)

    x = base_model(inputs=[image_input, masks_input, tf.constant([True], dtype=bool)])
    dependent_model = tf.keras.Model(inputs=[image_input, masks_input], outputs=x)

    return base_model, starting_model, dependent_model


def _create_inputs(cfg: Config):
    image_input_shape = cfg["patch_dimensions"] + (len(cfg["reduce_algorithms"]),)
    image_input: tf.Tensor = tf.keras.layers.Input(shape=image_input_shape)

    num_structures = len(cfg["structures"])
    masks_input_shape = cfg["patch_dimensions"] + (num_structures,)
    masks_input: tf.Tensor = tf.keras.layers.Input(
        shape=masks_input_shape, dtype=tf.uint8
    )

    return image_input, masks_input


def _base_model(cfg: Config):
    """Create autosegmentation tensorflow model"""

    image_input, masks_input = _create_inputs(cfg=cfg)
    use_masks_flag: tf.Tensor = tf.keras.layers.Input(
        shape=(), dtype=tf.bool, batch_size=1
    )

    x: tf.Tensor = image_input
    x = _convolution(
        x=x, filters=cfg["encoding_filter_counts"][0], name="image_initial"
    )

    converted_masks_input = tf.cast(masks_input, dtype=tf.float32) / 255
    x_with_masks = x + _convolution(
        x=converted_masks_input,
        filters=cfg["encoding_filter_counts"][0],
        name="masks_initial",
    )

    x = ConditionalLayer()(inputs=[use_masks_flag, x_with_masks, x])

    x = _core(cfg=cfg, x=x)

    mask_output = tf.cast(tf.round(x * 255), dtype=tf.uint8)

    base_model = tf.keras.Model(
        inputs=[image_input, masks_input, use_masks_flag], outputs=mask_output
    )

    return base_model


class ConditionalLayer(tf.keras.layers.Layer):
    def call(self, inputs, *_args, **_kwargs):
        use_masks_flag, x_with_masks, x_without_masks = inputs
        x = tf.cond(use_masks_flag, lambda: x_with_masks, lambda: x_without_masks)

        return x


def _core(cfg: Config, x: tf.Tensor):
    skips: List[tf.Tensor] = []

    for i, filters in enumerate(cfg["encoding_filter_counts"]):
        is_last_step = i >= len(cfg["encoding_filter_counts"]) - 1

        x, skip = _encode(
            x=x,
            filters=filters,
            pool=not is_last_step,
            skip_first_convolution=i == 0,
            name_index=i,
        )

        if not is_last_step:
            skips.append(skip)

    skips.reverse()

    for i, (filters, skip) in enumerate(zip(cfg["decoding_filter_counts"], skips)):
        x = _decode(x=x, skip=skip, filters=filters, name_index=i)

    x = tf.keras.layers.Conv3D(
        filters=len(cfg["structures"]), kernel_size=1, padding="same"
    )(x)
    x = tf.keras.layers.Activation("sigmoid")(x)

    return x


def _encode(
    x: tf.Tensor,
    filters: int,
    pool: bool,
    skip_first_convolution: bool,
    name_index: int,
):
    name = f"encode_{name_index}"

    for i in range(2):
        looped_name = f"{name}_{i}"
        if skip_first_convolution and i == 0:
            pass
        else:
            x = _convolution(x=x, filters=filters, name=looped_name)

        x = _activation(x=x, name=looped_name)

    skip = x

    if pool:
        x = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2), name=f"{name}_max_pool")(
            x
        )

    return x, skip


def _decode(x: tf.Tensor, skip: tf.Tensor, filters: int, name_index: int):
    name = f"decode_{name_index}"

    x = _conv_transpose(x=x, filters=filters, name=name)
    x = _activation(x, name=name)

    x = tf.keras.layers.concatenate([skip, x], axis=-1)

    for i in range(2):
        looped_name = f"{name}_{i}"
        x = _convolution(x=x, filters=filters, name=looped_name)
        x = _activation(x=x, name=looped_name)

    return x


def _convolution(x: tf.Tensor, filters: int, name: str):
    x = tf.keras.layers.Conv3D(
        filters=filters,
        kernel_size=3,
        padding="same",
        name=f"{name}_convolution",
    )(x)

    return x


def _conv_transpose(x: tf.Tensor, filters: int, name: str):
    x = tf.keras.layers.Conv3DTranspose(
        filters=filters,
        kernel_size=3,
        strides=(2, 2, 2),
        padding="same",
        name=f"{name}_conv_transpose",
    )(x)

    return x


def _activation(x: tf.Tensor, name: str):
    x = tf.keras.layers.Activation("relu", name=f"{name}_activation")(x)

    return x
