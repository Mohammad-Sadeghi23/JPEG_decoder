rlc_data = [
    -26,
    (0, -3), (1, -3), (0, -2), (0, -6), (0, 2),
    (0, -4), (0, 1), (0, -3), (0, 1), (0, 1),
    (0, 5), (0, 1), (0, 2), (0, -1), (0, 2),
    (5, -1), (0, -1), (0, 0)
]

def decode_rlc(rlc):
    result = []

    # First value = DC coefficient
    result.append(rlc[0])

    # Process the rest
    for item in rlc[1:]:
        
        # Unpack the tuple into seperate run and value variables
        run, value = item

        # End of block
        if (run, value) == (0, 0):
            break

        # Add zeros
        result.extend([0] * run)

        # Add the value
        result.append(value)

    # Pad with zeros to reach 64 values
    while len(result) < 64:
        result.append(0)

    return result

decoded = decode_rlc(rlc_data)

print(len(decoded))   # should be 64
print(decoded)