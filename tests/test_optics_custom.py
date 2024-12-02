# from .conftest import skip_s4_test

def test_tmm_profile(pol, angle):
    import numpy as np
    import matplotlib.pyplot as plt
    from solcore import si, material
    from solcore.structure import Layer
    from solcore.solar_cell import SolarCell
    from solcore.optics.tmm import calculate_rat, calculate_absorption_profile, OptiStack

    # wavelengths = np.linspace(300, 767, 468)  # dev1 & dev3 mapbicl
    # wavelengths = np.linspace(300, 900, 601)  # dev2 mapbi3
    wavelengths = np.linspace(300, 800, 501)  # fapbi3

    Ag = material('Ag')()
    Spiro = material('Spiro')()
    # MAPbICl = material('MAPbICl')()
    FAPbI3 = material('FAPbI3')()
    TiO2 = material('TiO2')()
    solar_cell = SolarCell([Layer(material=TiO2, width=si('101nm')),  # remember to revert struct!
                                  Layer(material=FAPbI3, width=si('400nm')),
                                  Layer(material=Spiro, width=si('201nm'))], substrate=Ag)
    # Ag_sd = material('Ag_sd')()
    # NiOx = material('NiOx')()
    # MAPbI3 = material('MAPbI3')()
    # C60 = material('MAPbI3')()
    # solar_cell = SolarCell([Layer(material=NiOx, width=si('21nm')),
    #                               Layer(material=MAPbI3, width=si('500nm')),
    #                               Layer(material=C60, width=si('51nm'))], substrate=Ag_sd)
    # PEDOT = material('PEDOT')()
    # MAPbICl = material('MAPbICl')()
    # PCBM = material('PCBM')()
    # solar_cell = SolarCell([Layer(material=PEDOT, width=si('52nm')),
    #                             Layer(material=MAPbICl, width=si('400nm')),
    #                             Layer(material=PCBM, width=si('62nm'))], substrate=Ag)

    solar_cell_OS = OptiStack(solar_cell, no_back_reflection=False, substrate=solar_cell.substrate)
    tmm_result = calculate_rat(solar_cell_OS, wavelengths, angle, pol, no_back_reflection=False)

    dist = np.loadtxt("x-dev1.csv", delimiter=',')

    tmm_profile = calculate_absorption_profile(solar_cell_OS, wavelengths, no_back_reflection=False,
                                               angle=angle, pol=pol, RAT_out=tmm_result, dist=dist)
    
    np.savetxt("RAT_fapbi3.csv", np.array([wavelengths, tmm_result['R'], tmm_result['A'], tmm_result['T']]).T, delimiter=',')
    np.savetxt("AbsorptionProfile_fapbi3.csv", np.array(tmm_profile['absorption']), delimiter=',')
    plt.figure(1)
    plt.plot(wavelengths, tmm_result['R'], label="Reflection")
    plt.plot(wavelengths, tmm_result['A'], label="Absorption")
    plt.title("Reflection and absorption vs wavelengths")
    plt.legend()
    plt.savefig("RA_fapbi3.png")
    plt.figure(2)
    ax = plt.contourf(tmm_profile['position'], wavelengths, tmm_profile['absorption'], 200)
    plt.xlabel('Position (nm)')
    plt.ylabel('Wavelength (nm)')
    cbar = plt.colorbar()
    cbar.set_label('Absorption (1/nm)')
    plt.savefig("AProfile_fapbi3.png")


def create_custom_materials():
    import os
    from solcore.material_system import create_new_material
    create_new_material(
        "NiOx",
        os.path.expanduser("~/.solcore/NiOx-Material/n.txt"),
        os.path.expanduser("~/.solcore/NiOx-Material/k.txt"),
        overwrite=True,
    )
    create_new_material(
        "MAPbI3",
        os.path.expanduser("~/.solcore/MAPbI3-Material/n.txt"),
        os.path.expanduser("~/.solcore/MAPbI3-Material/k.txt"),
        overwrite=True,
    )
    create_new_material(
        "C60",
        os.path.expanduser("~/.solcore/C60-Material/n.txt"),
        os.path.expanduser("~/.solcore/C60-Material/k.txt"),
        overwrite=True,
    )


if __name__ == "__main__":
    # create_custom_materials()
    test_tmm_profile('u', 0)
