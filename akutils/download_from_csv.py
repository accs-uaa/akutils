# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Download Files From CSV
# Author: Timm Nawrocki
# Last Updated: 2025-12-18
# Usage: Must be executed in a Python 3.12+ installation.
# Description: "Download Files From CSV" contacts a server to download a series of files specified in a csv table. The full path to the download must be specified in the table.
# ---------------------------------------------------------------------------

# Define a function to download files from a csv
def download_from_csv(input_table, url_column, download_folder):
    """
    Description: downloads set of files specified in a particular column of a csv table.
    Inputs: input_table -- csv table containing rows for download items.
            url_column -- title for column containing download urls.
            download_folder -- folder to store download results.
    Returned Value: Function returns status messages only. Downloaded data are stored on drive.
    Preconditions: input csv table must be generated from web application tools or manually.
    """

    # Import packages
    import datetime
    import os
    import pandas as pd
    import time
    import requests

    # Import a csv file with download urls
    download_items = pd.read_csv(input_table)

    # Initialize download count
    n = len(download_items[url_column])

    # Loop through urls in the downloadURL column and download
    count = 1
    for url in download_items[url_column]:
        # Define destination file path
        destination_path = os.path.join(download_folder, os.path.split(url)[1])

        # Download file if it does not already exist on local disk
        if os.path.exists(destination_path) == 0:
            print(f'Downloading of {count} of {n} files...')
            try:
                iteration_start = time.time()
                # Determine download size
                response = requests.get(url, stream=True)
                total_bytes = int(response.headers.get('content-length', 0))
                total_mb = round((total_bytes / (1024 * 1024)), 0)

                # Print download size
                if total_bytes == 0:
                    print('\tCould not determine file size.')
                elif total_mb == 0:
                    print(f'\tDownload size is {total_bytes} bytes.')
                else:
                    print(f'\tDownload size is {total_mb} mb.')

                # Download file in chunks
                with open(destination_path, "wb") as file:
                    progress_percentage = 0
                    cumulative_bytes = 0
                    for chunk in response.iter_content(chunk_size=4096):
                        cumulative_bytes += len(chunk)
                        file.write(chunk)

                        # Calculate progress percentage
                        if total_bytes > 0:
                            cumulative_percentage = round(((cumulative_bytes / total_bytes) * 100), 0)
                            if cumulative_percentage > progress_percentage:
                                print(f'\t{cumulative_percentage}%')
                            progress_percentage = round(((cumulative_bytes / total_bytes) * 100), 0)

                # End timing
                iteration_end = time.time()
                iteration_elapsed = int(iteration_end - iteration_start)
                iteration_success_time = datetime.datetime.now()
                # Report success
                print(
                    f'Completed at {iteration_success_time.strftime("%Y-%m-%d %H:%M")} (Elapsed time: {datetime.timedelta(seconds=iteration_elapsed)})')
                print('----------')
            except:
                print(f'File {count} of {n} not available for download. Check url.')
                print('----------')
        else:
            print(f'\tFile {count} of {n} already exists...')
            print('\t----------')
        # Increase counter
        count += 1
