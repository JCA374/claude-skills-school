# Episode 02: How your skills learn

Welcome back. Last time we covered what a skill is. Today is about how a skill gets better. And you have a real example, so I will use it.

A skill does not learn by itself the way a model learns from data. It learns because someone writes down a lesson. The skill file is a living document. Every time something goes wrong, the fix can become a rule. The next time, I follow that rule without being told.

Your audiobook studio does this better than anything else on your machine. It has a training folder with ten cases so far. Each case is a moment where the audio sounded wrong. Case one was a short question, "Can I?", that ended flat, so it sounded cut off. I wrote the line twice, once with the old rules and once with a fix, and rendered both. You listened and picked the better one. Only then did the fix become a rule in the narration prep skill. Today that rule runs automatically on every book and every podcast, including this one.

Notice the order. A problem is reported. It becomes a case, with a before and an after. You choose. Then it becomes a rule. And a test is added, so a later rule can never quietly undo an earlier fix. There are tests like that for every scanner rule, and they must pass before anything is published.

The second source of lessons is a machine listener. The listen check skill has Whisper transcribe the finished audio and compare it with the script. In one book, a character asks for something to go on the record. Kokoro kept slurring the words want and it into a single word, wanted. Whisper caught it four times, and the check only keeps a flag when a second, slower model hears the same thing. That became case eight.

Your project site skill learned in a different way. It has a section called rules learned the hard way. One rule says the publisher must never run a rebase with auto stash, because once it silently threw away an hour of work. That single sentence now protects every project you start.

So that is the first habit: when something breaks, write the lesson into the skill, not just into the chat. A chat is forgotten. A skill is not.

The second habit is to measure. The skill creator, which Anthropic ships, runs the same task twice, once with the skill and once without it. Then it compares the results side by side. If the skill does not beat the baseline, it is not pulling its weight yet. It can also test the description alone. It writes realistic requests, some that should trigger the skill and some that should not, and checks how often I pick it.

The third habit is about how to write the lesson. Explain why. If a rule says never, in capital letters, I will obey it, but I cannot judge the cases the rule did not foresee. If the rule says why, I can. Your listen check skill does this well. It explains why there is no pitch check. You measured twenty six lines. Questions fell in pitch just like statements. So a rise detector would flag every question. Because the reason is written down, nobody adds that check again by mistake.

Last, keep it lean. A skill file should stay under about five hundred lines. Move long details into reference files, and say exactly when to open them. And if you notice me writing the same helper script for the third time, that script belongs in the skill's scripts folder.

Next episode, we will build something new together on paper: a skill that reviews academic papers and reports.
