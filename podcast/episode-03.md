# Episode 03: A skill that reviews papers

In this episode, we design a skill you do not have yet. It reviews academic papers and long reports. It is a good first project, because you can test it on papers you already know well.

Start with the description, because that is the trigger. It should say what the skill does and when to use it. Something like this. Review an academic paper, a thesis chapter or a technical report, the way a careful referee would. Use it when someone asks to review, critique, referee, check or give feedback on a paper or report, or attaches a PDF and asks if it holds up.

Then the instructions. A good review follows a fixed path, so the skill should too. First, read the whole thing once and write a three sentence summary of the claim. If I cannot summarize the claim, that is already the first finding. Second, check the claim against the evidence. Does every main result come from a table, a figure or a test? Are the sample sizes stated? Is there a baseline? Third, look at the method. Could the result be luck, a leak between training and test data, or a choice made after seeing the results? Fourth, check the references. Are the important sources cited, and does the paper say what those sources actually say? Fifth, the writing. Is the abstract honest about the result?

The output should be a fixed form. A summary, the major issues, the minor issues, questions for the authors, and a verdict with a confidence level. Every issue must point to a page or a section. A review that says "the method is weak" without saying where is useless.

Now the parts that make it a real skill instead of a long prompt. Put the checklists in a reference folder. One for machine learning papers, one for statistics, one for business reports. The skill file tells me to open only the one that fits. A script can pull the text and the tables out of the PDF, and count the figures and references, so I start from facts.

Then make it learn, the same way your audiobook studio does. Keep a folder of test papers. Some are good, some have known flaws, and a few could be retracted papers where the flaw is public. Each time I miss a flaw, that becomes a case. Write down what I missed and why, then add a rule. Run every test paper again after each change. And use the skill creator to compare reviews with the skill and without it, so you know the skill is actually helping.

One warning matters here. A reviewer skill must never invent a citation or a number. So add a rule that every quote and every number in the review must be found in the paper text, and let a script check it. That is the same idea as your listen check. A second reader confirms the first.

It also fits your other skills. The PDF skill reads the file. The failure analysis report gives you a way to show where reviews go wrong. And voice text could even read the review aloud, so you can listen to it on a walk.

On the website, the projects tab has more ideas like this, from small to large. Pick one, build the first version in an evening, and then let the cases make it better. That is how every good skill on your machine was made.
