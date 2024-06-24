# Camera Sensor Database

A collection of camera sensor information.

To quickly view the data, go to docs page:
<https://emberlightvfx.github.io/Camera-Sensor-Database/>

## Structure

```cmd
Vendor
└─── Camera
     ├─── Info
     │    └─── Other
     └─── Sensor Dimensions
          ├─── Focal Length (optional)
          ├─── Resolution
          │    ├─── Height
          │    └─── Width
          ├─── mm
          │    ├─── Height
          │    ├─── Width
          │    └─── Diagonal
          └─── Inches
               ├─── Height
               ├─── Width
               └─── Diagonal
```

## Formats

The data comes in multiple formats.
You find them all in the data folder.

- json
- csv
- yaml
- markdown

## Missing Sensor Data?

To add a new sensor data, create a new sensor submission by going to [Issues -> New issue -> Sensor Submission](https://github.com/EmberLightVFX/Camera-Sensor-Database/issues/new/choose) and fill out all needed information.
After submitting a PR will automatically be created with all files auto-generated and ready to be reviewed.
