# from .conftest import skip_s4_test

def test_tmm_profile(pol, angle):
    import numpy as np
    import matplotlib.pyplot as plt
    from solcore import si, material
    from solcore.structure import Layer
    from solcore.solar_cell import SolarCell
    from solcore.optics.tmm import calculate_rat, calculate_absorption_profile, OptiStack

    Spiro = material('Spiro')()
    MAPbICl = material('MAPbICl')()
    TiO2 = material('TiO2')()
    Ag = material('Ag')()

    wavelengths = np.linspace(300, 767, 468)

    solar_cell = SolarCell([Layer(material=Spiro, width=si('201nm')),
                                  Layer(material=MAPbICl, width=si('400nm')),
                                  Layer(material=TiO2, width=si('101nm'))], substrate=Ag)

    solar_cell_OS = OptiStack(solar_cell, no_back_reflection=True, substrate=solar_cell.substrate)
    tmm_result = calculate_rat(solar_cell_OS, wavelengths, angle, pol, no_back_reflection=True)

    dist = np.loadtxt("par.xx.csv", delimiter=',')

    tmm_profile = calculate_absorption_profile(solar_cell_OS, wavelengths, no_back_reflection=True,
                                               angle=angle, pol=pol, RAT_out=tmm_result, dist=dist)
    
    # np.savetxt("RAT1.csv", np.array([wavelengths, tmm_result['R'], tmm_result['A'], tmm_result['T']]), delimiter=',')
    np.savetxt("AbsorptionProfile.csv", np.array(tmm_profile['absorption']), delimiter=',')
    # plt.plot(wavelengths, tmm_result['R'], label="Reflection")
    # plt.plot(wavelengths, tmm_result['A'], label="Absorption")
    # plt.title("Reflection and absorption vs wavelengths")
    # plt.legend()
    # plt.savefig("RA1_dev1.png")
    # plt.figure(1)
    ax = plt.contourf(tmm_profile['position'], wavelengths, tmm_profile['absorption'], 200)
    plt.xlabel('Position (nm)')
    plt.ylabel('Wavelength (nm)')
    cbar = plt.colorbar()
    cbar.set_label('Absorption (1/nm)')
    plt.savefig("AProfile1_dev1.png")


def create_custom_materials():
    import os
    from solcore.material_system import create_new_material
    create_new_material(
        "Spiro",
        os.path.expanduser("~/.solcore/Spiro-Material/n.txt"),
        os.path.expanduser("~/.solcore/Spiro-Material/k.txt"),
        overwrite=True,
    )
    create_new_material(
        "MAPbICl",
        os.path.expanduser("~/.solcore/MAPbICl-Material/n.txt"),
        os.path.expanduser("~/.solcore/MAPbICl-Material/k.txt"),
        overwrite=True,
    )
    create_new_material(
        "TiO2",
        os.path.expanduser("~/.solcore/TiO2-Material/n.txt"),
        os.path.expanduser("~/.solcore/TiO2-Material/k.txt"),
        overwrite=True,
    )


if __name__ == "__main__":
    # create_custom_materials()
    test_tmm_profile('u', 0)
