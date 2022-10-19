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
var transverseElement = plotlyElement.querySelector('.xy')
var coronalElement = plotlyElement.querySelector('.x3y3')
var sagittalElement = plotlyElement.querySelector('.x4y4')

var images = {
    "transverse": [],
    "coronal": [],
    "sagittal": [],
};

plotlyElement.layout.images.forEach(image => {
    var splitImageName = image.name.split("_")

    var planeOrientation = splitImageName[0]
    var sliceIndex = splitImageName[1]

    images[planeOrientation][sliceIndex] = image
});

var contourTraces = {
    "transverse": [],
    "coronal": [],
    "sagittal": [],
};

plotlyElement.data.forEach(trace => {
    if (trace.type !== "scatter") {
        return;
    }

    var splitScatterName = trace.name.split(",");

    var planeOrientation = splitScatterName[0];
    var structureName = splitScatterName[1];
    var sliceIndex = splitScatterName[2];
    var contourIndex = splitScatterName[3];

    if (contourTraces[planeOrientation][sliceIndex] === undefined) {
        contourTraces[planeOrientation][sliceIndex] = [trace];
    } else {
        contourTraces[planeOrientation][sliceIndex].push(trace)
    }
});

var updatePlaneOrientations = {
    "transverse": ["sagittal", "coronal"],
    "coronal": ["sagittal", "transverse"],
    "sagittal": ["coronal", "transverse"],
};

plotlyElement.on('plotly_click', function(data){
    var point = data.points[0]
    var clickedPlaneOrientation = point.data.name

    var clickedX = point.pointIndex[1]
    var clickedY = point.pointIndex[0]

    var xUpdate = updatePlaneOrientations[clickedPlaneOrientation][0]
    var yUpdate = updatePlaneOrientations[clickedPlaneOrientation][1]

    setOrientationVisibleFalse(xUpdate)
    setOrientationVisibleFalse(yUpdate)

    setOrientationIndexVisibleTrue(xUpdate, clickedX)
    setOrientationIndexVisibleTrue(yUpdate, clickedY)

    Plotly.react(plotlyElement, plotlyElement.data, plotlyElement.layout)
});

function setOrientationVisibleFalse(planeOrientation) {
    images[planeOrientation].forEach(image => {
        image.visible = false;
    });

    contourTraces[planeOrientation].forEach(contours => {
        contours.forEach(contourTrace => {
            contourTrace.visible = false;
        });
    });
};


function setOrientationIndexVisibleTrue(planeOrientation, index) {
    images[planeOrientation][index].visible = true

    var contours = contourTraces[planeOrientation][index]

    if (contours !== undefined) {
        contours.forEach(contourTrace => {
            contourTrace.visible = true;
        });
    }

};


transverseElement.addEventListener('wheel', (event) => {
    event.preventDefault()
    console.log(event)
})

coronalElement.addEventListener('wheel', (event) => {
    event.preventDefault()
    console.log(event)
})

sagittalElement.addEventListener('wheel', (event) => {
    event.preventDefault()
    console.log(event)
})
