from job.multiple_pump_simulate_job import MultiplePumpSimulateJob
from job.well_multiple_frequency_simulate_job import WellMultipleFrequencySimulateJob
from src.job.multiple_frequency_simulate_job import MultipleFrequencySimulateJob
from src.job.single_simulate_job import SingleSimulateJob

if __name__ == "__main__":
    # choose the job you are interested in here
    # simple job will solve ode and print its solution one time
    # job = SingleSimulateJob()

    # will solve ode and print its solution for multiple pumps
    # job = MultiplePumpSimulateJob()

    # will solve ode and print its solution for multiple frequencies
    # job = MultipleFrequencySimulateJob()

    # will solve ode and print its solution for multiple frequencies
    job = WellMultipleFrequencySimulateJob()

    # run the job
    job.run()
