import pandas as pd
from pathlib import Path
import plotly
import argparse
import plotly.graph_objects as go
import geopandas as gpd
import yaml

def get_params():

    # construct an argument parser
    parser = argparse.ArgumentParser()

    # add argument to the parser
    parser.add_argument('config')

    # get arguments
    args = vars(parser.parse_args())
    config_file = args['config']
    with open(config_file, 'r') as yaml_file:
        params = yaml.safe_load(yaml_file)
    f_semi_pts = Path(params['f_semi_pts'])
    f_semi_pts_out = Path(params['f_semi_pts_out'])
    f_selection_area = Path(params['f_selection_area'])
    epsg_in = params['epsg_in']
    epsg_out = params['epsg_out']
    return f_semi_pts, f_semi_pts_out, f_selection_area, epsg_in, epsg_out


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
        text=(semi_pts.index + 2).map(str),
        showlegend=False,
        mode='markers',
        marker=dict(size=2, color=semi_pts['z'], colorscale='RdylBu_r', cmin=0,
                    cmax=5,
                    opacity=1,
                    line=dict(width=0), colorbar=dict(thickness=20)),
    ))
    html_file = 'test2.html'
    plotly.offline.plot(fig, filename=html_file, auto_open=False)

    # fig.show()
    return fig


# execution parameter
extract = True

# read yaml parameters
f_semi_pts, f_semi_pts_out, f_selection_area, epsg_in, epsg_out = get_params()

# bbox and selection area
bbox_xmin_lamb93 = 498068
bbox_xmax_lamb93 = 498101
bbox_ymin_lamb93 = 6960164
bbox_ymax_lamb93 = 6960194
selection_area = gpd.read_file(f_selection_area)

# read semi points
semi_pts = pd.read_csv(f_semi_pts, sep=' ', usecols=['x', 'y', 'z'])

# select points inside selection area
if extract:

    # keep only points inside bbox_lamb93
    semi_pts_out = semi_pts[(semi_pts['x'].between(bbox_xmin_lamb93, bbox_xmax_lamb93)) & (semi_pts['y'].between(bbox_ymin_lamb93, bbox_ymax_lamb93))]

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



