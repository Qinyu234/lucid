<div align="center">
  <h1>Code Generator</h1>
  <p>一个写着玩的本地代码生成实验<br/>
     A local code generation experiment I built for fun</p>
</div>

<hr/>

<h2>Part 1：定义 | Definition</h2>

<p>
这是一个水简历项目。<br/>
This is basically something I can put into my resume (*^_^*).
</p>

<p>
还在不断改，没有稳定版本。整体状态大概是：<br/>
Still under heavy changes, no stable version at all. Current state:
</p>

<blockquote>
能跑，但不太稳定，也不保证什么时候会推倒重来。<br/>
It runs, but unstable, and may get rewritten anytime.
</blockquote>

<hr/>

<h2>Part 2：它是干嘛的 | What it does</h2>

<p>
简单来说就是：<br/>
In short:
</p>

<blockquote>
根据一些简单要求自动生成代码。<br/>
Generate code from simple requirements.
</blockquote>

<p>
本质上就是在复刻现在各种 AI coding tool 在做的事情，只不过是我自己在本地搭了一套。<br/>
It's basically redoing what existing AI coding tools already do, but built locally by myself.
</p>

<h3>Part 2.1：现在能用吗 | Can it actually be used?</h3>

<p>
不太行。<br/>
Not really.
</p>

<p>最近的问题 | Current problems:</p>

<ul>
  <li>容易出现语义上的文件循环<br/>Semantic file loops happen</li>
  <li>结构和人类思路相去甚远，看着很扭<br/>Structure looks very unnatural</li>
  <li>我的破电脑太慢，反馈周期基本按天算<br/>My laptop is too slow that feedback loop takes 1+ day</li>
</ul>

<p>
如果只是想写代码：<br/>
If you actually just want to write code:
</p>

<p>
更推荐直接用现成工具。<br/>
use existing tools instead.
</p>

<hr/>

<h2>Part 3：那为什么还在做 | Why still doing this</h2>

<p>
理由其实很简单：<br/>
Reasons are simple:
</p>

<ul>
  <li>最近有点闲<br/>Free time</li>
  <li>可以水简历<br/>Good for resume</li>
  <li>项目式学习更有意思<br/>Project-based learning is more fun</li>
</ul>

<p>
所以更像是一个实验台，没有产品的想法。<br/>
So it's more like an experiment setup, not a product.
</p>

<hr/>

<h2>Part 4：现在在做什么 | Current approach</h2>

<p>
核心思路是：<br/>
Core idea:
</p>

<blockquote>
用一套我自己定的规则去生成和检查代码。<br/>
Use a set of self-defined rules to generate and validate code.
</blockquote>

<h3>4.1 结构规则 | Structure rules</h3>

<ul>
  <li>函数 = 文件<br/>Function = file</li>
  <li>文件名 = 函数名<br/>Filename = function name</li>
  <li>每个文件夹必须有 init<br/>Each folder must have an init</li>
  <li>init = 模块入口<br/>Init acts as module entry</li>
  <li>import 被限制<br/>Import is restricted</li>
</ul>

<p>
本质就是强行控制结构，同时缩小 LLM task。<br/>
Forcing structure + reducing LLM task size.
</p>

<h3>4.2 默认语言 | Default language</h3>

<pre><code>Python</code></pre>

<p>
没有认真支持多语言，要改的话 init 要改，有些还改不了。<br/>
No multi-language support. Init design is Python-specific.
</p>

<h3>4.3 拆分问题 | Task decomposition</h3>

<p>
核心问题：<br/>
Main problem:
</p>

<blockquote>
怎么把任务拆合理。<br/>
How to decompose tasks properly.
</blockquote>

<p>当前做法 | Current method:</p>
<ul>
  <li>用模板拆分（sequence / parallel / router）<br/>
      Template-based (sequence / parallel / router)</li>
</ul>

<p>问题 | Issues:</p>
<ul>
  <li>不稳定<br/>Unstable</li>
  <li>函数名极长且不可读<br/>Function names become unreadable</li>
</ul>

<p>
现在在考虑：<br/>
Considering:
</p>

<ul>
  <li>更大模型<br/>Use larger models</li>
  <li>更复杂模板<br/>Improve template structure</li>
</ul>

<hr/>

<h2>Part 4.5：失败思路 | Failed attempts</h2>

<h3>memory / 复用已有代码</h3>

<p>
一个想法是：<br/>
Idea:
</p>

<ul>
  <li>存储已经生成的 leaf 函数<br/>Store generated leaf functions</li>
  <li>作为 memory 供后续复用<br/>Use them as reusable memory</li>
</ul>

<p>
听起来不错，但问题很多：<br/>
but:
</p>

<blockquote>
跑到第四个小时程序直接崩。<br/>
Crashed after 4 hours runtime.
</blockquote>

<p>
大概率是 context 或状态过长。<br/>
Likely due to context explosion.
</p>

<p>
目前结论：<br/>
Conclusion:
</p>

<blockquote>
理论可行，但现实跑不动。<br/>
Theoretically valid, practically unusable.
</blockquote>

<hr/>

<h2>Part 5：未来规划 | Future</h2>

<p>
结论：<br/>
Conclusion:
</p>

<blockquote>
短期不会变好用。<br/>
Won't be good anytime soon.
</blockquote>

<p>可能方向 | Possible ideas:</p>
<ul>
  <li>抄现成方案<br/>Use existing solutions</li>
  <li>合并重复代码<br/>Deduplicate code</li>
  <li>支持多语言<br/>Support multiple languages</li>
  <li>优化效率<br/>Improve efficiency</li>
</ul>

<h3>怎么优化 | How?</h3>

<p>
还没想清楚。<br/>
Not clear yet.
</p>

<p>
一个想法：<br/>
One idea:
</p>

<ul>
  <li>拆成节点+路径<br/>Split into nodes and paths</li>
  <li>给路径拟合效率函数<br/>Fit efficiency functions</li>
  <li>用 maxflow + gene优化方法分配<br/>Optimize with maxflow+gene methods</li>
</ul>

<p>
但目前只是想法，而且电脑跑不动。<br/>
Theoretical, also hardware struggles.
</p>

<hr/>

<h2>📌 总结 | Summary</h2>

<ul>
  <li>能跑<br/>Runs</li>
  <li>不稳定<br/>Unstable</li>
  <li>有更好的替代方案<br/>Better tools exist</li>
</ul>

<p>
这个项目的意义就是：<br/>
This project exists to:
</p>

<blockquote>
看看不用现成工具，我自己这套思路能走到哪一步。<br/>
See how far I can push this idea.
</blockquote>

<hr/>

<div align="center">
  <p>Qinyu Zhang</p>
</div>
