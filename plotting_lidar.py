import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as image
from matplotlib.colors import LogNorm
import numpy as np
import datetime as dt
from netCDF4 import Dataset


"""
Useful functions
"""

def set_major_minor_date_ticks(ax):
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0,24,2)))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M\n%Y/%m/%d"))
    
    
    
"""
Plots for today's data
"""

def stare_aerosol_backscatter_today(stare_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png', only_good_data = True):
    """
    Create plot of aerosol backscatter from Stare data
    """
    stare_today_dataset = Dataset(stare_today_file)
    
    y_2d = stare_today_dataset['range'][:,:,0]
    x_2d = np.empty(y_2d.shape, dtype=object)
    dt_times = [ dt.datetime.fromtimestamp(j, dt.timezone.utc) for j in stare_today_dataset['time'][:] ]
    for i in range(y_2d.shape[1]):
        x_2d[:,i] = dt_times
        
    im = image.imread(image_file)
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    if only_good_data:
        data = np.ma.masked_where(stare_today_dataset['qc_flag_backscatter'][:] > 1, stare_today_dataset['attenuated_aerosol_backscatter_coefficient'][:])
    else:
        data = stare_today_dataset['attenuated_aerosol_backscatter_coefficient'][:]
    c = ax.pcolormesh(x_2d,y_2d,data[:,:,0],norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))
    
    set_major_minor_date_ticks(ax)

    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient {stare_today_dataset['attenuated_aerosol_backscatter_coefficient'].units}")

    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    if only_good_data:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_stare_aerosol-backscatter_today_qc.png')
    else:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_stare_aerosol-backscatter_today.png')
    plt.close()
    
    

def wind_profile_aerosol_backscatter_today(wp_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png', only_good_data = True):
    """
    Create plot of aerosol backscatter from Wind Profile data
    """
    wp_today_dataset = Dataset(wp_today_file)
    
    y_2d = wp_today_dataset['range'][:,:,0]
    x_2d = np.empty(y_2d.shape, dtype=object)
    dt_times = [ dt.datetime.fromtimestamp(j, dt.timezone.utc) for j in wp_today_dataset['time'][:] ]
    for i in range(y_2d.shape[1]):
        x_2d[:,i] = dt_times
        
    im = image.imread(image_file)
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    if only_good_data:
        data = np.ma.masked_where(wp_today_dataset['qc_flag_backscatter'][:] > 1, wp_today_dataset['attenuated_aerosol_backscatter_coefficient'][:])
    else:
        data = wp_today_dataset['attenuated_aerosol_backscatter_coefficient'][:]
    
    c = ax.pcolormesh(x_2d,y_2d,data[:,:,0],norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))
    
    set_major_minor_date_ticks(ax)

    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient {wp_today_dataset['attenuated_aerosol_backscatter_coefficient'].units}")

    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    if only_good_data:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_aerosol-backscatter_today_qc.png')
    else:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_aerosol-backscatter_today.png')
    plt.close()
    
    
    
def wind_profile_mean_winds_speed_direction_today(meanwind_today_file, output_location = '.', image_file = 'logo--white_43f4c135.png', barb_interval = 5):
    """
    Create plot of wind speed and direction from Wind Profile data
    """
    meanwind_today_dataset = Dataset(meanwind_today_file)
    
    im = image.imread(image_file)
    
    u = meanwind_today_dataset['eastward_wind'][:]
    v = meanwind_today_dataset['northward_wind'][:]
    
    y = meanwind_today_dataset['altitude'][:]
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in meanwind_today_dataset['time'][:] ]
    
    x,y = np.meshgrid(x,y)
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    pc = ax.pcolormesh(x,y,meanwind_today_dataset['wind_speed'][:].T)
    
    set_major_minor_date_ticks(ax)
    
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time')
    ax.grid(which='both')
    
    cbar = fig.colorbar(pc, ax = ax)
    cbar.ax.set_ylabel('Wind speed (m s-1)')
    ax.barbs(x[::barb_interval,::barb_interval], y[::barb_interval,::barb_interval], u[::barb_interval,::barb_interval].T, v[::barb_interval,::barb_interval].T, length = 7)
    
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_mean-winds_speed-direction_today.png')
    plt.close()
    
    
    
def wind_profile_mean_winds_upward_velocity_today(meanwind_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of upward air velocity from Wind Profile data
    """
    meanwind_today_dataset = Dataset(meanwind_today_file)
    
    y = meanwind_today_dataset['altitude'][:]
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in meanwind_today_dataset['time'][:] ]
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    c = ax.pcolormesh(x,y,meanwind_today_dataset['upward_air_velocity'][:].T, cmap='RdBu_r', vmin = -5, vmax = 5)
    
    set_major_minor_date_ticks(ax)
    
    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Upward air velocity {meanwind_today_dataset['upward_air_velocity'].units}")
    
    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_mean-winds_upward-velocity_today.png')
    plt.close()

    
"""
Plots for last 24 hours
"""

def stare_aerosol_backscatter_last24(stare_yesterday_file, stare_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png', only_good_data = True):
    """
    Create plot of aerosol backscatter from Stare data for last 24 hours
    """
    stare_yesterady_dataset = Dataset(stare_yesterday_file)
    stare_today_dataset = Dataset(stare_today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    time_minus_24 = current_time - dt.timedelta(days=1)
    time_minus_24_timestamp = time_minus_24.timestamp()
    
    y_locs = np.where(stare_yesterady_dataset['time'][:] > time_minus_24_timestamp)[0]
    
    y_times = stare_yesterady_dataset['time'][:][y_locs]
    t_times = stare_today_dataset['time'][:]
    times = np.hstack((y_times,t_times))
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
        
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    if only_good_data:
        data_y = np.ma.masked_where(stare_yesterady_dataset['qc_flag_backscatter'][y_locs,:,:] > 1, stare_yesterady_dataset['attenuated_aerosol_backscatter_coefficient'][y_locs,:,:])
        data_t = np.ma.masked_where(stare_today_dataset['qc_flag_backscatter'][:] > 1, stare_today_dataset['attenuated_aerosol_backscatter_coefficient'][:])
        data = np.ma.vstack((data_y,data_t))
    else:
        data_y = stare_yesterady_dataset['attenuated_aerosol_backscatter_coefficient'][y_locs,:,:]
        data_t = stare_today_dataset['attenuated_aerosol_backscatter_coefficient'][:]
        data = np.vstack((data_y,data_t))
        
    c = ax.pcolormesh(x,stare_today_dataset['range'][0,:,0],data[:,:,0].T,norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))
    
    set_major_minor_date_ticks(ax)

    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient {stare_today_dataset['attenuated_aerosol_backscatter_coefficient'].units}")

    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    if only_good_data:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_stare_aerosol-backscatter_last24_qc.png')
    else:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_stare_aerosol-backscatter_last24.png')
    plt.close()
    

    
def wind_profile_aerosol_backscatter_last24(wp_yesterday_file, wp_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png', only_good_data = True):
    """
    Create plot of aerosol backscatter from Wind Profile data for last 24 hours
    """
    wp_yesterday_dataset = Dataset(wp_yesterday_file)
    wp_today_dataset = Dataset(wp_today_file)
    
    current_time = dt.datetime.strptime("2022-06-07T17:54:48 +00:00","%Y-%m-%dT%H:%M:%S %z")
    time_minus_24 = current_time - dt.timedelta(days=1)
    time_minus_24_timestamp = time_minus_24.timestamp()
    
    y_locs = np.where(wp_yesterday_dataset['time'][:] > time_minus_24_timestamp)[0]
    
    y_times = wp_yesterday_dataset['time'][:][y_locs]
    t_times = wp_today_dataset['time'][:]
    times = np.hstack((y_times,t_times))
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
        
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    if only_good_data:
        data_y = np.ma.masked_where(wp_yesterday_dataset['qc_flag_backscatter'][y_locs,:,:] > 1, wp_yesterday_dataset['attenuated_aerosol_backscatter_coefficient'][y_locs,:,:])
        data_t = np.ma.masked_where(wp_today_dataset['qc_flag_backscatter'][:] > 1, wp_today_dataset['attenuated_aerosol_backscatter_coefficient'][:])
        data = np.ma.vstack((data_y,data_t))
    else:
        data_y = wp_yesterday_dataset['attenuated_aerosol_backscatter_coefficient'][y_locs,:,:]
        data_t = wp_today_dataset['attenuated_aerosol_backscatter_coefficient'][:]
        data = np.vstack((data_y,data_t))
        
    c = ax.pcolormesh(x,wp_today_dataset['range'][0,:,0],data[:,:,0].T,norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))
    
    set_major_minor_date_ticks(ax)

    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient {wp_today_dataset['attenuated_aerosol_backscatter_coefficient'].units}")

    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    if only_good_data:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_aerosol-backscatter_last24_qc.png')
    else:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_aerosol-backscatter_last24.png')
    plt.close()
    
    
    
def wind_profile_mean_winds_speed_direction_last24(meanwind_yesterday_file, meanwind_today_file, output_location = '.', image_file = 'logo--white_43f4c135.png', barb_interval = 5):
    """
    Create plot of wind speed and direction from Wind Profile data for last 24 hours
    """
    meanwind_yesterday_dataset = Dataset(meanwind_yesterday_file)
    meanwind_today_dataset = Dataset(meanwind_today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    time_minus_24 = current_time - dt.timedelta(days=1)
    time_minus_24_timestamp = time_minus_24.timestamp()
    
    y_locs = np.where(meanwind_yesterday_dataset['time'][:] > time_minus_24_timestamp)[0]
    
    y_times = meanwind_yesterday_dataset['time'][:][y_locs]
    t_times = meanwind_today_dataset['time'][:]
    times = np.hstack((y_times,t_times))
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
    
    u_y = meanwind_today_dataset['eastward_wind'][y_locs]
    u_t = meanwind_today_dataset['eastward_wind'][:]
    u = np.vstack((u_y,u_t))
    
    v_y = meanwind_today_dataset['northward_wind'][y_locs]
    v_t = meanwind_today_dataset['northward_wind'][:]
    v = np.vstack((v_y,v_t))
    
    ws_y = meanwind_today_dataset['wind_speed'][y_locs]
    ws_t = meanwind_today_dataset['wind_speed'][:]
    ws = np.vstack((ws_y,ws_t))
    
    y = meanwind_today_dataset['altitude'][:]
    
    x,y = np.meshgrid(x,y)
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    pc = ax.pcolormesh(x,y,ws.T)
    
    set_major_minor_date_ticks(ax)
    
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time')
    ax.grid(which='both')
    
    cbar = fig.colorbar(pc, ax = ax)
    cbar.ax.set_ylabel('Wind speed (m s-1)')
    ax.barbs(x[::barb_interval,::barb_interval], y[::barb_interval,::barb_interval], u[::barb_interval,::barb_interval].T, v[::barb_interval,::barb_interval].T, length = 7)
    
    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_mean-winds_speed-direction_last24.png')
    plt.close()
    
    
    
def wind_profile_mean_winds_upward_velocity_last24(meanwind_yesterday_file, meanwind_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of upward air velocity from Wind Profile data
    """
    meanwind_yesterday_dataset = Dataset(meanwind_yesterday_file)
    meanwind_today_dataset = Dataset(meanwind_today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    time_minus_24 = current_time - dt.timedelta(days=1)
    time_minus_24_timestamp = time_minus_24.timestamp()
    
    y_locs = np.where(meanwind_yesterday_dataset['time'][:] > time_minus_24_timestamp)[0]
    
    y_times = meanwind_yesterday_dataset['time'][:][y_locs]
    t_times = meanwind_today_dataset['time'][:]
    times = np.hstack((y_times,t_times))
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
    
    y = meanwind_today_dataset['altitude'][:]
    
    w_y = meanwind_today_dataset['upward_air_velocity'][y_locs]
    w_t = meanwind_today_dataset['upward_air_velocity'][:]
    w = np.vstack((w_y,w_t))
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    c = ax.pcolormesh(x,y,w.T, cmap='RdBu_r', vmin = -5, vmax = 5)
    
    set_major_minor_date_ticks(ax)
    
    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Upward air velocity {meanwind_today_dataset['upward_air_velocity'].units}")
    
    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_mean-winds_upward-velocity_last24.png')
    plt.close()


"""
Plots for last 48 hours
"""

def stare_aerosol_backscatter_last48(stare_daybeforeyesterday_file, stare_yesterday_file, stare_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png', only_good_data = True):
    """
    Create plot of aerosol backscatter from Stare data for last 24 hours
    """
    stare_dby_dataset = Dataset(stare_daybeforeyesterday_file)
    stare_yesterady_dataset = Dataset(stare_yesterday_file)
    stare_today_dataset = Dataset(stare_today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    time_minus_48 = current_time - dt.timedelta(days=2)
    time_minus_48_timestamp = time_minus_48.timestamp()
    
    y_locs = np.where(stare_dby_dataset['time'][:] > time_minus_48_timestamp)[0]
    
    dby_times = stare_dby_dataset['time'][:][y_locs]
    y_times = stare_yesterady_dataset['time'][:]
    t_times = stare_today_dataset['time'][:]
    times = np.hstack((dby_times, y_times,t_times))
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
        
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    if only_good_data:
        data_dby = np.ma.masked_where(stare_dby_dataset['qc_flag_backscatter'][y_locs,:,:] > 1, stare_dby_dataset['attenuated_aerosol_backscatter_coefficient'][y_locs,:,:])
        data_y = np.ma.masked_where(stare_yesterady_dataset['qc_flag_backscatter'][:] > 1, stare_yesterady_dataset['attenuated_aerosol_backscatter_coefficient'][:])
        data_t = np.ma.masked_where(stare_today_dataset['qc_flag_backscatter'][:] > 1, stare_today_dataset['attenuated_aerosol_backscatter_coefficient'][:])
        data = np.ma.vstack((data_dby,data_y,data_t))
    else:
        data_dby = stare_dby_dataset['attenuated_aerosol_backscatter_coefficient'][y_locs,:,:]
        data_y = stare_yesterady_dataset['attenuated_aerosol_backscatter_coefficient'][:]
        data_t = stare_today_dataset['attenuated_aerosol_backscatter_coefficient'][:]
        data = np.vstack((data_dby,data_y,data_t))
        
    c = ax.pcolormesh(x,stare_today_dataset['range'][0,:,0],data[:,:,0].T,norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))
    
    set_major_minor_date_ticks(ax)

    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient {stare_today_dataset['attenuated_aerosol_backscatter_coefficient'].units}")

    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    if only_good_data:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_stare_aerosol-backscatter_last48_qc.png')
    else:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_stare_aerosol-backscatter_last48.png')
    plt.close()
    

    
def wind_profile_aerosol_backscatter_last48(wp_daybeforeyesterday_file, wp_yesterday_file, wp_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png', only_good_data = True):
    """
    Create plot of aerosol backscatter from Wind Profile data for last 24 hours
    """
    wp_dby_dataset = Dataset(wp_daybeforeyesterday_file)
    wp_yesterday_dataset = Dataset(wp_yesterday_file)
    wp_today_dataset = Dataset(wp_today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    time_minus_48 = current_time - dt.timedelta(days=2)
    time_minus_48_timestamp = time_minus_48.timestamp()
    
    y_locs = np.where(wp_dby_dataset['time'][:] > time_minus_48_timestamp)[0]
    
    dby_times = wp_dby_dataset['time'][:][y_locs]
    y_times = wp_yesterday_dataset['time'][:]
    t_times = wp_today_dataset['time'][:]
    times = np.hstack((dby_times, y_times,t_times))
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
        
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    if only_good_data:
        data_dby = np.ma.masked_where(wp_dby_dataset['qc_flag_backscatter'][y_locs,:,:] > 1, wp_dby_dataset['attenuated_aerosol_backscatter_coefficient'][y_locs,:,:])
        data_y = np.ma.masked_where(wp_yesterday_dataset['qc_flag_backscatter'][:] > 1, wp_yesterday_dataset['attenuated_aerosol_backscatter_coefficient'][:])
        data_t = np.ma.masked_where(wp_today_dataset['qc_flag_backscatter'][:] > 1, wp_today_dataset['attenuated_aerosol_backscatter_coefficient'][:])
        data = np.ma.vstack((data_dby,data_y,data_t))
    else:
        data_dby = wp_dby_dataset['attenuated_aerosol_backscatter_coefficient'][y_locs,:,:]
        data_y = wp_yesterday_dataset['attenuated_aerosol_backscatter_coefficient'][:]
        data_t = wp_today_dataset['attenuated_aerosol_backscatter_coefficient'][:]
        data = np.vstack((data_dby,data_y,data_t))
        
    c = ax.pcolormesh(x,wp_today_dataset['range'][0,:,0],data[:,:,0].T,norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))
    
    set_major_minor_date_ticks(ax)

    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient {wp_today_dataset['attenuated_aerosol_backscatter_coefficient'].units}")

    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    if only_good_data:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_aerosol-backscatter_last48_qc.png')
    else:
        plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_aerosol-backscatter_last48.png')
    plt.close()
    
    
    
def wind_profile_mean_winds_speed_direction_last48(meanwind_daybeforeyesterday_file, meanwind_yesterday_file, meanwind_today_file, output_location = '.', image_file = 'logo--white_43f4c135.png', barb_interval = 5):
    """
    Create plot of wind speed and direction from Wind Profile data for last 24 hours
    """
    meanwind_dby_dataset = Dataset(meanwind_daybeforeyesterday_file)
    meanwind_yesterday_dataset = Dataset(meanwind_yesterday_file)
    meanwind_today_dataset = Dataset(meanwind_today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    time_minus_48 = current_time - dt.timedelta(days=2)
    time_minus_48_timestamp = time_minus_48.timestamp()
    
    y_locs = np.where(meanwind_dby_dataset['time'][:] > time_minus_48_timestamp)[0]
    
    dby_times = meanwind_dby_dataset['time'][:][y_locs]
    y_times = meanwind_yesterday_dataset['time'][:]
    t_times = meanwind_today_dataset['time'][:]
    times = np.hstack((dby_times, y_times,t_times))
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
    
    u_dby = meanwind_dby_dataset['eastward_wind'][y_locs]
    u_y = meanwind_yesterday_dataset['eastward_wind'][:]
    u_t = meanwind_today_dataset['eastward_wind'][:]
    u = np.vstack((u_dby,u_y,u_t))
    
    v_dby = meanwind_dby_dataset['northward_wind'][y_locs]
    v_y = meanwind_yesterday_dataset['northward_wind'][:]
    v_t = meanwind_today_dataset['northward_wind'][:]
    v = np.vstack((v_dby,v_y,v_t))
    
    ws_dby = meanwind_dby_dataset['wind_speed'][y_locs]    
    ws_y = meanwind_yesterday_dataset['wind_speed'][:]
    ws_t = meanwind_today_dataset['wind_speed'][:]
    ws = np.vstack((ws_dby,ws_y,ws_t))
    
    y = meanwind_today_dataset['altitude'][:]
    
    x,y = np.meshgrid(x,y)
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    pc = ax.pcolormesh(x,y,ws.T)
    
    set_major_minor_date_ticks(ax)
    
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time')
    ax.grid(which='both')
    
    cbar = fig.colorbar(pc, ax = ax)
    cbar.ax.set_ylabel('Wind speed (m s-1)')
    ax.barbs(x[::barb_interval,::barb_interval], y[::barb_interval,::barb_interval], u[::barb_interval,::barb_interval].T, v[::barb_interval,::barb_interval].T, length = 7)
    
    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_mean-winds_speed-direction_last48.png')
    plt.close()
    
    
    
def wind_profile_mean_winds_upward_velocity_last48(meanwind_daybeforeyesterday_file, meanwind_yesterday_file, meanwind_today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of upward air velocity from Wind Profile data
    """
    meanwind_dby_dataset = Dataset(meanwind_daybeforeyesterday_file)
    meanwind_yesterday_dataset = Dataset(meanwind_yesterday_file)
    meanwind_today_dataset = Dataset(meanwind_today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    time_minus_48 = current_time - dt.timedelta(days=2)
    time_minus_48_timestamp = time_minus_48.timestamp()
    
    y_locs = np.where(meanwind_dby_dataset['time'][:] > time_minus_48_timestamp)[0]
    
    dby_times = meanwind_dby_dataset['time'][:][y_locs]
    y_times = meanwind_yesterday_dataset['time'][:]
    t_times = meanwind_today_dataset['time'][:]
    times = np.hstack((dby_times, y_times,t_times))
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
    
    y = meanwind_today_dataset['altitude'][:]
    
    w_dby = meanwind_dby_dataset['upward_air_velocity'][:][y_locs]
    w_y = meanwind_yesterday_dataset['upward_air_velocity'][:]
    w_t = meanwind_today_dataset['upward_air_velocity'][:]
    w = np.vstack((w_dby,w_y,w_t))
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    c = ax.pcolormesh(x,y,w.T, cmap='RdBu_r', vmin = -5, vmax = 5)
    
    set_major_minor_date_ticks(ax)
    
    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Upward air velocity {meanwind_today_dataset['upward_air_velocity'].units}")
    
    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-lidar-dop-2_wind-profile_mean-winds_upward-velocity_last48.png')
    plt.close()



    
if __name__ == "__main__":
    """
    import sys
    #meanwind_today_file = sys.argv[1]
    #wind_profile_mean_winds_upward_velocity_today(meanwind_today_file)
    stare_yesterday_file=sys.argv[2]
    stare_today_file=sys.argv[3]
    stare_dby_file = sys.argv[1]
    stare_aerosol_backscatter_today(stare_today_file)
    stare_aerosol_backscatter_last24(stare_yesterday_file, stare_today_file)
    stare_aerosol_backscatter_last48(stare_dby_file, stare_yesterday_file, stare_today_file)
    #stare_aerosol_backscatter_today(stare_today_file)
    """
    import argparse
    parser = argparse.ArgumentParser(description = 'Make plots for ncas-lidar-dop-2.', allow_abbrev=False, argument_default=argparse.SUPPRESS)
    parser.add_argument('netCDFs', nargs = '+', help = "netCDF files with data to be plotted. At minimum today's file should be given, \
                                                        as well as yesterday's for 24 hour plots and the day before yesterday's for 48 hour plots.")
    parser.add_argument('-o','--output-location', default = ".", help = "Location of where to save plots. Default is '.'.")
    parser.add_argument('-s','--stare-aerosol-backscatter-today', action='store_true', help = 'Make plot of aerosol backscatter for today from Stare data.')
    parser.add_argument('-w','--wp-aerosol-backscatter-today', action='store_true', help = 'Make plot of aerosol backscatter for today from Wind Profile data.')
    parser.add_argument('-u','--speed-direction-today', action='store_true', help = 'Make plot of wind speed and direction for today.')
    parser.add_argument('-v','--vertical-velocity-today', action='store_true', help = 'Make plot of vertical velocity for today.')
    
    parser.add_argument('-s24','--stare-aerosol-backscatter-last24', action='store_true', help = 'Make plot of aerosol backscatter for last 24 hours from Stare data.')
    parser.add_argument('-w24','--wp-aerosol-backscatter-last24', action='store_true', help = 'Make plot of aerosol backscatter for last 24 hours from Wind Profile data.')
    parser.add_argument('-u24','--speed-direction-last24', action='store_true', help = 'Make plot of wind speed and direction for last 24 hours.')
    parser.add_argument('-v24','--vertical-velocity-last24', action='store_true', help = 'Make plot of vertical velocity for last 24 hours.')
    
    parser.add_argument('-s48','--stare-aerosol-backscatter-last48', action='store_true', help = 'Make plot of aerosol backscatter for last 48 hours from Stare data.')
    parser.add_argument('-w48','--wp-aerosol-backscatter-last48', action='store_true', help = 'Make plot of aerosol backscatter for last 48 hours from Wind Profile data.')
    parser.add_argument('-u48','--speed-direction-last48', action='store_true', help = 'Make plot of wind speed and direction for last 48 hours.')
    parser.add_argument('-v48','--vertical-velocity-last48', action='store_true', help = 'Make plot of vertical velocity for last 48 hours.')
    args = parser.parse_args()
    
    
    given_args = args._get_kwargs()
    netcdf_files = args.netCDFs
    
    # Check no repeated netCDF files
    if len(set(netcdf_files)) != len(netcdf_files):
        counter = Counter(netcdf_files)
        msg = 'the following files have been given more than once:'
        for i in counter.items():
            if i[1] > 1:
                msg += ' '
                msg += str(i[0])
                msg += ','
        msg = msg[:-1]  # remove trailing comma
        raise ValueError(msg)
    
    
    # Check not too many netCDF files
    stare_netcdfs = [ f for f in netcdf_files if 'aerosol-backscatter-radial-winds_stare' in f ]
    if len(stare_netcdfs) > 3:
        msg = "Too many netCDF files for aerosol-backscatter-radial-winds_stare"
        raise ValueError(msg)
    stare_dates = [ f.split('ncas-lidar-dop-2')[1].split('_')[2] for f in stare_netcdfs ]
    
    # Check no repeated dates
    if len(set(stare_dates)) != len(stare_dates):
        counter = Counter(stare_netcdfs)
        msg = 'the following dates have been given more than once for aerosol-backscatter-radial-winds_stare:'
        for i in counter.items():
            if i[1] > 1:
                msg += ' '
                msg += str(i[0])
                msg += ','
        msg = msg[:-1]  # remove trailing comma
        raise ValueError(msg)
        
    # order files by date in reverse, i.e. today's file first
    reversed_dates = sorted(stare_dates, reverse=True)
    stare_netcdf_ordered = []
    for d in reversed_dates:
        for f in stare_netcdfs:
            if d in f:
                stare_netcdf_ordered.append(f)
                break
    
    
    # Check not too many netCDF files
    wp_netcdfs = [ f for f in netcdf_files if 'aerosol-backscatter-radial-winds_wind-profile' in f ]
    if len(wp_netcdfs) > 3:
        msg = "Too many netCDF files for aerosol-backscatter-radial-winds_wind-profile"
        raise ValueError(msg)
    wp_dates = [ f.split('ncas-lidar-dop-2')[1].split('_')[2] for f in wp_netcdfs ]
    
    # Check no repeated dates
    if len(set(wp_dates)) != len(wp_dates):
        counter = Counter(wp_dates)
        msg = 'the following dates have been given more than once for aerosol-backscatter-radial-winds_wind-profile:'
        for i in counter.items():
            if i[1] > 1:
                msg += ' '
                msg += str(i[0])
                msg += ','
        msg = msg[:-1]  # remove trailing comma
        raise ValueError(msg)
        
    # order files by date in reverse, i.e. today's file first
    reversed_dates = sorted(wp_dates, reverse=True)
    wp_netcdf_ordered = []
    for d in reversed_dates:
        for f in wp_netcdfs:
            if d in f:
                wp_netcdf_ordered.append(f)
                break
    
    
    # Check not too many netCDF files
    meanwinds_netcdfs = [ f for f in netcdf_files if 'mean-winds-profile' in f ]
    if len(meanwinds_netcdfs) > 3:
        msg = "Too many netCDF files for mean-winds-profile"
        raise ValueError(msg)
    mw_dates = [ f.split('ncas-lidar-dop-2')[1].split('_')[2] for f in meanwinds_netcdfs ]
    
    # Check no repeated dates
    if len(set(mw_dates)) != len(mw_dates):
        counter = Counter(mw_dates)
        msg = 'the following dates have been given more than once for mean-winds-profile:'
        for i in counter.items():
            if i[1] > 1:
                msg += ' '
                msg += str(i[0])
                msg += ','
        msg = msg[:-1]  # remove trailing comma
        raise ValueError(msg)
        
    # order files by date in reverse, i.e. today's file first
    reversed_dates = sorted(mw_dates, reverse=True)
    meanwinds_netcdf_ordered = []
    for d in reversed_dates:
        for f in meanwinds_netcdfs:
            if d in f:
                meanwinds_netcdf_ordered.append(f)
                break
                
                
    # make the requested plots
    for i in given_args:
        if i[0] not in  ['netCDFs', 'output_location']:
            if i[0] == 'stare_aerosol_backscatter_today':
                print('Making stare_aerosol_backscatter_today')
                stare_aerosol_backscatter_today(stare_netcdf_ordered[0], output_location = args.output_location)
            elif i[0] == 'stare_aerosol_backscatter_last24':
                print('Making stare_aerosol_backscatter_last24')
                stare_aerosol_backscatter_last24(stare_netcdf_ordered[1], stare_netcdf_ordered[0], output_location = args.output_location)
            elif i[0] == 'stare_aerosol_backscatter_last48':
                print('Making stare_aerosol_backscatter_last48')
                stare_aerosol_backscatter_last48(stare_netcdf_ordered[2], stare_netcdf_ordered[1], stare_netcdf_ordered[0], output_location = args.output_location)
                
            elif i[0] == 'wp_aerosol_backscatter_today':
                print('Making wp_aerosol_backscatter_today')
                wind_profile_aerosol_backscatter_today(wp_netcdf_ordered[0], output_location = args.output_location)
            elif i[0] == 'wp_aerosol_backscatter_last24':
                print('Making wp_aerosol_backscatter_last24')
                wind_profile_aerosol_backscatter_last24(wp_netcdf_ordered[1], wp_netcdf_ordered[0], output_location = args.output_location)
            elif i[0] == 'wp_aerosol_backscatter_last48':
                print('Making wp_aerosol_backscatter_last48')
                wind_profile_aerosol_backscatter_last48(wp_netcdf_ordered[2], wp_netcdf_ordered[1], wp_netcdf_ordered[0], output_location = args.output_location)
                
            elif i[0] == 'speed_direction_today':
                print('Making speed_direction_today')
                wind_profile_mean_winds_speed_direction_today(meanwinds_netcdf_ordered[0], output_location = args.output_location)
            elif i[0] == 'speed_direction_last24':
                print('Making speed_direction_last24')
                wind_profile_mean_winds_speed_direction_last24(meanwinds_netcdf_ordered[1], meanwinds_netcdf_ordered[0], output_location = args.output_location)
            elif i[0] == 'speed_direction_last48':
                print('Making speed_direction_last48')
                wind_profile_mean_winds_speed_direction_last48(meanwinds_netcdf_ordered[2], meanwinds_netcdf_ordered[1], meanwinds_netcdf_ordered[0], output_location = args.output_location)
                
            elif i[0] == 'vertical_velocity_today':
                print('Making vertical_velocity_today')
                wind_profile_mean_winds_upward_velocity_today(meanwinds_netcdf_ordered[0], output_location = args.output_location)
            elif i[0] == 'vertical_velocity_last24':
                print('Making vertical_velocity_last24')
                wind_profile_mean_winds_upward_velocity_last24(meanwinds_netcdf_ordered[1], meanwinds_netcdf_ordered[0], output_location = args.output_location)
            elif i[0] == 'vertical_velocity_last48':
                print('Making vertical_velocity_last48')
                wind_profile_mean_winds_upward_velocity_last48(meanwinds_netcdf_ordered[2], meanwinds_netcdf_ordered[1], meanwinds_netcdf_ordered[0], output_location = args.output_location)
                
            else:
                print(f'Unexpected option {i}, not sure how to deal with it, skipping... ')
