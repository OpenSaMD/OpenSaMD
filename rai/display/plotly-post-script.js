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


console.log("{plot_id}")

var plotlyElement = document.getElementById("{plot_id}");

var axisElements = {
    "transverse": plotlyElement.querySelector('.xy'),
    "coronal": plotlyElement.querySelector('.x3y3'),
    "sagittal": plotlyElement.querySelector('.x4y4'),
}

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
    // var structureName = splitScatterName[1];
    var sliceIndex = splitScatterName[2];
    // var contourIndex = splitScatterName[3];

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

var currentSliceIndices = {
    "transverse": null,
    "coronal": null,
    "sagittal": null,
}

var planeOrientation = ["transverse", "coronal", "sagittal"]

planeOrientation.forEach(planeOrientation => {
    images[planeOrientation].forEach((image, index) => {
        if (image.visible) {
            currentSliceIndices[planeOrientation] = index;
        }
    });
});

console.log(currentSliceIndices)

var numSlices = {
    "transverse": images["transverse"].length,
    "coronal": images["coronal"].length,
    "sagittal": images["sagittal"].length,
}

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

    // TODO: Look into race conditions resulting from this approach.
    currentSliceIndices[planeOrientation] = null
};


function setOrientationIndexVisibleTrue(planeOrientation, index) {
    images[planeOrientation][index].visible = true

    var contours = contourTraces[planeOrientation][index]

    if (contours !== undefined) {
        contours.forEach(contourTrace => {
            contourTrace.visible = true;
        });
    }

    currentSliceIndices[planeOrientation] = index;
};


// https://www.freecodecamp.org/news/javascript-debounce-example/
function debounce(func, timeout = 50){
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

function plotlyFigureUpdate(){
    Plotly.react(plotlyElement, plotlyElement.data, plotlyElement.layout);
}
const plotlyDebouncedFigureUpdate = debounce(() => plotlyFigureUpdate());


planeOrientation.forEach(planeOrientation => {
    var axisElement = axisElements[planeOrientation];

    axisElement.addEventListener('wheel', event => {
        event.preventDefault();

        var direction = Math.sign(event.deltaY);

        var newSliceIndex = currentSliceIndices[planeOrientation] + direction
        if (newSliceIndex < 0) {
            newSliceIndex = 0;
        } else if (newSliceIndex > numSlices[planeOrientation]) {
            newSliceIndex = numSlices[planeOrientation];
        }

        setOrientationVisibleFalse(planeOrientation);
        setOrientationIndexVisibleTrue(planeOrientation, newSliceIndex);

        plotlyDebouncedFigureUpdate()
    })
});
