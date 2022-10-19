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


var plotlyElement = document.getElementById("{plot_id}");

var images = {
    "transverse": {},
    "coronal": {},
    "sagittal": {},
};

var updatePlaneOrientations = {
    "transverse": ["sagittal", "coronal"],
    "coronal": ["sagittal", "transverse"],
    "sagittal": ["coronal", "transverse"],
};


plotlyElement.layout.images.forEach(image => {
    var splitImageName = image.name.split("_")

    var planeOrientation = splitImageName[0]
    var sliceIndex = splitImageName[1]

    images[planeOrientation][sliceIndex] = image
});

plotlyElement.on('plotly_click', function(data){
    var point = data.points[0]
    var clickedPlaneOrientation = point.data.name

    var clickedX = point.pointIndex[1]
    var clickedY = point.pointIndex[0]

    var xUpdate = updatePlaneOrientations[clickedPlaneOrientation][0]
    var yUpdate = updatePlaneOrientations[clickedPlaneOrientation][1]

    for (var i = 0; i < Object.keys(images[xUpdate]).length; i++) {
        images[xUpdate][i].visible = false
    }
    for (var i = 0; i < Object.keys(images[yUpdate]).length; i++) {
        images[yUpdate][i].visible = false
    }

    images[xUpdate][clickedX].visible = true
    images[yUpdate][clickedY].visible = true

    Plotly.react(plotlyElement, plotlyElement.data, plotlyElement.layout)
})
