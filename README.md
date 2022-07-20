# ncas-lidar-dop-2-tools

Code to make plots from ncas-lidar-dop-2 data for today, last 24 hours, and last 48 hours.

`plotting_lidar.sh` will find netCDF files and make all plots available, options to potentially change are:
* `netcdf_file_location` - where to find the netCDF files
* `plot_output_location` - where to save the plots


`plotting_lidar.py` can be called directly (i.e. `python plotting_lidar.py`) with command line options to make individual plots. Use `python plotting_lidar.py -h` to see all the available options.
