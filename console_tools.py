import time

# Print iterations progress
def print_progress_bar (start_time, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    progress_time = round(time.time() - start_time, 3)
    print(f'\r{prefix} |{bar}| {percent}% {suffix} - {progress_time} seconds', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()