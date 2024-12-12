# 2024 Day 12

## Part One

See [README.md](README.md)

## Part Two

https://adventofcode.com/2024/day/12#part2

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>Fortunately, the Elves are trying to order so much fence that they qualify for a <em>bulk discount</em>!</p>
<p>Under the bulk discount, instead of using the perimeter to calculate the price, you need to use the <em>number of sides</em> each region has. Each straight section of fence counts as a side, regardless of how long it is.</p>
<p>Consider this example again:</p>
<pre><code>AAAA
BBCD
BBCC
EEEC
</code></pre>
<p>The region containing type <code>A</code> plants has <code>4</code> sides, as does each of the regions containing plants of type <code>B</code>, <code>D</code>, and <code>E</code>. However, the more complex region containing the plants of type <code>C</code> has <code>8</code> sides!</p>
<p>Using the new method of calculating the per-region price by multiplying the region's area by its number of sides, regions <code>A</code> through <code>E</code> have prices <code>16</code>, <code>16</code>, <code>32</code>, <code>4</code>, and <code>12</code>, respectively, for a total price of <code><em>80</em></code>.</p>
<p>The second example above (full of type <code>X</code> and <code>O</code> plants) would have a total price of <code><em>436</em></code>.</p>
<p>Here's a map that includes an E-shaped region full of type <code>E</code> plants:</p>
<pre><code>EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
</code></pre>
<p>The E-shaped region has an area of <code>17</code> and <code>12</code> sides for a price of <code>204</code>. Including the two regions full of type <code>X</code> plants, this map has a total price of <code><em>236</em></code>.</p>
<p>This map has a total price of <code><em>368</em></code>:</p>
<pre><code>AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
</code></pre>
<p>It includes two regions full of type <code>B</code> plants (each with <code>4</code> sides) and a single region full of type <code>A</code> plants (with <code>4</code> sides on the outside and <code>8</code> more sides on the inside, a total of <code>12</code> sides). Be especially careful when counting the fence around regions like the one full of type <code>A</code> plants; in particular, each section of fence has an in-side and an out-side, so the fence does not connect across the middle of the region (where the two <code>B</code> regions touch diagonally). (The Elves would have used the Möbius Fencing Company instead, but their contract terms were too one-sided.)</p>
<p>The larger example from before now has the following updated prices:</p>
<ul>
<li>A region of <code>R</code> plants with price <code>12 * 10 = 120</code>.</li>
<li>A region of <code>I</code> plants with price <code>4 * 4 = 16</code>.</li>
<li>A region of <code>C</code> plants with price <code>14 * 22 = 308</code>.</li>
<li>A region of <code>F</code> plants with price <code>10 * 12 = 120</code>.</li>
<li>A region of <code>V</code> plants with price <code>13 * 10 = 130</code>.</li>
<li>A region of <code>J</code> plants with price <code>11 * 12 = 132</code>.</li>
<li>A region of <code>C</code> plants with price <code>1 * 4 = 4</code>.</li>
<li>A region of <code>E</code> plants with price <code>13 * 8 = 104</code>.</li>
<li>A region of <code>I</code> plants with price <code>14 * 16 = 224</code>.</li>
<li>A region of <code>M</code> plants with price <code>5 * 6 = 30</code>.</li>
<li>A region of <code>S</code> plants with price <code>3 * 6 = 18</code>.</li>
</ul>
<p>Adding these together produces its new total price of <code><em>1206</em></code>.</p>
<p><em>What is the new total price of fencing all regions on your map?</em></p>
</article>

### My Solution

* My input was [input.txt](input.txt)
* I wrote [part2.py](part2.py)
* My [part2-output.txt](part2-output.txt) was correct
