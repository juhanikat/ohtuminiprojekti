"""
Interaction file for index.py generated by chatGPT.

Used by robots.
"""

import os
import subprocess
import sys
import time


def interact_with_index(robot_inputs):
    # Set the current working directory to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_dir = os.path.join(script_dir, "..")
    index_dir = os.path.abspath(index_dir)
    os.chdir(index_dir)

    output = None
    with subprocess.Popen(['python', 'index.py'],
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          text=True) as process:

        # Wait a bit for the initial output
        time.sleep(.2)

        # Send inputs to the program
        for robot_input in robot_inputs:
            process.stdin.write(robot_input + '\n')
            process.stdin.flush()
            time.sleep(.2)  # Adjust as needed

        # Close stdin, read output, and wait for the process to exit
        process.stdin.close()
        output = process.stdout.read()
        process.wait()

    return output


if __name__ == "__main__":
    inputs = sys.argv[1:]  # Get inputs passed as command-line arguments
    print(interact_with_index(inputs))
