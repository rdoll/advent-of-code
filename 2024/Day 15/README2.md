# 2024 Day 15

## Part One

See [README.md](README.md)

## Part Two

https://adventofcode.com/2024/day/15#part2

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>The lanternfish use your information to find a safe moment to swim in and turn off the malfunctioning robot! Just as they start preparing a festival in your honor, reports start coming in that a <em>second</em> warehouse's robot is <em>also</em> malfunctioning.</p>
<p>This warehouse's layout is surprisingly similar to the one you just helped. There is one key difference: everything except the robot is <em>twice as wide</em>! The robot's list of movements doesn't change.</p>
<p>To get the wider warehouse's map, start with your original map and, for each tile, make the following changes:</p>
<ul>
<li>If the tile is <code>#</code>, the new map contains <code>##</code> instead.</li>
<li>If the tile is <code>O</code>, the new map contains <code>[]</code> instead.</li>
<li>If the tile is <code>.</code>, the new map contains <code>..</code> instead.</li>
<li>If the tile is <code>@</code>, the new map contains <code>@.</code> instead.</li>
</ul>
<p>This will produce a new warehouse map which is twice as wide and with wide boxes that are represented by <code>[]</code>. (The robot does not change size.)</p>
<p>The larger example from before would now look like this:</p>
<pre><code>####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################
</code></pre>
<p>Because boxes are now twice as wide but the robot is still the same size and speed, boxes can be aligned such that they directly push two other boxes at once. For example, consider this situation:</p>
<pre><code>#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

&lt;vv&lt;&lt;^^&lt;&lt;^^
</code></pre>
<p>After appropriately resizing this map, the robot would push around these boxes as follows:</p>
<pre><code>Initial state:
##############
##......##..##
##..........##
##....[][]<em>@</em>.##
##....[]....##
##..........##
##############

Move &lt;:
##############
##......##..##
##..........##
##...[][]<em>@</em>..##
##....[]....##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[].<em>@</em>..##
##..........##
##############

Move v:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.......<em>@</em>..##
##############

Move &lt;:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##......<em>@</em>...##
##############

Move &lt;:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.....<em>@</em>....##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....<em>@</em>....##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....<em>@</em>....##
##..........##
##############

Move &lt;:
##############
##......##..##
##...[][]...##
##....[]....##
##....<em>@</em>.....##
##..........##
##############

Move &lt;:
##############
##......##..##
##...[][]...##
##....[]....##
##...<em>@</em>......##
##..........##
##############

Move ^:
##############
##......##..##
##...[][]...##
##...<em>@</em>[]....##
##..........##
##..........##
##############

Move ^:
##############
##...[].##..##
##...<em>@</em>.[]...##
##....[]....##
##..........##
##..........##
##############
</code></pre>
<p>This warehouse also uses GPS to locate the boxes. For these larger boxes, distances are measured from the edge of the map to the closest edge of the box in question. So, the box shown below has a distance of <code>1</code> from the top edge of the map and <code>5</code> from the left edge of the map, resulting in a GPS coordinate of <code>100 * 1 + 5 = 105</code>.</p>
<pre><code>##########
##...[]...
##........
</code></pre>
<p>In the scaled-up version of the larger example from above, after the robot has finished all of its moves, the warehouse would look like this:</p>
<pre><code>####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..<em>@</em>......[].[][]##
##......[][]..[]..##
####################
</code></pre>
<p>The sum of these boxes' GPS coordinates is <code><em>9021</em></code>.</p>
<p>Predict the motion of the robot and boxes in this new, scaled-up warehouse. <em>What is the sum of all boxes' final GPS coordinates?</em></p>
</article>

### My Solution

* My input was [input.txt](input.txt)
* I wrote [part2.py](part2.py)
* My [part2-output.txt](part2-output.txt) was correct
