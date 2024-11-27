def chunk_iterator(reader, chunk_size=100):
    chunk = []
    for row in reader:
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []

        chunk.append(row)
    yield chunk
