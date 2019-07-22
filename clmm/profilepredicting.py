"""@file.py profilepredicting.py
Functions to compute profiles from theory.  Default is NFW.
"""
import numpy as np
import pyccl as ccl
import cluster_toolkit as ct

# AIM: I'm removing these hardcoded things from the notebook.
# # Define CCL cosmology object
# cosmo_ccl = ccl.Cosmology(Omega_c=0.27, Omega_b=0.045, h=0.67, A_s=2.1e-9, n_s=0.96)

# # Select density profile and profile parametrization options
# density_profile_parametrization = 'nfw'
# mass_Delta = 200
# cluster_mass = 1.e15
# cluster_concentration = 4

# AIM: standard nomenclature for verbs
# compute for heavy computation
# calculate for straightforward calculations
# get for lookup existing value

def get_Om(cosmo):
    '''
    Retrieves matter energy density from cosmology

    Parameters
    ----------
    cosmo : [type(cosmo)]
        CCL Cosmology object

    Returns
    -------
    cosmo : [type(cosmo)]
        modified CCL Cosmology object
    '''
    cosmo['Omega_m'] = cosmo['Omega_c'] + cosmo['Omega_b']
    return cosmo

def get_3d_density_profile(r3d, mdelta, cdelta, cosmo, Delta=200, halo_profile_parameterization='nfw'):
    '''
    Computes the 3d density profile:
    $\rho(r) = ...$

    Parameters
    ----------
    r3d : array-like, float
        The radial positions in Mpc/h.
    r_proj : array-like
        The projected radial positions in Mpc/h.
    mdelta : float
        Galaxy cluster mass in Msun/h.
    cdelta : float
        Galaxy cluster NFW concentration.
    cosmo : [type(cosmo)]
        CCL Cosmology object
    Delta : int, optional
        Mass overdensity definition; defaults to 200.
    halo_profile_parameterization :obj:`str`, optional
        Profile model parameterization, with the following supported options:
        `nfw` (default) - [insert citation here]
    z_src_model : `str`, optional
        Source redshift model, with the following supported options:
        `single_plane` (default) - all sources at one redshift
        `known_z_src` - known individual source galaxy redshifts, e.g. discrete case
        `z_src_distribution` - known source redshift distribution, e.g. continuous case requiring integration.

    Returns
    -------
    rho : array-like, float
        3-dimensional mass density profile

    Notes
    -----
    AIM: We should only require arguments that are necessary for all profiles and use another structure to take the arguments necessary for specific profiles.
    '''
    cosmo = get_Om(cosmo)

    if halo_profile_parameterization=='nfw':
        rho = ct.density.rho_nfw_at_r(r3d, mdelta, cdelta, cosmo['Omega_m'] delta=Delta)
        return rho
    else:
        pass

def calculate_surface_density(r_proj, mdelta, cdelta, cosmo, Delta=200, halo_profile_parameterization='nfw'):
    '''
    Computes the surface density profile:
    $\Sigma = ...$

    Parameters
    ----------
    r_proj : array-like
        The projected radial positions in Mpc/h.
    mdelta : float
        Galaxy cluster mass in Msun/h.
    cdelta : float
        Galaxy cluster NFW concentration.
    cosmo : [type(cosmo)]
        CCL Cosmology object
    Delta : int, optional
        Mass overdensity definition; defaults to 200.
    halo_profile_parameterization : str, optional
        Profile model parameterization, with the following supported options:
        `nfw` (default) - [insert citation here]
    z_src_model : str, optional
        Source redshift model, with the following supported options:
        `single_plane` (default) - all sources at one redshift
        `known_z_src` - known individual source galaxy redshifts, e.g. discrete case
        `z_src_distribution` - known source redshift distribution, e.g. continuous case requiring integration.

    Returns
    -------
    sigma : array-like, float
        Surface density, Sigma.

    Notes
    -----
    AIM: We should only require arguments that are necessary for all profiles and use another structure to take the arguments necessary for specific profiles.
    '''
    Om_m = cosmo['Omega_c'] + cosmo['Omega_b']

    if halo_profile_parameterization=='nfw':
        sigma = ct.deltasigma.Sigma_nfw_at_R(r_proj, mdelta, cdelta, Om_m, delta=Delta)
        return sigma
    else:
        #return ct.Sigma_at_R(r_proj, mdelta, cdelta, cosmo.Omegam, delta=Delta)
        pass

def calculate_excess_surface_density(r_proj, mdelta, cdelta, cosmo, Delta=200, halo_profile_parameterization='nfw'):
    '''
    Computes the excess surface density profile:
    $\Delta\Sigma = ...$

    Parameters
    ----------
    r_proj : array-like
        The projected radial positions in Mpc/h.
    mdelta : float
        Galaxy cluster mass in Msun/h.
    cdelta : float
        Galaxy cluster NFW concentration.
    cosmo : [type(cosmo)]
        CCL Cosmology object
    Delta : int, optional
        Mass overdensity definition; defaults to 200.
    halo_profile_parameterization :obj:`str`, optional
        Profile model parameterization, with the following supported options:
        `nfw` (default) - [insert citation here]
    z_src_model : `str`, optional
        Source redshift model, with the following supported options:
        `single_plane` (default) - all sources at one redshift
        `known_z_src` - known individual source galaxy redshifts, e.g. discrete case
        `z_src_distribution` - known source redshift distribution, e.g. continuous case requiring integration.

    Returns
    -------
    deltsigma : array-like, float
        Excess surface density, DeltaSigma.
    '''
    Om_m = cosmo['Omega_c'] + cosmo['Omega_b']

    if halo_profile_parameterization == 'nfw':

        Sigma = ct.deltasigma.Sigma_nfw_at_R(r_proj, mdelta, cdelta, Om_m, delta=Delta)
        # ^ Note: Let's not use this naming convention when transfering ct to ccl....
        deltasigma = ct.deltasigma.DeltaSigma_at_R(r_proj, r_proj, Sigma, mdelta, cdelta, Om_m, delta=Delta)
        return deltasigma
    else:
        pass


def _comoving_angular_distance_aexp1_aexp2(cosmo, aexp1, aexp2):
    '''

    This is a monkey-patched method to calculate d_LS (angular
    distance between lens and source) because CCL does not yet have
    this PR completed.  Temporarily using the astropy implementation.

    # AIM: needs a docstring for args

    '''
    z1 = 1. / aexp1 - 1.
    z2 = 1. / aexp2 - 1.
    # from astropy.cosmology import FlatLambdaCDM
    # cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
    d_a = cosmo.angular_diameter_distance_z1z2(z1, z2).value
    return d_a



def get_critical_surface_density(cosmo, z_cluster, z_source):
    '''
    Computes the tangential shear profile:
    $\gamma_t = ...$
    # Shouldn't this be critical surface density...?

    Parameters
    ----------
    cosmo : [type(cosmo)]
        CCL Cosmology object
    z_cluster : float
        Galaxy cluster redshift
    z_source : float
        Background source galaxy redshift

    Returns
    -------
    sigmacrit : float
        Cosmology-dependent critical surface density

    Notes
    -----
    We will need gamma inf and kappa inf for alternative z_src_models using Beta_s
    '''
    c = ccl.physical_constants.CLIGHT
    G = ccl.physical_constants.GNEWT
    aexp_cluster = 1. / (1. + z_cluster)
    aexp_src = 1. / (1. + z_source)
    d_l = ccl.comoving_angular_distance(cosmo, aexp_cluster)
    d_s = ccl.comoving_angular_distance(cosmo, aexp_src)
    d_ls = _comoving_angular_distance_aexp1_aexp2(cosmo, aexp_cluster, aexp_src)

    # will need to deal with units: distances in Mpc and some CCL constants in SI
    sigmacrit = d_s / (d_l * d_ls) * c * c / (4 * np.pi * G)
    return sigmacrit

def compute_tangential_shear_profile(r_proj, mdelta, cdelta, z_cluster, z_source, cosmo, Delta=200,
                                     halo_profile_parameterization='nfw',
                                     z_src_model='single_plane'):
    '''
    Computes the tangential shear profile:
    $\gamma_t = ...$

    Parameters
    ----------
    r_proj : array-like
        The projected radial positions in Mpc/h.
    mdelta : float
        Galaxy cluster mass in Msun/h.
    cdelta : float
        Galaxy cluster NFW concentration.
    z_cluster : float
        Galaxy cluster redshift
    z_source : float
        Background source galaxy redshift
    cosmo : [type(cosmo)]
        CCL Cosmology object
    Delta : int, optional
        Mass overdensity definition.  Defaults to 200.
    halo_profile_parameterization :obj:`str`, optional
        Profile model parameterization that we wish to use, with the following supported options:
        `nfw` (default) - [insert citation here]
    z_src_model : str, optional
        Source redshift model, with the following supported options:
        `single_plane` (default) - all sources at one redshift
        `known_z_src` - known individual source galaxy redshifts, e.g. discrete case
        `z_src_distribution` - known source redshift distribution, e.g. continuous case requiring integration.

    Returns
    -------
    gammat : array-like, float
        tangential shear profile

    Notes
    -----
    We will need gamma inf and kappa inf for alternative z_src_models using Beta_s.
    AIM: Don't we want to raise exceptions rather than errors here?
    '''
    delta_sigma = calculate_excess_surface_density(r_proj, mdelta, cdelta, cosmo, Delta=Delta,
                                                   halo_profile_parameterization=halo_profile_parameterization)

    if z_src_model == 'single_plane':
        sigma_c = get_critical_surface_density(cosmo, z_cluster, z_source)
        gammat = delta_sigma / sigma_c
        return gammat
    elif z_src_model == 'known_z_src': # Discrete case
        NotImplementedError('Need to implemnt Beta_s functionality, or average delta_sigma/sigma_c gamma_t = Beta_s*gamma_inf')
    elif z_src_model == 'z_src_distribution' : # Continuous ( from a distribution) case
        NotImplementedError('Need to implement Beta_s calculation from integrating distribution of redshifts in each radial bin')

def compute_convergence_profile(r_proj, mdelta, cdelta, z_cluster, z_source, cosmo, Delta=200,
                                     halo_profile_parameterization='nfw',
                                    z_src_model='single_plane'):
    '''
    Computes the mass convergence profile:
    $\kappa = ...$

    Parameters
    ----------
    r_proj : array-like
        The projected radial positions in Mpc/h.
    mdelta : float
        Galaxy cluster mass in Msun/h.
    cdelta : float
        Galaxy cluster NFW concentration.
    z_cluster : float
        Galaxy cluster redshift
    z_source : float
        Background source galaxy redshift
    cosmo : [type(cosmo)]
        CCL Cosmology object
    Delta : int, optional
        Mass overdensity definition.  Defaults to 200.
    halo_profile_parameterization :obj:`str`, optional
        Profile model parameterization that we wish to use, with the following supported options:
        `nfw` (default) - [insert citation here]
    z_src_model : str, optional
        Source redshift model, with the following supported options:
        `single_plane` (default) - all sources at one redshift
        `known_z_src` - known individual source galaxy redshifts, e.g. discrete case
        `z_src_distribution` - known source redshift distribution, e.g. continuous case requiring integration.

    Returns
    -------
    kappa : array-like, float
        Mass convergence profile, kappa.

    Notes
    -----
    AIM: Don't we want to raise exceptions rather than errors here?
    '''
    sigma = calculate_surface_density(r_proj, mdelta, cdelta, cosmo, Delta=Delta,
                                                      halo_profile_parameterization=halo_profile_parameterization)

    if z_src_model == 'single_plane':
        sigma_c = get_critical_surface_density(cosmo, z_cluster, z_source)
        kappa = sigma / sigma_c
        return kappa
    elif z_src_model == 'known_z_src': # Discrete case
        NotImplementedError('Need to implemnt Beta_s functionality, or average sigma/sigma_c kappa_t = Beta_s*kappa_inf')
    elif z_src_model == 'z_src_distribution' : # Continuous ( from a distribution) case
        NotImplementedError('Need to implement Beta_s calculation from integrating distribution of redshifts in each radial bin')

def compute_reduced_tangential_shear_profile(r_proj, mdelta, cdelta, z_cluster, z_source, cosmo, Delta=200,
                                             halo_profile_parameterization='nfw',
                                                z_src_model='single_plane'):
    '''
    Computes the reduced tangential shear profile:
    $g_t = \frac{\\gamma_t}{1-\\kappa}$.

    Parameters
    ----------
    r_proj : array-like
        The projected radial positions in Mpc/h.
    mdelta : float
        Galaxy cluster mass in Msun/h.
    cdelta : float
        Galaxy cluster NFW concentration.
    z_cluster : float
        Galaxy cluster redshift
    z_source : float
        Background source galaxy redshift
    cosmo : [type(cosmo)]
        CCL Cosmology object
    Delta : int, optional
        Mass overdensity definition.  Defaults to 200.
    halo_profile_parameterization :obj:`str`, optional
        Profile model parameterization that we wish to use, with the following supported options:
        `nfw` (default) - [insert citation here]
    z_src_model : str, optional
        Source redshift model, with the following supported options:
        `single_plane` (default) - all sources at one redshift
        `known_z_src` - known individual source galaxy redshifts, e.g. discrete case
        `z_src_distribution` - known source redshift distribution, e.g. continuous case requiring integration.

    Returns
    -------
    gt : array-like, float
        Reduced tangential shear.

    Notes
    -----
    AIM: Don't we want to raise exceptions rather than errors here?
    '''
    if z_src_model == 'single_plane':
        kappa = compute_convergence_profile(r_proj, mdelta, cdelta, z_cluster, z_source, cosmo, Delta,
                                         halo_profile_parameterization,
                                        z_src_model)
        gamma_t = compute_tangential_shear_profile(r_proj, mdelta, cdelta, z_cluster, z_source, cosmo, Delta,
                                         halo_profile_parameterization,
                                        z_src_model)
        gt = gamma_t / (1 - kappa)
        return gt
    elif z_src_model == 'known_z_src': # Discrete case
        NotImplementedError('Need to implemnt Beta_s functionality, or average sigma/sigma_c kappa_t = Beta_s*kappa_inf')
    elif z_src_model == 'z_src_distribution' : # Continuous ( from a distribution) case
        NotImplementedError('Need to implement Beta_s and Beta_s2 calculation from integrating distribution of redshifts in each radial bin')


# AIM: Let's use these as a starting point for unit tests
# # Quick test of functions
#
# r3d = np.logspace(-2,2,100)
#
# rho = get_3d_density_profile(r3d,mdelta=cluster_mass, cdelta=cluster_concentration, cosmo=cosmo_ccl)
#
# Sigma = calculate_surface_density(r3d, cluster_mass, cluster_concentration, cosmo=cosmo_ccl, Delta=200,
#                                   halo_profile_parameterization='nfw')
#
# DeltaSigma = calculate_excess_surface_density(r3d, cluster_mass, cluster_concentration, cosmo=cosmo_ccl, Delta=200,
#                                               halo_profile_parameterization='nfw')
#
# Sigmac = get_critical_surface_density(cosmo_ccl, z_cluster=1.0, z_source=2.0)
#
# gammat = compute_tangential_shear_profile(r3d, mdelta=cluster_mass, cdelta=cluster_concentration, z_cluster=1.0,
#                                           z_source=2.0, cosmo=cosmo_ccl, Delta=200,
#                                           halo_profile_parameterization='nfw', z_src_model='single_plane')
#
# kappa = compute_convergence_profile(r3d, mdelta=cluster_mass, cdelta=cluster_concentration,
#                             z_cluster=1.0, z_source=2.0,
#                                  cosmo=cosmo_ccl, Delta=200,
#                                      halo_profile_parameterization='nfw',
#                                     z_src_model='single_plane')
#
# gt = compute_reduced_tangential_shear_profile(r3d, mdelta=cluster_mass, cdelta=cluster_concentration,
#                                          z_cluster=1.0, z_source=2.0, cosmo=cosmo_ccl, Delta=200,
#                                          halo_profile_parameterization='nfw', z_src_model='single_plane')
#
#
# import matplotlib.pyplot as plt
#
# def plot_profile(r, profile_vals, profile_label='rho'):
#     plt.loglog(r, profile_vals)
#     plt.xlabel('r [Mpc]', fontsize='xx-large')
#     plt.ylabel(profile_label, fontsize='xx-large')
#
#
#
# def check_import3():
#     print("Imported profilepredicting.py")
