from data_generation.h_function import generate_data


def test_generate_data():
  assert len(generate_data(records_generate=20)) == 20