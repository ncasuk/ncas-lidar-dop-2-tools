#
# Make all plots for ncas-lidar-dop-2
#

netcdf_file_location=/gws/nopw/j04/ncas_obs/iao/processing/ncas-lidar-dop-2/netcdf_files
plot_output_location=/gws/nopw/j04/ncas_obs/iao/public/ncas-lidar-dop-2/plots
version=1.0



SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

today_date=$(date --utc +%Y%m%d)
yesterday_date=$(date --utc -d "-1 day" +%Y%m%d)
day_before_yesterday_date=$(date --utc -d "-2 days" +%Y%m%d)


stare_aerosol_today_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${today_date}_aerosol-backscatter-radial-winds_stare_v${version}.nc
stare_aerosol_yest_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${yesterday_date}_aerosol-backscatter-radial-winds_stare_v${version}.nc
stare_aerosol_dby_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${day_before_yesterday_date}_aerosol-backscatter-radial-winds_stare_v${version}.nc

wp_aerosol_today_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${today_date}_aerosol-backscatter-radial-winds_wind-profile_v${version}.nc
wp_aerosol_yest_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${yesterday_date}_aerosol-backscatter-radial-winds_wind-profile_v${version}.nc
wp_aerosol_dby_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${day_before_yesterday_date}_aerosol-backscatter-radial-winds_wind-profile_v${version}.nc

meanwinds_today_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${today_date}_mean-winds-profile_v${version}.nc
meanwinds_yest_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${yesterday_date}_mean-winds-profile_v${version}.nc
meanwinds_dby_ncfile=${netcdf_file_location}/ncas-lidar-dop-2_iao_${day_before_yesterday_date}_mean-winds-profile_v${version}.nc



python ${SCRIPT_DIR}/plotting_lidar.py ${stare_aerosol_today_ncfile} ${stare_aerosol_yest_ncfile} ${stare_aerosol_dby_ncfile} ${wp_aerosol_today_ncfile} ${wp_aerosol_yest_ncfile} ${wp_aerosol_dby_ncfile} ${meanwinds_today_ncfile} ${meanwinds_yest_ncfile} ${meanwinds_dby_ncfile} -s -s24 -s48 -w -w24 -w48 -u -u24 -u48 -v -v24 -v48 -o ${plot_output_location}
