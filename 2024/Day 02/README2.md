# 2024 Day 02

## Part One

See [README.md](README.md)

## Part Two

https://adventofcode.com/2024/day/2#part2

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the <span title="I need to get one of these!">Problem Dampener</span>.</p>
<p>The Problem Dampener is a reactor-mounted module that lets the reactor safety systems <em>tolerate a single bad level</em> in what would otherwise be a safe report. It's like the bad level never happened!</p>
<p>Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.</p>
<p>More of the above example's reports are now safe:</p>
<ul>
<li><code>7 6 4 2 1</code>: <em>Safe</em> without removing any level.</li>
<li><code>1 2 7 8 9</code>: <em>Unsafe</em> regardless of which level is removed.</li>
<li><code>9 7 6 2 1</code>: <em>Unsafe</em> regardless of which level is removed.</li>
<li><code>1 <em>3</em> 2 4 5</code>: <em>Safe</em> by removing the second level, <code>3</code>.</li>
<li><code>8 6 <em>4</em> 4 1</code>: <em>Safe</em> by removing the third level, <code>4</code>.</li>
<li><code>1 3 6 7 9</code>: <em>Safe</em> without removing any level.</li>
</ul>
<p>Thanks to the Problem Dampener, <code><em>4</em></code> reports are actually <em>safe</em>!</p>
<p>Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. <em>How many reports are now safe?</em></p>
</article>

### My Solution

* My input was [input.txt](input.txt)
* I wrote [part2.py](part2.py)
* My [part2-output.txt](part2-output.txt) was correct
* Note that this was tricky because all permutations were not in the sample input -- a good lesson!