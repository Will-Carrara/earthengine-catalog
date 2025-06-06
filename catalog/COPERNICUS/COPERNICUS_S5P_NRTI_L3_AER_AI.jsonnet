local id = 'COPERNICUS/S5P/NRTI/L3_AER_AI';
local subdir = 'COPERNICUS';

local ee_const = import 'earthengine_const.libsonnet';
local ee = import 'earthengine.libsonnet';
local spdx = import 'spdx.libsonnet';
local units = import 'units.libsonnet';

local license = spdx.proprietary;

local basename = std.strReplace(id, '/', '_');
local base_filename = basename + '.json';
local self_ee_catalog_url = ee_const.ee_catalog_url + basename;

local s5p_desc = importstr 'COPERNICUS_S5P_description.md';
local COPERNICUS_S5P = import 'COPERNICUS_S5P.libsonnet';

{
  stac_version: ee_const.stac_version,
  type: ee_const.stac_type.collection,
  stac_extensions: [
    ee_const.ext_eo,
  ],
  id: id,
  title: 'Sentinel-5P NRTI AER AI: Near Real-Time UV Aerosol Index',
  'gee:type': ee_const.gee_type.image_collection,
  description: |||
    ### NRTI/L3_AER_AI

    This dataset provides near real-time high-resolution imagery of the UV Aerosol Index
    (UVAI), also called the Absorbing Aerosol Index (AAI).

    The AAI is based on wavelength-dependent changes in Rayleigh scattering in
    the UV spectral range for a pair of wavelengths.  The difference between
    observed and modelled reflectance results in the AAI.  When the AAI is
    positive, it indicates the presence of UV-absorbing aerosols like dust and
    smoke. It is useful for tracking the evolution of episodic aerosol plumes from
    dust outbreaks, volcanic ash, and biomass burning.

    The wavelengths used have very low ozone absorption, so unlike aerosol optical
    thickness measurements, AAI can be calculated in the presence of clouds.
    Daily global coverage is therefore possible.

    For this L3 AER_AI product, the absorbing_aerosol_index is calculated with a
    pair of measurements at the 354 nm and 388 nm wavelengths.

    ### NRTI L3 Product

    To make our NRTI L3 products, we use
    [harpconvert](https://stcorp.github.io/harp/doc/html/harpconvert.html) to grid the data.

    Example harpconvert invocation for one tile:
    ```
    harpconvert --format hdf5 --hdf5-compression 9
    -a 'absorbing_aerosol_index_validity>50;derive(datetime_stop {time});
    bin_spatial(2001, 50.000000, 0.01, 2001, -120.000000, 0.01);
    keep(absorbing_aerosol_index,sensor_altitude,sensor_azimuth_angle,
         sensor_zenith_angle,solar_azimuth_angle,solar_zenith_angle)'
    S5P_NRTI_L2__AER_AI_20181113T080042_20181113T080542_05618_01_010200_20181113T083707.nc
    output.h5
    ```

  ||| + s5p_desc,
  license: license.id,
  links: ee.standardLinks(subdir, id),
  'gee:categories': ['atmosphere'],
  keywords: [
    'aai',
    'aerosol',
    'air_quality',
    'copernicus',
    'esa',
    'eu',
    'knmi',
    'pollution',
    's5p',
    'sentinel',
    'tropomi',
    'uvai',
  ],
  providers: COPERNICUS_S5P.providers(self_ee_catalog_url),
  extent: ee.extent_global('2018-07-10T11:17:44Z', null),
  summaries: {
    'gee:schema': COPERNICUS_S5P.schema(),
    gsd: [
      1113.2,
    ],
    platform: [
      'Sentinel-5P',
    ],
    instruments: [
      'TROPOMI',
    ],
    'eo:bands': [
      {
        name: 'absorbing_aerosol_index',
        description: |||
          A measure of the prevalence of aerosols in the atmosphere.

          The UVAI index is based on spectral contrast in the ultraviolet (UV)
          spectral range for a given wavelength pair, where the difference
          between observed and modeled reflectance results in a residual value.
          When this residual is positive it indicates the presence of
          UV-absorbing aerosols, like dust and smoke, and is often referred
          to as the Absorbing Aerosol Index (AAI). Clouds yield near-zero
          residual values and strongly negative residual values can be
          indicative of the presence of non-absorbing aerosols including
          sulfate aerosols.

          Unlike satellite-based aerosol optical thickness
          measurements, AAI can also be calculated in the presence of clouds
          so that daily, global coverage is possible. This is ideal for tracking
          the evolution of episodic aerosol plumes consisting of desert dust,
          ash from volcanic eruptions, and smoke from biomass burning.

          See further details in the
          [ATBD](https://sentinel.esa.int/documents/247904/2476257/Sentinel-5P-TROPOMI-ATBD-UV-Aerosol-Index.pdf).
        |||,
      },
      {
        name: 'sensor_altitude',
        description: 'Altitude of the satellite with respect to the geodetic sub-satellite point\n(WGS84).',
        'gee:units': units.meter,
      },
    ] + COPERNICUS_S5P.bands_common,
    'gee:visualizations': [
      {
        display_name: 'RGB',
        lookat: {
          lat: 24.27,
          lon: 44.09,
          zoom: 4,
        },
        image_visualization: {
          band_vis: {
            min: [
              -1.0,
            ],
            max: [
              1.5,
            ],
            palette: [
              'black',
              'blue',
              'purple',
              'cyan',
              'green',
              'yellow',
              'red',
            ],
            bands: [
              'absorbing_aerosol_index',
            ],
          },
        },
      },
    ],
    absorbing_aerosol_index: {
      minimum: -25.0,
      maximum: 39.0,
      'gee:estimated_range': true,
    },
    sensor_altitude: {
      minimum: 828543.0,
      maximum: 856078.0,
      'gee:estimated_range': true,
    },
    sensor_azimuth_angle: {
      minimum: -180.0,
      maximum: 180.0,
      'gee:estimated_range': true,
    },
    sensor_zenith_angle: {
      minimum: 0.09,
      maximum: 67.0,
      'gee:estimated_range': true,
    },
    solar_azimuth_angle: {
      minimum: -180.0,
      maximum: 180.0,
      'gee:estimated_range': true,
    },
    solar_zenith_angle: {
      minimum: 8.0,
      maximum: 88.0,
      'gee:estimated_range': true,
    },
  },
  'gee:interval': {
    type: 'revisit_interval',
    unit: 'day',
    interval: 2,
  },
  'gee:terms_of_use': COPERNICUS_S5P.terms_of_use,
}
