**ACADEMIC HONESTY**

As usual, the standard honor code and academic honesty policy applies. We will be using automated **plagiarism detection** software to ensure that only original work is given credit. Submissions isomorphic to (1) those that exist anywhere online, (2) those submitted by your classmates, or (3) those submitted by students in prior semesters, will be detected and considered plagiarism.

**INSTRUCTIONS**

In this assignment you will create an agent to solve the 8**-puzzle** game. You may visit [**mypuzzle.org/sliding**](http://mypuzzle.org/sliding) for a refresher of the rules of the game. You will implement and compare several search algorithms and collect some statistics related to their performances. Please read all sections of the instructions carefully:

- **I.** Introduction
- **II.** Algorithm Review
- **III.** What You Need To Submit
- **IV.** What Your Program Outputs
- **V.** Important Information
- **VI.** Before You Finish

**NOTE**: This project incorporates material learned from both **Week 2** (uninformed search) and **Week 3** (informed search). Since this project involves a fair amount of programming and design, we are releasing it now to let you get started earlier. In particular, do not worry if certain concepts (e.g. heuristics, A-Star, etc.) are not familiar at this point; you will understand everything you need to know by Week 3.

Also note that there is **skeleton code available for use** (see the third tab of this assignment). This is **completely optional to use**, and you may alter it as much as you'd like. You may also complete the assignment without referring to the skeleton code at all.

**I. Introduction**

An instance of the N-puzzle game consists of a **board** holding N = m^2 − 1 (m = 3, 4, 5, ...) distinct movable tiles, plus an empty space. The tiles are numbers from the set {1, …, m^2 − 1}. For any such board, the empty space may be legally swapped with any tile horizontally or vertically adjacent to it. In this assignment, we will represent the blank space with the number 0 and focus on the m = 3 case (8-puzzle).

Given an initial **state** of the board, the combinatorial search problem is to find a sequence of moves that transitions this state to the goal state; that is, the configuration with all tiles arranged in ascending order ⟨0, 1, …, m^2 − 1⟩. The search space is the set of all possible states reachable from the initial state.

The blank space may be swapped with a component in one of the four directions {‘Up’, ‘Down’, ‘Left’, ‘Right’}, one move at a time. The cost of moving from one configuration of the board to another is the same and equal to one. Thus, the total cost of path is equal to the number of moves made from the initial state to the goal state.

**II. Algorithm Review**

Recall from the lectures that searches begin by visiting the root node of the search tree, given by the initial state. Among other book-keeping details, three major things happen in sequence in order to visit a node:

- First, we **remove** a node from the frontier set.
- Second, we **check** the state against the goal state to determine if a solution has been found.
- Finally, if the result of the check is negative, we then **expand** the node. To expand a given node, we generate successor nodes adjacent to the current node, and add them to the frontier set. Note that if these successor nodes are already in the frontier, or have already been visited, then they should not be added to the frontier again.

This describes the life-cycle of a visit, and is the basic order of operations for search agents in this assignment—(1) remove, (2) check, and (3) expand. In this assignment, we will implement algorithms as described here. Please refer to lecture notes for further details, and review the lecture pseudocode before you begin the assignment.

**IMPORTANT**: Note that you may encounter implementations elsewhere that attempt to short-circuit this order by performing the goal-check on successor nodes immediately upon expansion of a parent node. For example, Russell & Norvig's implementation of breadth-first search does precisely this. Doing so may lead to edge-case gains in efficiency, but do not alter the general characteristics of complexity and optimality for each method. For simplicity and grading purposes in this assignment, **do not make such modifications to algorithms learned in lecture**.

**III. What You Need To Submit**

Your job in this assignment is to write driver.py, which solves any 8-puzzle board when given an arbitrary starting configuration. The program will be executed as follows:

$ python3 driver.py <method> <board>

The method argument will be one of the following. You need to implement all three of them:

bfs (Breadth-First Search)

dfs (Depth-First Search)

ast (A-Star Search)

The board argument will be a comma-separated list of integers containing no spaces. For example, to use the bread-first search strategy to solve the input board given by the starting configuration {0,8,7,6,5,4,3,2,1}, the program will be executed like so (with no spaces between commas):

$ python3 driver.py bfs 0,8,7,6,5,4,3,2,1

**IMPORTANT**: The version of the python that we are using is **Python 3.6.4.**

**IV. What Your Program Outputs**

When executed, your program will create / write to a file called output.txt, containing the following statistics:

path\_to\_goal: the sequence of moves taken to reach the goal

cost\_of\_path: the number of moves taken to reach the goal

nodes\_expanded: the number of nodes that have been expanded

search\_depth: the depth within the search tree when the goal node is found

max\_search\_depth:  the maximum depth of the search tree in the lifetime of the algorithm

running\_time: the total running time of the search instance, reported in seconds

max\_ram\_usage: the maximum RAM usage in the lifetime of the process as measured by the **ru\_maxrss** attribute in the **resource** module, reported in megabytes

**Example #1: Breadth-First Search**

Suppose the program is executed for breadth-first search as follows:

$ python3 driver.py bfs 1,2,5,3,4,0,6,7,8

Which should lead to the following solution to the input board:

![input](https://user-images.githubusercontent.com/28363806/143877715-f5f8cb24-0be6-45a3-b5cd-285177892828.png)

The output file ([example](https://github.com/emotionalmonkey/AI/blob/master/AI/8-Puzzle/output.txt)) will contain **exactly** the following lines:

path\_to\_goal: ['Up', 'Left', 'Left']

cost\_of\_path: 3

nodes\_expanded: 10

search\_depth: 3

max\_search\_depth: 4

running\_time: 0.00188088

max\_ram\_usage: 0.07812500

.

**Example #2: Depth-First Search**

.

Suppose the program is executed for depth-first search as follows:

$ python3 driver.py dfs 1,2,5,3,4,0,6,7,8

Which should lead to the following solution to the input board:

![input](https://user-images.githubusercontent.com/28363806/143877715-f5f8cb24-0be6-45a3-b5cd-285177892828.png)

.

The output file ([example](https://github.com/emotionalmonkey/AI/blob/master/AI/8-Puzzle/output.txt)) will contain **exactly** the following lines:

path\_to\_goal: ['Up', 'Left', 'Left']

cost\_of\_path: 3

nodes\_expanded: 181437

search\_depth: 3

max\_search\_depth: 66125

running\_time: 5.01608433

max\_ram\_usage: 4.23940217

.

Other test cases are available on **Week 2 Project: Implementation FAQs** page.

**Note on Correctness**

.

Of course, the specific values for running\_time and max\_ram\_usage variables will vary greatly depending on the machine used and the specific implementation details; there is no "correct" value to look for. They are intended to enable you to check the time and space complexity characteristics of your code, and you should spend time to do so. All the other variables, however, will have **one and only one** correct answer for each algorithm and initial board specified in the sample test cases.**\*** A good way to check the correctness of your program is to walk through small examples by hand, like the ones above.

.

**\*** In general, **for any initial board whatsoever**, for BFS and DFS there is one and only one correct answer. For A\*, however, your output of nodes\_expanded may vary a little, depending on specific implementation details. You will be fine as long as your algorithm conforms to all **specifications** listed in these instructions. 

**V. Important Information**

Please read the following information carefully. Since this is the first programming project, we are providing many hints and explicit instructions. Before you post a clarifying question on the discussion board, make sure that your question is not already answered in the following sections.

**1. Implementation**

You will implement the following three algorithms as demonstrated in lecture. In particular:

- **Breadth-First Search**. Use an explicit queue, as shown in lecture.
- **Depth-First Search**. Use an explicit stack, as shown in lecture.
- **A-Star Search**. Use a priority queue, as shown in lecture. For the choice of heuristic, use the Manhattan priority function; that is, the sum of the distances of the tiles from their goal positions. Note that the blanks space is not considered an actual tile here.

**2. Order of Visits**

In this assignment, where an arbitrary choice must be made, we always **visit** child nodes in the "**UDLR**" order; that is, [‘Up’, ‘Down’, ‘Left’, ‘Right’] in that exact order. Specifically: 

- **Breadth-First Search**. Enqueue in UDLR order; dequeuing results in UDLR order.
- **Depth-First Search**. Push onto the stack in reverse-UDLR order; popping off results in UDLR order.
- **A-Star Search**. Since you are using a priority queue, what happens when there are duplicate keys? What do you need to do to ensure that nodes are retrieved from the priority queue in the desired order?

**3. Submission Test Cases**

You can **submit** your project any number of times before the deadline. Only the final submission will be graded. Following each submission, all three of your algorithms will be automatically run on two sample test cases each, for a total of **6** distinct tests:

**Test Case #1**
python3 driver.py bfs 3,1,2,0,4,5,6,7,8
python3 driver.py dfs 3,1,2,0,4,5,6,7,8
python3 driver.py ast 3,1,2,0,4,5,6,7,8

**Test Case #2**
python3 driver.py bfs 1,2,5,3,4,0,6,7,8
python3 driver.py dfs 1,2,5,3,4,0,6,7,8
python3 driver.py ast 1,2,5,3,4,0,6,7,8

This is provided as a sanity check for your code and the required output format. In particular, this is intended to ensure that you do not lose credit for incorrect output formatting. **Make sure your code passes at least these two test cases**. You will see that the results of each test are assessed by 8 items: 7 items are listed in **Section IV. What Your Program Outputs**. The last point is for code that executes and produces any output at all. Each item is worth 0.75 point.

**4. Grading and Stress Tests**

We will grade your project by running **additional test cases** on your code. In particular, there will be five test cases in total, each tested on all three of your algorithms, for a total of **15** distinct tests. Similar to the submission test cases, each test will be graded by 8 items, for a total of 90 points. **Plus, we give 10 points for code completing all 15 test cases within 10 minutes**. If you implement your code with reasonable designs of data structures, your code will solve all 15 test cases within a minute in total. We will be using a wide variety of inputs to stress-test your algorithms to check for correctness of implementation. So, we recommend that you test your own code extensively.

Do not worry about checking for **malformed input** boards, including boards of non-square dimensions, or unsolvable boards. 

**You will not be graded on the absolute values of your running-time or RAM usage statistics.** The values of these statistics can vary widely depending on the machine. **However, we recommend that you take advantage of them in testing your code.** Try batch-running your algorithms on various inputs, and plotting your results on a graph to learn more about the space and time complexity characteristics of your code. Just because an algorithm provides the correct path to goal does not mean it has been implemented correctly.

**5. Tips on Getting Started**

Begin by writing a class to represent the **state** of the game at a given turn, including parent and child nodes. We suggest writing a separate **solver** class to work with the state class. Feel free to experiment with your design, for example including a **board** class to represent the low-level physical configuration of the tiles, delegating the high-level functionality to the state class. When comparing your code with pseudocode, you might come up with another class for organising specific aspects of your search algorithm elegantly.

You will not be graded on your design, so you are at a liberty to choose among your favorite programming paradigms. Students have successfully completed this project using an entirely object-oriented approach, and others have done so with a purely functional approach. Your submission will receive full credit as long as your driver program outputs the correct information.

**VI. Before You Finish**

- **Make sure** your code passes at least the two submission test cases. 
- **Make sure** your algorithms generate the correct solution for an arbitrary solvable problem instance of 8-puzzle.
- **Make sure** your program always terminates without error, and in a reasonable amount of time. **You will receive zero points from the grader if your program fails to terminate. Running times of more than a minute or two may indicate a problem with your implementation.** If your implementation exceeds the time limit allocated (20 minutes for all test cases), your grade may be incomplete.
- **Make sure** your program output follows the specified format exactly. In particular, for the path to goal, use square brackets to surround the list of items, use single quotes around each item, and capitalize the first letter of each item. Round floating point numbers to 8 places after the decimal. You will not receive proper credit from the grader if your format differs from the provided examples above.

**USE OF VOCAREUM**

This assignment uses Vocareum for submission and grading. Vocareum comes equipped with an editing environment that you may use to do your development work. You are **NOT** required to use the editor. In particular, you are free to choose your favorite editor / IDE to do your development work on. When you are done with your work, you can simply upload your files onto Vocareum for submission and grading.

However, your assignments will be graded on the platform, so you **MUST** make sure that your code passes at least the submission test cases. In particular, do not use third-party libraries and packages. We do not guarantee that they will work on the platform, even if they work on your personal computer. For the purposes of this project, everything that comes with the standard Python library should be more than sufficient.

