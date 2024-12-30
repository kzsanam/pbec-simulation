from job.diff_all_coupling_one_pump_two_bath_well_multiple_frequency_simulate_job import \
    DiffAllCouplingOnePumpTwoBathWellMultipleFrequencySimulateJob
from job.diff_bath_coupling_one_pump_two_bath_well_multiple_frequency_simulate_job import \
    DiffBathCouplingOnePumpTwoBathWellMultipleFrequencySimulateJob
from job.diff_coupling_one_pump_two_bath_well_multiple_frequency_simulate_job import \
    DiffCouplingOnePumpTwoBathWellMultipleFrequencySimulateJob

if __name__ == "__main__":
    # choose the job you are interested in here

    # simple job will solve ode and print its solution one time
    # job = SingleSimulateJob()

    # will solve ode and print its solution for multiple pumps
    # job = MultiplePumpSimulateJob()

    # will solve ode and print its solution for multiple frequencies
    # job = MultipleFrequencySimulateJob()

    # will solve ode for double well and one bath and plot its solution for multiple frequencies
    # job = WellMultipleFrequencySimulateJob()

    # will solve ode for double well and 2 baths and plot its solution for multiple frequencies
    # job = TwoBathWellMultipleFrequencySimulateJob()

    # will solve ode for double well and 2 baths when pumping only one site
    # and plot its solution for multiple frequencies
    # job = OnePumpTwoBathWellMultipleFrequencySimulateJob()

    # will solve ode for double well and 2 baths with different couplings when pumping only one site
    # and plot its solution for multiple frequencies
    job = DiffCouplingOnePumpTwoBathWellMultipleFrequencySimulateJob()

    # will solve ode for double well and 2 baths with different bath couplings
    # when driving only one site
    # and plot its solution for multiple frequencies
    # job = DiffBathCouplingOnePumpTwoBathWellMultipleFrequencySimulateJob()

    # will solve ode for double well and 2 baths
    # with different photon and bath couplings
    # when driving only one site
    # and plot its solution for multiple frequencies
    # job = DiffAllCouplingOnePumpTwoBathWellMultipleFrequencySimulateJob()

    # run the job
    job.run()
