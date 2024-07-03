<div align="center">
    <img src="https://raw.githubusercontent.com/EmberLightVFX/Camera-Sensor-Database/main/assets/logo.svg?sanitize=true" alt="logo" title="Logo" height="250" />

# Camera Sensor Database

</div>

<p align="center">
  <i>A collection of camera sensor information. Free to use anywhere.</i>
</p>

<p align="center">
     <img alt="GitHub last commit (branch)" src="https://img.shields.io/github/last-commit/EmberLightVFX/Camera-Sensor-Database/main?color=48b293">
     <a href="https://github.com/EmberLightVFX/Camera-Sensor-Database/graphs/contributors">
          <img src="https://img.shields.io/github/contributors-anon/EmberLightVFX/Camera-Sensor-Database?color=d1a91d" alt="contributors"></a>
     <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues-pr/EmberLightVFX/Camera-Sensor-Database">
     <img alt="GitHub License" src="https://img.shields.io/github/license/EmberLightVFX/Camera-Sensor-Database?color=097bbb">
     <a href="https://ko-fi.com/emberlightvfx">
          <img alt="Static Badge" src="https://img.shields.io/badge/donate-fa615d?logo=ko-fi&logoColor=white"></a>
</p>

<div align="center">

  [Web Docs](#web-docs) •
  [External Projects](#external-projects) •
  [Data Structure](#data-structure) •
  [Formats](#formats) •
  [Missing Sensor Data?](#missing-sensor-data)
  
</div>

## Web Docs

You can browse all data directly in the browser here:

<https://emberlightvfx.github.io/Camera-Sensor-Database/>

## External Projects

This is a list of external projects using Camera Sensor Database:

* [Camera Sensor Database for BlackMagic Fusion](https://www.steakunderwater.com/wesuckless/viewtopic.php?p=48931#p48931)

## Data Structure

```tree
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

* json
* csv
* yaml
* markdown

## Missing Sensor Data?

To add a new sensor data, create a new sensor submission by going to [Issues -> New issue -> Sensor Submission](https://github.com/EmberLightVFX/Camera-Sensor-Database/issues/new/choose) and fill out all needed information.
After submitting a PR will automatically be created with all files auto-generated and ready to be reviewed.
