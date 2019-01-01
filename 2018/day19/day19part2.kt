/*

To compile and run:
    kotlinc day19part2.kt -include-runtime -d day19part2.jar && java -jar day19part2.jar

*/

import kotlin.math.*

fun main() {
    val b = 10551311
    var result = 0
    val sqrt_b = sqrt(b.toDouble())
    val max_p = ceil(sqrt_b).toInt()
    (1..floor(sqrt_b).toInt()).forEach {
        p ->
        if (b % p == 0) {
            result += p
            if (p < max_p) result += (b / p).toInt()
        }
    }
    println("Part 2: ${result}")
}
