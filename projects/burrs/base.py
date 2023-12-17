from build123d import Pos, Box, fillet, Axis


def burr_piece(size, blocks):
    boxes = []
    for z, x_blocks in enumerate(blocks):
        for x, y_blocks in enumerate(x_blocks):
            for y, block in enumerate(y_blocks):
                if block:
                    boxes.append(Pos(x * size, y * size, z * size) * Box(size, size, size))

    result = boxes[0]
    for box in boxes[1:]:
        result += box

    # Fillet the outer
    result = fillet((result.edges() | Axis.Y).group_by(Axis.Z)[0], radius=2)
    return result
