# 2024 Day 01

## Part One

See [README.md](README.md)

## Part Two

https://adventofcode.com/2024/day/1#part2

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>Your analysis only confirmed what everyone feared: the two lists of location IDs are indeed very different.</p>
<p>Or are they?</p>
<p>The Historians can't agree on which group made the mistakes <em>or</em> how to read most of the Chief's handwriting, but in the commotion you notice an interesting detail: <span title="We were THIS close to summoning the Alot of Location IDs!">a lot</span> of location IDs appear in both lists! Maybe the other numbers aren't location IDs at all but rather misinterpreted handwriting.</p>
<p>This time, you'll need to figure out exactly how often each number from the left list appears in the right list. Calculate a total <em>similarity score</em> by adding up each number in the left list after multiplying it by the number of times that number appears in the right list.</p>
<p>Here are the same example lists again:</p>
<pre><code>3   4
4   3
2   5
1   3
3   9
3   3
</code></pre>
<p>For these example lists, here is the process of finding the similarity score:</p>
<ul>
<li>The first number in the left list is <code>3</code>. It appears in the right list three times, so the similarity score increases by <code>3 * 3 = <em>9</em></code>.</li>
<li>The second number in the left list is <code>4</code>. It appears in the right list once, so the similarity score increases by <code>4 * 1 = <em>4</em></code>.</li>
<li>The third number in the left list is <code>2</code>. It does not appear in the right list, so the similarity score does not increase (<code>2 * 0 = 0</code>).</li>
<li>The fourth number, <code>1</code>, also does not appear in the right list.</li>
<li>The fifth number, <code>3</code>, appears in the right list three times; the similarity score increases by <code><em>9</em></code>.</li>
<li>The last number, <code>3</code>, appears in the right list three times; the similarity score again increases by <code><em>9</em></code>.</li>
</ul>
<p>So, for these example lists, the similarity score at the end of this process is <code><em>31</em></code> (<code>9 + 4 + 0 + 0 + 9 + 9</code>).</p>
<p>Once again consider your left and right lists. <em>What is their similarity score?</em></p>
</article>

### My Solution

* My input was [input.txt](input.txt)
* I wrote [part2.py](part2.py)
* My [part2-output.txt](part2-output.txt) was correct
