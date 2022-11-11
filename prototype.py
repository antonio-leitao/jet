from tqdm import trange, tqdm
import time

##GREEN!!!!: #179883

print("\nRunning tests")
progress_bar = tqdm(
    ["a", "b", "c", "d", "e"],
    bar_format="{l_bar}{bar:50}| {n_fmt}/{total_fmt}",
    leave=False,
    position=0,
    colour="#E01563",
    postfix="",
)


# print('\n')


with tqdm(total=5, position=1, bar_format="{desc}", desc="All tests passed!") as desc:
    for i in progress_bar:
        desc.set_description(f"Found {i} tests failed and {3} warnings out of {100}")

        # progress_bar.write(f"Test: {i} [PASSED]") #verbose option
        time.sleep(1)


var = 3
another = 5
print(3 + 5)
