# 2024 Day 10

## Part One

See [README.md](README.md)

## Part Two

https://adventofcode.com/2024/day/10#part2

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper.</p>
<p>The paper describes a second way to measure a trailhead called its <em>rating</em>. A trailhead's rating is the <em>number of distinct hiking trails</em> which begin at that trailhead. For example:</p>
<pre><code>.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
</code></pre>
<p>The above map has a single trailhead; its rating is <code>3</code> because there are exactly three distinct hiking trails which begin at that position:</p>
<pre><code>.....0.   .....0.   .....0.
..4321.   .....1.   .....1.
..5....   .....2.   .....2.
..6....   ..6543.   .....3.
..7....   ..7....   .....4.
..8....   ..8....   ..8765.
..9....   ..9....   ..9....
</code></pre>
<p>Here is a map containing a single trailhead with rating <code>13</code>:</p>
<pre><code>..90..9
...1.98
...2..7
6543456
765.987
876....
987....
</code></pre>
<p>This map contains a single trailhead with rating <code>227</code> (because there are <code>121</code> distinct hiking trails that lead to the <code>9</code> on the right edge and <code>106</code> that lead to the <code>9</code> on the bottom edge):</p>
<pre><code>012345
123456
234567
345678
4.6789
56789.
</code></pre>
<p>Here's the larger example from before:</p>
<pre><code>89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
</code></pre>
<p>Considering its trailheads in reading order, they have ratings of <code>20</code>, <code>24</code>, <code>10</code>, <code>4</code>, <code>1</code>, <code>4</code>, <code>5</code>, <code>8</code>, and <code>5</code>. The sum of all trailhead ratings in this larger example topographic map is <code><em>81</em></code>.</p>
<p>You're not sure how, but the reindeer seems to have crafted some tiny flags out of toothpicks and bits of paper and is using them to mark trailheads on your topographic map. <em>What is the sum of the ratings of all trailheads?</em></p>
</article>

### My Solution

* My input was [input.txt](input.txt)
* I wrote [part2.py](part2.py)
* My [part2-output.txt](part2-output.txt) was correct
