import pandas as pd
from pathlib import Path
import numpy as np
import plotly
import plotly.graph_objects as go
import geopandas as gpd


def plotly_3d_scatter_plot(semi_pts, dir_plot):
    """
    3D plot of scatter points.

    Parameters
    ----------

    """

    # dir_plot.mkdir(parents=True, exist_ok=True)

    layout = go.Layout(
        width=1000,
        height=800,
        title_text="3D points",
        scene=dict(
            xaxis=dict(title='Easting (m)'),
            yaxis=dict(title='Northing (m)'),
            zaxis=dict(title='Height (m)'),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=1)
            ))


    fig = go.Figure(layout=layout)

    fig.add_trace(go.Scatter3d(
        x=semi_pts['x'],
        y=semi_pts['y'],
        z=semi_pts['z'],
        showlegend=False,
        mode='markers',
        marker=dict(size=2, color=semi_pts['z'], colorscale='RdylBu_r', cmin=0,
                    cmax=5,
                    opacity=1,
                    line=dict(width=0), colorbar=dict(thickness=20)),
    ))
    # fig.update_layout(
    #     scene=dict(
    #         # xaxis=dict(nticks=5, range=[settings['xmin'], settings['xmax']]),
    #         # yaxis=dict(nticks=5, range=[settings['ymin'], settings['ymax']]),
    #         # zaxis=dict(nticks=5, range=[settings['cmin'], settings['cmax']]),
    #         camera_eye=dict(x=0.9, y=1.1, z=0.5),
    #     ))
    html_file = 'test2.html'
    plotly.offline.plot(fig, filename=html_file, auto_open=False)

    # fig.show()
    return fig


# parameters
extract = True

# semi points filepaths in, out
f_semi_pts = Path(
    '/home/florent/Projects/Etretat/litto3d/0495_6965/NHDF-MAR_FRA_0498_6961_2016-2018_L93_RGF93_IGN69/Semis_points_Sol/NHDF-MAR_FRA_0498_6961_PTS_2016-2018_L93_RGF93_IGN69.xyz')
f_semi_pts_out = f_semi_pts.parent.joinpath(f_semi_pts.name.replace('.xyz', '_selection.xyz'))

# epsg in, out
epsg_in = 2154
epsg_out = 32631

# bbox and selection area
bbox_xmin = 498068
bbox_xmax = 498101
bbox_ymin = 6960164
bbox_ymax = 6960194
selection_area_filepath = Path('/home/florent/Projects/Etretat/Geodesie/selection_area_litto3d_semi_pts_test.gpkg')
selection_area = gpd.read_file(selection_area_filepath)

# read semi points
semi_pts = pd.read_csv(f_semi_pts, sep=' ', usecols=['x', 'y', 'z'])

# select points inside selection area
if extract:

    # keep onlly points inside bbox
    semi_pts_out = semi_pts[(semi_pts['x'].between(bbox_xmin, bbox_xmax)) & (semi_pts['y'].between(bbox_ymin, bbox_ymax))]

    # create geodataframe
    semi_pts_out = gpd.GeoDataFrame(
        semi_pts_out, geometry=gpd.points_from_xy(semi_pts_out.x, semi_pts_out.y, semi_pts_out.z), crs="EPSG:%s"%epsg_in
    )
    semi_pts_out = semi_pts_out.drop(columns=['x', 'y', 'z'])

    # convert geodataframe to epsg_out
    semi_pts_out = semi_pts_out.to_crs(epsg_out)

    # keep only points inside selection area
    semi_pts_out = gpd.clip(semi_pts_out, selection_area.geometry[0])

    # convert gdf to df
    d = {'x': semi_pts_out['geometry'].x, 'y': semi_pts_out['geometry'].y, 'z': semi_pts_out['geometry'].z}
    df = pd.DataFrame(data=d)

    # save selection of semi points
    df.to_csv(f_semi_pts_out, index=False)

semi_pts_out = pd.read_csv(f_semi_pts_out)

# Create 3D scatter plot
plotly_3d_scatter_plot(semi_pts_out, f_semi_pts.parent)



