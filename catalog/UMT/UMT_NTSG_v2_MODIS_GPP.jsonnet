local id = 'UMT/NTSG/v2/MODIS/GPP';
local subdir = 'UMT';

local ee_const = import 'earthengine_const.libsonnet';
local ee = import 'earthengine.libsonnet';
local spdx = import 'spdx.libsonnet';

local license = spdx.proprietary;

local basename = std.strReplace(id, '/', '_');
local base_filename = basename + '.json';
local self_ee_catalog_url = ee_const.ee_catalog_url + basename;

{
  stac_version: ee_const.stac_version,
  type: ee_const.stac_type.collection,
  stac_extensions: [
    ee_const.ext_eo,
    ee_const.ext_sci,
    ee_const.ext_ver,
  ],
  id: id,
  title: 'MODIS Gross Primary Production CONUS',
  version: '0.2.0',
  'gee:type': ee_const.gee_type.image_collection,
  description: |||
    The MODIS Gross Primary Production (GPP) CONUS dataset estimates GPP using
    MODIS Surface Reflectance for CONUS. GPP is the amount of
    carbon captured by plants in an ecosystem and is an essential component in
    the calculations of Net Primary Production (NPP). GPP is calculated using the
    MOD17 algorithm (see [MOD17 User
    Guide](https://www.ntsg.umt.edu/files/modis/MOD17UsersGuide2015_v3.pdf)) with
    MODIS Surface Reflectance, gridMET, and the National Land Cover Database.
  |||,
  license: license.id,
  links: ee.standardLinks(subdir, id),
  'gee:categories': ['plant-productivity'],
  keywords: [
    '8_day',
    'conus',
    'gpp',
    'gridmet_derived',
    'mod09q1',
    'mod17',
    'modis',
    'nlcd_derived',
    'photosynthesis',
    'production',
    'productivity',
  ],
  providers: [
    ee.producer_provider('University of Montana Numerical Terradynamic Simulation Group (NTSG)', 'https://www.ntsg.umt.edu/project/landsat/landsat-productivity.php'),
    ee.host_provider(self_ee_catalog_url),
  ],
  extent: ee.extent(-124.84, 24.42, -64.82, 49.72,
                    '2001-01-01T00:00:00Z', null),
  summaries: {
    gsd: [
      250.0,
    ],
    platform: [
      'Terra',
    ],
    instruments: [
      'MODIS',
    ],
    'eo:bands': [
      {
        name: 'GPP',
        description: '8-day gross primary production',
        'gee:units': 'kg*C/m^2/8-day',
        'gee:scale': 0.0001,
      },
      {
        name: 'QC',
        description: |||
          Indicates if the original NDVI value was adjusted through the
          smoothing algorithm. 0 denotes the value was not adjusted. 1 indicates
          the value was adjusted.
        |||,
      },
    ],
    'gee:visualizations': [
      {
        display_name: 'GPP',
        lookat: {
          lat: 37.07,
          lon: -94.83,
          zoom: 5,
        },
        image_visualization: {
          band_vis: {
            min: [
              0.0,
            ],
            max: [
              1000.0,
            ],
            palette: [
              'bbe029',
              '0a9501',
              '074b03',
            ],
            bands: [
              'GPP',
            ],
          },
        },
      },
    ],
    GPP: {
      minimum: 0.0,
      maximum: 65535.0,
      'gee:estimated_range': false,
    },
    QC: {
      minimum: 0.0,
      maximum: 1.0,
      'gee:estimated_range': false,
    },
  },
  'sci:citation': |||
    Robinson, N.P., B.W. Allred, W.K. Smith, M.O. Jones, A. Moreno, T.A.
    Erickson, D.E. Naugle, and S.W. Running. 2018. Terrestrial primary
    production for the conterminous United States derived from Landsat 30 m and
    MODIS 250 m. Remote Sensing in Ecology and Conservation.
    [doi:10.1002/rse2.74](https://doi.org/10.1002/rse2.74)
  |||,
  'gee:interval': {
    type: 'cadence',
    unit: 'day',
    interval: 8,
  },
  'gee:terms_of_use': |||
    This work is in the public domain and is free of known copyright
    restrictions. Users should properly cite the source used in the creation of
    any reports and publications resulting from the use of this dataset and note
    the date when the data was acquired.
  |||,
  'gee:user_uploaded': true,
}
