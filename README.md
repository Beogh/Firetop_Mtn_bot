Firetop Mountain Bot is a python bot created to play through The Warlock of Firetop Mountain on twitter. 
It updates every 6 hours and typically reads a poll then spits out the next events.

#**What is The Warlock of Firetop Mountain?**
It's a book, originally published in 1982 by Steve Jackson and Ian Livingstone. The Warlock of Firetop Mountain launched the Fighting Fantasy series, a collection of books that tried to build off "choose your own adventure" ideas and turn them into a full self-played game. Players have a character sheet that tracks stats and items, and make choices that determine their path through the passages, with one particular path giving the best ending.

#**Who made this?**
This bot was created by user @digitalmaxine on twitter.

#**Why make this?**
Mostly to go through the process of making it, but it's also fun to go through the game with a committee.

#**What changes did you make?**
There is exactly one designed change that restricts from the original book, a passage with five choices has one that only leads to a fight with no reward, so in the interest of keeping it a poll (which can only have four options) I removed this option. The only other notable and intentional change is the complete removal of any carrying limits imposed. If a passage says you may take something if you leave something else behind, you don't lose anything. The process for bot1.0 was a little haphazard so there's inevitably a few changes that were missed, but we'll smooth that out with time. I have also added the difficulties and classes to the game.

#**Why add the Difficulties and Classes?**
Difficulties: Initial stats play a big part in how the game plays out. Notably, at low Skill the texture of a lot of fights changes. It is proven possible to get the best ending with minimal stats, but it requires a little luck and near-perfect passage choices. With this in mind, a curated list of difficulties was preferable to rolling random stats, as it allows players to test against a known difficulty.
Classes: These arose from a format problem. Originally I didn't know what to do with the fact that players can test their luck in combat to deal extra damage or reduce damage taken. Twitter polls would mean either creating polls for each round, or automating this decision and the decision whether to flee. Once I had decided that fights should be automated, it was natural to have different 'personalities' that could flee at different danger levels and test luck in different situations, eventually leading to the current classes. 

#**What does the bot do in case of a poll tie?**
When there is a tie between results, the bot will choose one of the winners at random.


#**Rules of the Game:**

The character, controlled by all players via twitter poll, starts with several stats determined by their difficulty/class. These stats are the following:
Skill: primarily used when fighting enemies, skill is not often modified either positive or negative. In combat, players test 2d6 + skill against a monster rolling 2d6 + skill. If they tie, move to the next round. Elsewise, whoever wins deals damage (almost always 2) and then move to the next round. Players can test their luck to increase the damage they deal, or reduce the damage suffered.
Stamina: similar to HP in other games, if stamina is reduced to zero, the character has died and will have to start over. Provisions restore this and enemies, traps and bad luck reduce it.
Luck: A vital stat for any adventurer, Luck is used when the player is asked to test their luck. To do so, roll 2d6 and if the result is lower than your Luck, you are considered Lucky. Elsewise, you're Unlucky. Proceed accordingly. Each time Luck is tested, it is then reduced by one.
Gold: The material wealth of the dungeon. Gold doesn't take up any space in the haversack and it's primarily used to keep score though there are denizens that accept coin for goods or services.
Provisions: Normally restore Stamina by 4, and can only be eaten at certain safe locations. Running out of provisions doesn't mean you'll starve to death, but it does make survival that much less likely.

In addition, the player is given a choice of which potion you would like to start with. Each potion has two measures, and unlike later Fighting Fantasy games they may be quaffed even during combat. They are listed here:
Skill: Potion of Skill restores your Skill to full.
Strength: Potion of Strength restores your Stamina to full
Fortune: Potion of Fortune restores your Luck to full and adds 1 to your initial Luck.

The character will move through the dungeon until there is a notable event (usually a decision poll, but fights and item acquirement also count) then an update will be posted to twitter. If a poll was created, then it will run for six hours and the results will be used to move to the next notable event. If the character runs out of stamina or any of the other ways of ending a game, they will run into a game over, then the bot will clean up and start anew.

More to come as questions arise. If you have any questions, DM @digitalmaxine on twitter.
