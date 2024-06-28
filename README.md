# 4DSpace Numerical Workshops

Plasma simulation project for [2024 Kobe+Oslo 4DSpace workshops](https://www.mn.uio.no/fysikk/english/research/projects/4dspace/education/04_japan-norway-intpart.html).

## Authors

Group 3: ***Aurora***
 - Doyeon Kim
 - Michał Jan Odorczuk
 - Rachel Knutsen Stiansen
 - Shunsuke Kawamura
 - Taito Taniguchi

## Description

The project is a part of a 4DSpace Numerical Workshop program. The program focused on Particle-In-Cell simulations in [EMSES](https://www.energy.kyoto-u.ac.jp/gcoe/en/emses/aboutemses.htm) software, using [CAMPHOR]() supercomputer from [Kyoto University](https://www.kyoto-u.ac.jp/ja).

### Context

The team was given access to a Particle-In-Cell simulation software with a high processing power computer and a study case of a simplified model of the satellite [NorSat-1](http://tid.uio.no/plasma/norsat/norsat1.html) in a supersonic, frozen-in plasma flow.

![NorSat-1](http://tid.uio.no/plasma/norsat/images/norsat1.jpg)

### Goals

During the initial workshop in Kobe, the team decided to investigate the formation of a Mach cone behind the satellite depending on various parameters of the flow, plasma and the magnetic field. PIC simulations may be simplified by using different plasma parameters, like much lighter ions, lower plasma temperature or much lower plasma densities. The table below compares the default values in the simulation with the environment experienced by the real NorSat-1.



| Parameter | default | real |
| :--- | ---: | ---: |
| Plasma density | $10^5$ #/cc | $2-6\times10^5$ #/cc[^goals1] |
| Electron temperature | $1000$ K | $\approx2600$ K[^goals2] |
| Ion temperature | $750$ K | $\approx1500$ K[^goals2] |
| Plasma flow speed | $7786$ m/s | $7572$ m/s[^goals3] |
| Ion to electron mass ratio | $1000$ | $29000$ [^goals4] |

Default values result in Mach number being equal to 2, and the true values result in Mach number of approximately 6.4. This research aims to verify the feasibility of using such a simplification to model the true behaviour of the Mach cone and the depletion zone formed right behind the satellite.


### Usage

This repository consists of several[^usage1] tools for analysis the simulation output data. To prepare a datafile, import the resultant EMSIS XDMF file containing plasma densities and electric potential field into ParaView, and export the data from the frame of interest (usually the last one) into a CSV file and name it `data_B[axis]_Ma[Mach number]_[Magnetic field strength]uT.csv`, where `[axis]` is the axis parallel to the magnetic field, `[Mach number]` is the Mach number of the plasma flow, and `[Magnetic field Strength]` is the strength of the magnetic field given in μT. For example, `data_Bz_Ma6.4_50uT.csv` is a file including data for a simulation with a plasma moving in the positive x direction at 6.4 times higher velocity than the ion thermal velocity, with magnetic field of strength 50μT oriented in the z direction.

Each notebook should state, where the datafiles should be stored in the **usage** section. Optionally, a choice of the source directory may be given to the user. The name of the data file is used for the labelling of the plots.

## License

[MIT](https://choosealicense.com/licenses/mit/)

[^usage1]: At the moment of writing this description, only one notebook exists.
[^goals1]: http://www.astrosurf.com/luxorion/qsl-hf-tutorial-nm7m3.htm
[^goals2]: Lopez-Arreguin, A.J.R. & Stoll, Enrico. (2019). Addressing the effects of background plasma and wake formation on nanosatellites with electric propulsion using a 3D Particle In Cell code. Results in Physics. 14. 102442. 10.1016/j.rinp.2019.102442.
[^goals3]: $v=\sqrt{\frac{MG}{r}}$, where $M = 5.972\times10^24$, $G=6.674\times 10^6$ and $r=6.951 \times 10^6$ assuming the altitude to be $580$ km.
[^goals4]: Mainly oxygen plasma