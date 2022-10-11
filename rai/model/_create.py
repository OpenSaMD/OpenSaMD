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

import tensorflow as tf

PATCH_DIMENSIONS = (64, 64, 64)
ENCODING_FILTER_COUNTS = [32, 64, 128, 256]
DECODING_FILTER_COUNTS = [128, 64, 32, 16]


def create_model(num_structures: int):
    """Create autosegmentation tensorflow model"""
    image_input: tf.Tensor = tf.keras.layers.Input(shape=PATCH_DIMENSIONS)

    x: tf.Tensor = image_input[..., None]
    x = _core(x=x, num_structures=num_structures)

    mask_output = tf.cast(tf.round(x * 255), dtype=tf.uint8)

    model = tf.keras.Model(inputs=image_input, outputs=mask_output)

    return model


def _core(x: tf.Tensor, num_structures: int):
    skips: list[tf.Tensor] = []

    for i, filters in enumerate(ENCODING_FILTER_COUNTS):
        is_last_step = i >= len(ENCODING_FILTER_COUNTS) - 1

        x, skip = _encode(x=x, filters=filters, pool=not is_last_step)

        if not is_last_step:
            skips.append(skip)

    skips.reverse()

    for filters, skip in zip(DECODING_FILTER_COUNTS, skips):
        x = _decode(x=x, skip=skip, filters=filters)

    x = tf.keras.layers.Conv3D(filters=num_structures, kernel_size=1, padding="same")(x)
    x = tf.keras.layers.Activation("sigmoid")(x)

    return x


def _encode(x: tf.Tensor, filters: int, pool: bool):
    for _ in range(2):
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
