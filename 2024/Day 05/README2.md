# 2024 Day 05

## Part One

See [README.md](README.md)

## Part Two

https://adventofcode.com/2024/day/5#part2

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.</p>
<p>For each of the <em>incorrectly-ordered updates</em>, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:</p>
<ul>
<li><code>75,97,47,61,53</code> becomes <code>97,75,<em>47</em>,61,53</code>.</li>
<li><code>61,13,29</code> becomes <code>61,<em>29</em>,13</code>.</li>
<li><code>97,13,75,29,47</code> becomes <code>97,75,<em>47</em>,29,13</code>.</li>
</ul>
<p>After taking <em>only the incorrectly-ordered updates</em> and ordering them correctly, their middle page numbers are <code>47</code>, <code>29</code>, and <code>47</code>. Adding these together produces <code><em>123</em></code>.</p>
<p>Find the updates which are not in the correct order. <em>What do you get if you add up the middle page numbers after correctly ordering just those updates?</em></p>
</article>

### My Solution

* My input was [input.txt](input.txt)
* I wrote [part2.py](part2.py)
* My [part2-output.txt](part2-output.txt) was correct
