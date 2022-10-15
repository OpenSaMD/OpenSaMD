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

from typing import List

import tensorflow as tf

from raicontours import Config


def create_model(cfg: Config):
    """Create autosegmentation tensorflow model"""

    image_input, masks_input, masks_input_shape = _create_inputs(cfg=cfg)

    base_model = _base_model(cfg=cfg)

    empty_masks = tf.broadcast_to(
        tf.cast(0 * image_input, dtype=tf.uint8), masks_input_shape
    )

    x = base_model(inputs=[image_input, empty_masks, tf.constant([False], dtype=bool)])
    starting_model = tf.keras.Model(inputs=image_input, outputs=x)

    x = base_model(inputs=[image_input, masks_input, tf.constant([True], dtype=bool)])
    dependent_model = tf.keras.Model(inputs=[image_input, masks_input], outputs=x)

    return starting_model, dependent_model


def _create_inputs(cfg: Config):
    image_input: tf.Tensor = tf.keras.layers.Input(shape=cfg["patch_dimensions"])

    num_structures = len(cfg["structures"])
    masks_input_shape = cfg["patch_dimensions"] + (num_structures,)
    masks_input: tf.Tensor = tf.keras.layers.Input(
        shape=masks_input_shape, dtype=tf.uint8
    )

    return image_input, masks_input, masks_input_shape


def _base_model(cfg: Config):
    """Create autosegmentation tensorflow model"""

    image_input, masks_input, _masks_input_shape = _create_inputs(cfg=cfg)
    use_masks_flag: tf.Tensor = tf.keras.layers.Input(
        shape=(1,), dtype=tf.bool, batch_size=1
    )

    x: tf.Tensor = image_input[..., None]
    x = _convolution(x=x, filters=cfg["encoding_filter_counts"][0])

    def _add_masks_conv(x):
        converted_masks_input = tf.cast(masks_input, dtype=tf.float32) / 255

        x = x + _convolution(
            x=converted_masks_input, filters=cfg["encoding_filter_counts"][0]
        )

        return x

    x = tf.cond(use_masks_flag, lambda: _add_masks_conv(x), lambda: x)

    x = _core(cfg=cfg, x=x)

    mask_output = tf.cast(tf.round(x * 255), dtype=tf.uint8)

    base_model = tf.keras.Model(
        inputs=[image_input, masks_input, use_masks_flag], outputs=mask_output
    )

    return base_model


def _core(cfg: Config, x: tf.Tensor):
    skips: List[tf.Tensor] = []

    for i, filters in enumerate(cfg["encoding_filter_counts"]):
        is_last_step = i >= len(cfg["encoding_filter_counts"]) - 1

        x, skip = _encode(
            x=x, filters=filters, pool=not is_last_step, skip_first_convolution=i == 0
        )

        if not is_last_step:
            skips.append(skip)

    skips.reverse()

    for filters, skip in zip(cfg["decoding_filter_counts"], skips):
        x = _decode(x=x, skip=skip, filters=filters)

    x = tf.keras.layers.Conv3D(
        filters=len(cfg["structures"]), kernel_size=1, padding="same"
    )(x)
    x = tf.keras.layers.Activation("sigmoid")(x)

    return x


def _encode(x: tf.Tensor, filters: int, pool: bool, skip_first_convolution: bool):
    for i in range(2):
        if skip_first_convolution and i == 0:
            pass
        else:
            x = _convolution(x=x, filters=filters)

        x = _activation(x=x)

    skip = x

    if pool:
        x = tf.keras.layers.MaxPooling3D(pool_size=(2, 2, 2))(x)

    return x, skip


def _decode(x: tf.Tensor, skip: tf.Tensor, filters: int):
    x = _conv_transpose(x=x, filters=filters)
    x = _activation(x)

    x = tf.keras.layers.concatenate([skip, x], axis=-1)

    for _ in range(2):
        x = _convolution(x=x, filters=filters)
        x = _activation(x=x)

    return x


def _convolution(x: tf.Tensor, filters: int):
    x = tf.keras.layers.Conv3D(filters=filters, kernel_size=3, padding="same")(x)

    return x


def _conv_transpose(x: tf.Tensor, filters: int):
    x = tf.keras.layers.Conv3DTranspose(
        filters=filters, kernel_size=3, strides=(2, 2, 2), padding="same"
    )(x)

    return x


def _activation(x: tf.Tensor):
    x = tf.keras.layers.Activation("relu")(x)

    return x
