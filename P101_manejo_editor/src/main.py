import glob
import os.path
import shutil
import time
from pathlib import Path

from P101_manejo_editor.src.helpers.mapper import mapper

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_FOLDER = ACTIVITY_DIR / "data"
INPUT_FOLDER = ACTIVITY_DIR / "temp" / "input"
OUTPUT_FOLDER = ACTIVITY_DIR / "temp" / "output"
SUBMISSION_FOLDER = ACTIVITY_DIR / "submission"

# La carpeta input/ debe existir y estar vacia.
# -----------------------------------------------------------------------------

def clear_folder(folder):
    for file in glob.glob(f"{folder}/*"):
        os.remove(file)

def initialize_folder(folder):
    if os.path.exists(folder):
        clear_folder(folder)
    else:
        os.makedirs(folder)

def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)

def generate_files_copies(n):
    for file in glob.glob(f"{DATA_FOLDER}/*"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(1, n + 1):
            raw_filename_with_extension = os.path.basename(file)

            raw_filename_without_extension = os.path.splitext(raw_filename_with_extension)[
            0
        ]

            new_filename = f"{raw_filename_without_extension}_{i:05d}.txt"

            with open(f"{INPUT_FOLDER}/{new_filename}", "w", encoding="utf-8") as f2:
                f2.write(text)

def reducer(pairs_sequence):
    result = []
    for key, value in pairs_sequence:
        if result and result[-1][0] == key:
            result[-1] = (key, result[-1][1] + value)
        else:
            result.append((key, value))
    return result



def hadoop(input_folder,output_folder, mapper,reducer):
    def read_records_from_input(input_folder):
        sequence = []
        files = glob.glob(f"{input_folder}/*")
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    sequence.append((file, line))
        return sequence
    def shuffle_and_sort(pairs_sequence):
        pairs_sequence = sorted(pairs_sequence)
        return pairs_sequence
    def save_results_to_output(result):
        with open(f"{output_folder}/part-00000", "w", encoding="utf-8") as f:
            for key, value in result:
                f.write(f"{key}\t{value}\n")
    def create_success_file():
        with open(f"{output_folder}/_SUCCESS", "w", encoding="utf-8") as f:
            f.write("")

    def fail_if_output_exists():
        if os.path.exists(output_folder):
            raise Exception(f"Output folder '{output_folder}' alrady exists. Please delete it before running the job.")


    fail_if_output_exists()
    sequence = read_records_from_input(input_folder)
    pairs_sequence = mapper(sequence)
    pairs_sequence = shuffle_and_sort(pairs_sequence)
    result = reducer(pairs_sequence)
    initialize_folder(output_folder)
    save_results_to_output(result)
    create_success_file()




n = 1000

initialize_folder(INPUT_FOLDER)
generate_files_copies(n)

start_time = time.time()

hadoop(INPUT_FOLDER, OUTPUT_FOLDER, mapper, reducer)

end_time = time.time()
print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")