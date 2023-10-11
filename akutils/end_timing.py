def end_timing(iteration_start):
    """
    Description: calculates the amount of time that a process took
    Inputs: 'iteration_start' -- a time captured using time.time()
    Returned Value: no return
    Preconditions: requires datetime and time
    """

    # Import packages
    import datetime
    import time

    # End timing
    iteration_end = time.time()
    iteration_elapsed = int(iteration_end - iteration_start)
    iteration_success_time = datetime.datetime.now()

    # Report success
    print(
        f'Completed at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
    print('----------')
