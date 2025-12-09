# 2025 Day 08

## Part One

See [README.md](README.md)

## Part Two

https://adventofcode.com/2025/day/8#part2

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>The Elves were right; they <em>definitely</em> don't have enough extension cables. You'll need to keep connecting junction boxes together until they're all in <em>one large circuit</em>.</p>
<p>Continuing the above example, the first connection which causes all of the junction boxes to form a single circuit is between the junction boxes at <code>216,146,977</code> and <code>117,168,530</code>. The Elves need to know how far those junction boxes are from the wall so they can pick the right extension cable; multiplying the X coordinates of those two junction boxes (<code>216</code> and <code>117</code>) produces <code><em>25272</em></code>.</p>
<p>Continue connecting the closest unconnected pairs of junction boxes together until they're <span title="I strongly recommend making an interactive visualizer for this one; it reminds me a lot of maps from futuristic space games.">all in the same circuit</span>. <em>What do you get if you multiply together the X coordinates of the last two junction boxes you need to connect?</em></p>
</article>

### My Solution

* My input was [input.txt](input.txt)
* I wrote [part2.py](part2-all-df.py)
* My [part2-output.txt](part2-output.txt) was correct
