# 2024 Day 03

## Part One

See [README.md](README.md)

## Part Two

https://adventofcode.com/2024/day/3#part2

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.</p>
<p>There are two new instructions you'll need to handle:</p>
<ul>
<li>The <code>do()</code> instruction <em>enables</em> future <code>mul</code> instructions.</li>
<li>The <code>don't()</code> instruction <em>disables</em> future <code>mul</code> instructions.</li>
</ul>
<p>Only the <em>most recent</em> <code>do()</code> or <code>don't()</code> instruction applies. At the beginning of the program, <code>mul</code> instructions are <em>enabled</em>.</p>
<p>For example:</p>
<pre><code>x<em>mul(2,4)</em>&amp;mul[3,7]!^<em>don't()</em>_mul(5,5)+mul(32,64](mul(11,8)un<em>do()</em>?<em>mul(8,5)</em>)</code></pre>
<p>This corrupted memory is similar to the example from before, but this time the <code>mul(5,5)</code> and <code>mul(11,8)</code> instructions are <em>disabled</em> because there is a <code>don't()</code> instruction before them. The other <code>mul</code> instructions function normally, including the one at the end that gets re-<em>enabled</em> by a <code>do()</code> instruction.</p>
<p>This time, the sum of the results is <code><em>48</em></code> (<code>2*4 + 8*5</code>).</p>
<p>Handle the new instructions; <em>what do you get if you add up all of the results of just the enabled multiplications?</em></p>
</article>

### My Solution

* My input was [input.txt](input.txt)
* I wrote [part2.py](part2.py)
* My [part2-output.txt](part2-output.txt) was correct
