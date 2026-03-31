import math


rlc_data = [
    -26,
    (0, -3), (1, -3), (0, -2), (0, -6), (0, 2),
    (0, -4), (0, 1), (0, -3), (0, 1), (0, 1),
    (0, 5), (0, 1), (0, 2), (0, -1), (0, 2),
    (5, -1), (0, -1), (0, 0)
]

# Step 1
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


# Step 2
def inverse_zigzag(vector):
    zigzag_index = [
        (0,0),
        (0,1),(1,0),
        (2,0),(1,1),(0,2),
        (0,3),(1,2),(2,1),(3,0),
        (4,0),(3,1),(2,2),(1,3),(0,4),
        (0,5),(1,4),(2,3),(3,2),(4,1),(5,0),
        (6,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,6),
        (0,7),(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),(7,0),
        (7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7),
        (2,7),(3,6),(4,5),(5,4),(6,3),(7,2),
        (7,3),(6,4),(5,5),(4,6),(3,7),
        (4,7),(5,6),(6,5),(7,4),
        (7,5),(6,6),(5,7),
        (6,7),(7,6),
        (7,7)
    ]

    matrix = [[0 for _ in range(8)] for _ in range(8)]

    for idx, (i, j) in enumerate(zigzag_index):
        matrix[i][j] = vector[idx]

    return matrix


# Step 3
def multiply_luminance(matrix):

    luminance_table = [[16, 11, 10, 16, 24, 40, 51, 61],
                       [12, 12, 14, 19, 26, 58, 60, 55],
                       [14, 13, 16, 24, 40, 57, 69, 56],
                       [14, 17, 22, 29, 51, 87, 80, 62],
                       [18, 22, 37, 56, 68, 109, 103, 77],
                       [24, 35, 55, 64, 81, 104, 113, 92],
                       [49, 64, 78, 87, 103, 121, 120, 101],
                       [72, 92, 95, 98, 112, 100, 103, 99]]
    
    for i in range(8):
        for j in range(8):
            matrix[i][j] *= luminance_table[i][j]


# Step 4
def twod_inv_disc(matrix):

    result = [[0 for _ in range(8)] for _ in range(8)]

    for i in range(8):
        for j in range(8):

            sum_value = 0

            for u in range(8):
                for v in range(8):

                    Cu = math.sqrt(2)/2 if u == 0 else 1
                    Cv = math.sqrt(2)/2 if v == 0 else 1

                    CuCv = (Cu * Cv) / 4

                    cos1 = math.cos(((2*i + 1) * (u * math.pi)) / 16)
                    cos2 = math.cos(((2*j + 1) * (v * math.pi)) / 16)

                    sum_value += CuCv * cos1 * cos2 * matrix[u][v]

            result[i][j] = sum_value

    return result

# Step 5
def scale_to_0_255(matrix):
    for i in range(8):
        for j in range(8):
            matrix[i][j] += 128

    return matrix




decoded = decode_rlc(rlc_data)

print("Decoded:")
print(decoded)
print()

matrix = inverse_zigzag(decoded)

print("Zigzag:")
for row in matrix:
      print(row)
print()

multiply_luminance(matrix)

idct_result = twod_inv_disc(matrix)

# Checkpoint
print("Checkpoint:")
for row in idct_result:
    print([round(x) for x in row])
print()

# Final
print("Final:")
final_result = scale_to_0_255(idct_result)

for row in final_result:
    print([round(x) for x in row])
