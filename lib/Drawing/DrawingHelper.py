def PositionToLogical(pos, scale = 1.0, offset = (0, 0)):
    """
    Converts specified physical coordinates to logical coordinates using specified scale and offset.

    @param pos: Physical position to convert.
    @type pos: tuple

    @param scale: Scale, at which the conversion should be done.
    @type scale: float

    @param offset: Offset, which is subtracted from physical position.
    @type offset: tuple

    @rtype: tuple
    @return: Logical position.
    """
    pos = (pos[0] - offset[0]) / scale, (pos[1] - offset[0]) / scale
    return int(pos[0]), int(pos[1])

def PositionToPhysical(pos, scale = 1.0, offset = (0, 0)):
    """
    Converts specified logical coordinates to physical coordinates using specified scale and offset.

    @param pos: Logical position to convert.
    @type pos: tuple

    @param scale: Scale, at which the conversion should be done.
    @type scale: float

    @param offset: Offset, which is added to scaled logical position.
    @type offset: tuple

    @rtype: tuple
    @return: Physical position.
    """
    pos = (pos[0] * scale + offset[0]), (pos[1] * scale + offset[1])
    return int(pos[0]), int(pos[1])