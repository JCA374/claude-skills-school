# How Claude picks and loads a skill

## At the start: only a list

When a session starts, I do not read your skills. I only see a list. One line per skill, the name and the description. That is all.

## Your request meets the descriptions

When you ask for something, I compare your words with every description. Here you ask for a homepage for a training run. One description fits: the project site skill.

## Three levels of loading

Now the skill loads in layers. First the body of the skill file. Then, only when a step needs it, a reference file or a script. This is called progressive disclosure.

## Or call it yourself

You can also skip the matching. Type a slash and the skill's name, and it loads straight away. That is handy for commands you run on purpose, like a deploy or a review.

## Why the description matters most

So the description is the trigger. A weak one says what the skill is. A strong one also lists the words you actually say when you need it. Yours for the project site is a strong one.

