# Undistorted Sensor Size Calculator

Use this calculator to help you get the new sensor size after you have undistorted your footage.

You can ether enter in the original resolution and sensor size or select it from the database using the lists.
Next enter the new resolution of your footage and the new sensor size will automatically be calculated for you.

### Select/Enter original information

```calculator
{
    "element": "setup",
    "code": "updateList(camera, Object.keys(db[vendor.value]));"
},
{
    "element": "function",
    "name": "sensorSizeReCalc",
    "args": [
        "value",
        "newType"
    ],
    "code": "
    if (newType == 'mm') {
        return parseFloat((value * 25.4).toFixed(3));
    } else {
        return parseFloat((value / 25.4).toFixed(3));
    }
    "
},
{
    "element": "function",
    "name": "sensorSizeTypeChange",
    "args": [],
    "code": "
    sensorX.value = sensorSizeReCalc(sensorX.value, sensorSizeType.value);
    sensorY.value = sensorSizeReCalc(sensorY.value, sensorSizeType.value);
    sensorDiagonal.value = sensorSizeReCalc(sensorDiagonal.value, sensorSizeType.value);
    newSensorX.value = sensorSizeReCalc(newSensorX.value, sensorSizeType.value);
    newSensorY.value = sensorSizeReCalc(newSensorY.value, sensorSizeType.value);
    newSensorDiagonal.value = sensorSizeReCalc(newSensorDiagonal.value, sensorSizeType.value);
    "
},
{
    "element": "function",
    "name": "calculateNewSensorSize",
    "args": [],
    "code": "
    newSensorX.value = parseFloat(((newResolutionX.value / resolutionX.value) * sensorX.value).toFixed(3));
    newSensorY.value = parseFloat(((newResolutionY.value / resolutionY.value) * sensorY.value).toFixed(3));
    newSensorDiagonal.value = parseFloat(Math.sqrt(Math.pow(newSensorX.value,
    2) + Math.pow(newSensorY.value,
    2)).toFixed(3));
    "
},
{
    "element": "group",
    "columns": 3,
    "border": true,
    "content": [
        {
            "element": "list",
            "varName": "vendor",
            "label": "Vendor",
            "generate": "return Object.keys(db);",
            "onChange": "updateList(camera, Object.keys(db[vendor.value]));"
        },
        {
            "element": "list",
            "varName": "camera",
            "label": "Camera",
            "onChange": "updateList(sensor, Object.keys(db[vendor.value][camera.value]['sensor dimensions']));"
        },
        {
            "element": "list",
            "varName": "sensor",
            "label": "Sensor",
            "onChange": "
            resolutionX.value = db[vendor.value
            ][camera.value
            ]['sensor dimensions'
            ][sensor.value
            ]['resolution'
            ]['width'
            ];

            resolutionY.value = db[vendor.value
            ][camera.value
            ]['sensor dimensions'
            ][sensor.value
            ]['resolution'
            ]['height'
            ];

            sensorX.value = db[vendor.value
            ][camera.value
            ]['sensor dimensions'
            ][sensor.value
            ][sensorSizeType.value
            ]['width'
            ];
            
            sensorY.value = db[vendor.value
            ][camera.value
            ]['sensor dimensions'
            ][sensor.value
            ][sensorSizeType.value
            ]['height'
            ];
            
            sensorDiagonal.value = db[vendor.value
            ][camera.value
            ]['sensor dimensions'
            ][sensor.value
            ][sensorSizeType.value
            ]['diagonal'
            ];

            calculateNewSensorSize();
            "
        }
    ]
},
{
    "element": "group",
    "columns": 2,
    "content": [
        {
            "element": "multi",
            "label": "Resolution",
            "content": [
                {
                    "element": "input",
                    "varName": "resolutionX",
                    "placeholder": "Width",
                    "onChange": "calculateNewSensorSize();",
                    "readOnly": false
                },
                {
                    "element": "input",
                    "varName": "resolutionY",
                    "placeholder": "Height",
                    "onChange": "calculateNewSensorSize();",
                    "prefix": "x",
                    "suffix": "px",
                    "readOnly": false
                }
            ]
        }
    ]
},
{
    "element": "multi",
    "label": "Sensor Dimensions",
    "content": [
        {
            "element": "input",
            "varName": "sensorX",
            "placeholder": "Width",
            "readOnly": false
        },
        {
            "element": "input",
            "varName": "sensorY",
            "placeholder": "Height",
            "prefix": "x",
            "readOnly": false
        },
        {
            "element": "input",
            "varName": "sensorDiagonal",
            "prefix": "Diagonal",
            "readOnly": true
        },
        {
            "element": "list",
            "varName": "sensorSizeType",
            "list": [
                "mm",
                "inches"
            ],
            "onChange": "
            newSensorSizeType.value = sensorSizeType.value;
            sensorSizeTypeChange();
            "
        }
    ]
},
{
    "element": "rules"
}
```

### Enter new information

```calculator
{
    "element": "group",
    "columns": 2,
    "content": [
        {
            "element": "multi",
            "label": "New Resolution",
            "content": [
                {
                    "element": "input",
                    "varName": "newResolutionX",
                    "placeholder": "Width",
                    "onChange": "calculateNewSensorSize();"
                },
                {
                    "element": "input",
                    "varName": "newResolutionY",
                    "placeholder": "Height",
                    "onChange": "calculateNewSensorSize();",
                    "prefix": "x",
                    "suffix": "px"
                }
            ]
        }
    ]
},
{
    "element": "multi",
    "label": "New Sensor Dimensions",
    "content": [
        {
            "element": "input",
            "varName": "newSensorX",
            "placeholder": "Width",
            "readOnly": true
        },
        {
            "element": "input",
            "varName": "newSensorY",
            "placeholder": "Height",
            "prefix": "x",
            "readOnly": true
        },
        {
            "element": "input",
            "varName": "newSensorDiagonal",
            "prefix": "Diagonal",
            "readOnly": true
        },
        {
            "element": "list",
            "varName": "newSensorSizeType",
            "list": [
                "mm",
                "inches"
            ],
            "onChange": "
            sensorSizeType.value = newSensorSizeType.value;
            sensorSizeTypeChange();
            "
        }
    ]
}
```
