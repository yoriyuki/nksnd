from config import parallel_config

iteration = 30
gaussian = 1
tolerance = 0
unknownword_threshold = 1
eta = 0.1
regularization_factor = eta * 0.0001 * parallel_config.chunk_size * parallel_config.processes
