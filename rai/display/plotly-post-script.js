// Copyright (C) 2022 Radiotherapy AI Holdings Pty Ltd

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.


var plot_element = document.getElementById("{plot_id}");

console.log("{plot_id}")

var arrayLength = plot_element.layout.images.length;
var imageIndices = {
    "transverse": {},
    "coronal": {},
    "sagittal": {},
}

var updatePlaneOrientations = {
    "transverse": ["sagittal", "coronal"],
    "coronal": ["sagittal", "transverse"],
    "sagittal": ["coronal", "transverse"],
}

for (var i = 0; i < arrayLength; i++) {
    var image = plot_element.layout.images[i]
    var splitImageName = image.name.split("_")

    var planeOrientation = splitImageName[0]
    var sliceIndex = splitImageName[1]

    imageIndices[planeOrientation][sliceIndex] = i
}

plot_element.on('plotly_click', function(data){
    var point = data.points[0]
    var clickedPlaneOrientation = point.data.name

    var clickedX = point.pointIndex[1]
    var clickedY = point.pointIndex[0]

    var xUpdate = updatePlaneOrientations[clickedPlaneOrientation][0]
    var yUpdate = updatePlaneOrientations[clickedPlaneOrientation][1]

    var imageIndex

    for (var i = 0; i < Object.keys(imageIndices[xUpdate]).length; i++) {
        imageIndex = imageIndices[xUpdate][i]
        plot_element.layout.images[imageIndex].visible = false
    }
    for (var i = 0; i < Object.keys(imageIndices[yUpdate]).length; i++) {
        imageIndex = imageIndices[yUpdate][i]
        plot_element.layout.images[imageIndex].visible = false
    }

    imageIndex = imageIndices[xUpdate][clickedX]
    plot_element.layout.images[imageIndex].visible = true

    imageIndex = imageIndices[yUpdate][clickedY]
    plot_element.layout.images[imageIndex].visible = true

    Plotly.react(plot_element, plot_element.data, plot_element.layout)
})
