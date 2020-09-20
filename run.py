import cProfile
import importlib
import timeit

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        sol = importlib.import_module(sys.argv[1].replace(".py", ""))

        file_location = sys.argv[2].strip()
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()

        cProfile.run("print(sol.solve_it(input_data))")
        num_run = [1, 3, 5, 10]
        for i in num_run:
            avg = (
                timeit.timeit(
                    "sol.solve_it(input_data)", number=i, globals=globals()
                )
                / i
            )
            print(f"Average of {i} run(s): {avg}")
