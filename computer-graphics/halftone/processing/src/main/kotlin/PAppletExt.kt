import processing.core.PApplet

fun PApplet.stackMatrix(x: Number = 0f, y: Number = 0f, z: Number = 0f, transformation: () -> Unit) {
    stackMatrix(x.toFloat(), y.toFloat(), z.toFloat(), transformation)
}

fun PApplet.stackMatrix(x: Float = 0f, y: Float = 0f, z: Float = 0f, transformation: () -> Unit) {
    pushMatrix() // saves the current coordinate system to the stack
    translate(x, y, z)

    transformation()

    popMatrix() // restores the prior coordinate system
}