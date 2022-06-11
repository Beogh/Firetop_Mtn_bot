Firetop Mountain Bot is a python bot created by @digitlamaxine to play through The Warlock of Firetop Mountain on twitter. 
It updates thrice daily and typically reads a poll then spits out the next events.

## **What is The Warlock of Firetop Mountain?**
It's a book, originally published in 1982 by Steve Jackson and Ian Livingstone. The Warlock of Firetop Mountain launched the Fighting Fantasy series, a collection of books that tried to build off "choose your own adventure" ideas and turn them into a full self-played game. Players have a character sheet that tracks stats and items, and make choices that determine their path through the passages, with one particular path giving the best ending.

# **FAQ**
**Who made this?**

This bot was created by user @digitalmaxine on twitter.


**Why make this?**

Mostly to go through the process of making it, but it's also fun to go through the game with a committee.

**What changes did you make?**

There is exactly one designed change that restricts from the original book, a passage with five choices has one that only leads to a fight with no reward, so in the interest of keeping it a poll (which can only have four options) I removed this option. The only other notable and intentional change is the complete removal of any carrying limits imposed. If a passage says you may take something if you leave something else behind, you don't lose anything. The process for bot1.0 was a little haphazard so there's inevitably a few changes that were missed, but we'll smooth that out with time. I have also added the difficulties and classes to the game.


**Why add the Difficulties and Classes?**

Difficulties: Initial stats play a big part in how the game plays out. Notably, at low Skill the texture of a lot of fights changes. It is proven possible to get the best ending with minimal stats, but it requires a little luck and near-perfect passage choices. With this in mind, a curated list of difficulties was preferable to rolling random stats, as it allows players to test against a known difficulty.

Classes: These arose from a format problem. Originally I didn't know what to do with the fact that players can test their luck in combat to deal extra damage or reduce damage taken. Twitter polls would mean either creating polls for each round, or automating this decision and the decision whether to flee. Once I had decided that fights should be automated, it was natural to have different 'personalities' that could flee at different danger levels and test luck in different situations, eventually leading to the current classes. 


**What does the bot do in case of a poll tie?**

When there is a tie between results, the bot will choose one of the winners at random.



# **Rules of the Game:**

The character, controlled by all players via twitter poll, starts with several stats determined by their difficulty/class. These stats are the following:

**Skill**: primarily used when fighting enemies, skill is not often modified either positive or negative. In combat, players test 2d6 + skill against a monster rolling 2d6 + skill. If they tie, move to the next round. Elsewise, whoever wins deals damage (almost always 2) and then move to the next round. Players can test their luck to increase the damage they deal, or reduce the damage suffered.

**Stamina**: similar to HP in other games, if stamina is reduced to zero, the character has died and will have to start over. Provisions restore this and enemies, traps and bad luck reduce it.

**Luck**: A vital stat for any adventurer, Luck is used when the player is asked to test their luck. To do so, roll 2d6 and if the result is lower than your Luck, you are considered Lucky. Elsewise, you're Unlucky. Proceed accordingly. Each time Luck is tested, it is then reduced by one.

**Gold**: The material wealth of the dungeon. Gold doesn't take up any space in the haversack and it's primarily used to keep score though there are denizens that accept coin for goods or services.

**Provisions**: Normally restore Stamina by 4, and can only be eaten at certain safe locations. Running out of provisions doesn't mean you'll starve to death, but it does make survival that much less likely.

# **Difficulty and Classes**

There are four each of difficulties and classes. They are listed below with their mechanical adjustments.

## **Difficulties**
The chosen difficulty only modifies a characters initial stats. It does not change enemy or character behavior.

### **Easy**
Skill: 11

Stamina: 18

Luck: 11

Gold: 0

Provisions: 10


### **Medium**
Skill: 10

Stamina: 16

Luck: 10

Gold: 0

Provisions: 9


### **Hard**
Skill: 9

Stamina: 15

Luck: 8

Gold: 0

Provisions: 7


### **Very Hard**
Skill: 8

Stamina: 14

Luck: 8

Gold: 0

Provisions: 6



## **Classes**
The chosen class will potentially modify initial stats, and determines behavior. All classes will not flee if their stamina is 2 or below, as the fleeing penalty will kill them.

### **Soldier**
Stat changes: None

Flees: If the foe has 4, or more, skill higher than the character and can be fled from.

Tests luck in combat: 

-When attacking: Only if luck is above 8 (or 5 if current stamina is below 5) and the enemy has an odd (as opposed to "even") stamina, and your own skill is less than 2 above the enemies skill. So foes with skill above the soldier will trigger this.

-When defending: Only if current stamina is even (as opposed to "odd") and luck is 10 or higher and enemy skill is at least 2 above character skill.

### **Cook**
Stat changes: +4 starting provisions, +3 starting gold

Flees: If the enemy has higher skill and can be fled from.

Tests luck in combat: 

-When attacking: if the foe has odd stamina, and current luck is at least 10, and current skill is less than 4 above the foes skill.

-When defending: Only if luck is above 10 and taking the reduced damage would put the character at an odd stamina value

### **Berserker**
Stat changes: +1 skill

Flees: Only if the enemy has 6, or more, skill above the character, and they can be fled from.

Tests luck in combat: 

-When attacking: Only when above 8 luck, and doing so would reduce enemy stamina to a multiple of 2, and enemy is higher skill than the character.

-When defending: Never

Special: If the berserker would die, instead test luck + 4, and if lucky then they survive at 1 stamina. This test reduces luck.

### **Noble**
Stat changes: +6 gold

Flees: If the foe has 4, or more, skill higher than the character and can be fled from.

Tests luck in combat: 

-When attacking: If the foe has a higher skill, and the character has at least 11 luck, and the attack would reduce enemy stamina to an even number.

-When defending: If luck is at least 7, and enemy has greater skill than the character.


______________________________
In addition, the player is given a choice of which potion you would like to start with. Each potion has two measures, and unlike later Fighting Fantasy games they may be quaffed even during combat. They are listed here:

Skill: Potion of Skill restores your Skill to full.

Strength: Potion of Strength restores your Stamina to full

Fortune: Potion of Fortune restores your Luck to full and adds 1 to your initial Luck.


The character will move through the dungeon until there is a notable event (usually a decision poll, but fights and item acquirement also count) then an update will be posted to twitter. If a poll was created, then it will run for six hours and the results will be used to move to the next notable event. If the character runs out of stamina or any of the other ways of ending a game, they will run into a game over, then the bot will clean up and start anew.


More to come as questions arise. If you have any questions, DM @digitalmaxine on twitter.

Manual Repository of Final Run Tweets:
Run 1: https://twitter.com/twtt_rpg/status/1535009850031235084?s=20&t=Ur6oi5t6Hj_8V6dppTTwqw
