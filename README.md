# CommerceMaster

CommerceMaster is a GUI calculator to help you determine the best routes for your commercing in Mabinogi.

## Using

At the moment I haven't compiled any executables or anything.
This means that you'll have to install the following pip packages:

- [PySimpleGUI](https://pypi.org/project/PySimpleGUI/)

## Editing

### Editing Vehicles

Available vehicles can be edited in the `config/vehicles.json` file.

This part will likely be awkward to adapt to your setup if you only have the normal commerce partner instead of William.
The vehicle data is hardcoded, so if that's your situation you will need to look at your vehicle stats and change the relevant numbers in the `config/vehicles.json` file.
I believe partners only affect slots and weight, so you shouldn't need to figure out new speed values.
All numbers this file were derived either from the [Commerce/Transportation MabinogiWorld Wiki page](https://wiki.mabinogiworld.com/view/Commerce/Transportation), or the in-game commerce menu while you have the relevant pet/partner summoned/unsummoned.

That being said, I will probably add a menu where you can select which pets/partners/mounts are available so you don't have to edit any files soon™.

### Editing Pathfinding

The individual pathfinding notes can be edited in the `config/nodes.json` file.
I think I did an okay enough job of making and weighing the network,
but if you disagree, this is where you can change that.

The `distance` values on connections are in "time it takes for a nimbus to run there." These speed numbers are translated from "pet speed units" to "commerce speed units" during the process of reading the node file. This process is derived from the "Wagon" vehicle having the same speed as the "Haflinger" pet, and translating the nimbus pet speed into a distance, and using other commerce vehicle speeds to get an ETA.

I really can't exaggerate enough when I say I picked waypoint locations, took out my phone, and timed myself running between them for like 8 hours in total.
If I can do it, so can you.

### Editing other

All of the values for *Trading Posts* and *Items* are hardcoded at the moment.
So you'll just have to figure it out and write Python if you want different values.
I'll be adding JSON config support soon™.

All of the timings for the nodes have been recorded in seconds taken to travel the distance on a nimbus.