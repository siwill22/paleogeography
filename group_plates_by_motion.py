import pygplates
#import glob, re
import numpy as np
import matplotlib.pyplot as plt
import paleogeography as pg
reload(pg)


def determine(moving_plate_id,fixed_plate_id,time_from,time_to,rotation_model):
    angle = rotation_model.get_rotation(time_to,moving_plate_id,time_from,fixed_plate_id)
    return angle.represents_identity_rotation()


def split_plate_id_list(plate_id_list,time_from,time_to,rotation_model):
    
    fixed_plate_id = plate_id_list[0]
    
    plate_id_list_copy_True = list(plate_id_list)
    plate_id_list_copy_False = list(plate_id_list)
    
    plate_id_list_copy_True[:] = [tup for tup in plate_id_list_copy_True if determine(tup,fixed_plate_id,time_from,time_to,rotation_model)]
    plate_id_list_copy_False[:] = [tup for tup in plate_id_list_copy_False if not determine(tup,fixed_plate_id,time_from,time_to,rotation_model)]

    return plate_id_list_copy_True,plate_id_list_copy_False


def get_plate_motion_groups(plate_id_list,rotation_model,time,delta_time=1.):
# given a list of plate ids, a rotation model and a time range,
# this function will determine groups of those plate ids within which 
# there is no relative motion between the plates during the specified
# time range

    time_to = time
    time_from = time+delta_time
    
    plate_group_lists = []
    list_moving = list(plate_id_list)
    
    while len(list_moving)>0:
        list_fixed,list_moving = split_plate_id_list(list_moving,time_from,time_to,rotation_model)
        plate_group_lists.append(list_fixed)
        
    return plate_group_lists


def group_features_by_motion(features,rotation_model,time,delta_time=1,plot=False):
# given a list of features, a rotation model and a time range,
# this function will make a list of all the plate_ids based on the
# features, then determine groups of those plate ids within which 
# there is no relative motion between the plates during the specified
# time range
    
    rps = []
    pygplates.reconstruct(features,rotation_model,rps,time)

    pids = []
    for rp in rps:
        pids.append(rp.get_feature().get_reconstruction_plate_id())

    pg_pids = list(set(pids))
    
    plate_group_lists = get_plate_motion_groups(pg_pids,rotation_model,time,delta_time)

    #print 'Number of groups is %d' % len(plate_group_lists)
    #for plate_group in plate_group_lists:
    #    print plate_group

    if plot:
        cmap = plt.get_cmap('hsv')
        colors = cmap(np.linspace(0, 1, len(plate_group_lists)))

        plt.figure(figsize=(20,9))
        for rp in rps:
            for (plate_group,color) in zip(plate_group_lists,colors):
                if rp.get_feature().get_reconstruction_plate_id() in plate_group:
                    plt.plot(rp.get_reconstructed_geometry().to_lat_lon_array()[:,1],
                             rp.get_reconstructed_geometry().to_lat_lon_array()[:,0],color=color)
        plt.show()   
                    
    return plate_group_lists

