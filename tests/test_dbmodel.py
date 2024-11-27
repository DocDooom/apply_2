# from data_generation.generate_data import generate_csv
# import numpy as np
#
#
# def test_generate_csv(tmpdir):
#     temp_file = tmpdir.join("temp.csv")
#     records_to_gen = np.random.randint(10, high=1000)
#     print(records_to_gen)
#     output_of_func = generate_csv(temp_file.strpath, records_generate=records_to_gen)
#     assert len(output_of_func) == records_to_gen
#     assert (len(temp_file.read().split("\n")) - 2) == (len(output_of_func))
#
#
# def test_square():
#     pass
