# Course Scheduling Problem

## Introduction

Scheduling problems appear in many real-world situations, such as school timetables, employee shifts, and resource planning. In these problems, tasks must be assigned to limited time slots while satisfying different constraints. Finding a good schedule can be difficult because many possible combinations exist.

In this project, we study a simplified course scheduling problem. The goal is to assign courses to available time slots while avoiding scheduling conflicts. For example, two courses that share the same instructor or classroom should not be scheduled at the same time. As the number of courses and constraints increases, the search space grows quickly, making it hard to find a good solution using simple methods.

Evolutionary Algorithms (EA) provide a useful approach for solving such optimization problems. Instead of searching the entire solution space directly, an EA works by generating a population of candidate schedules and gradually improving them through selection, mutation, and recombination. By iteratively evolving better solutions, the algorithm can often find high-quality schedules even in complex search spaces.

---

## Problem Formulation

A set of courses must be assigned to available time slots. The goal is to generate a schedule that satisfies the constraints while minimizing scheduling conflicts.

### Inputs

| Input | Description |
|-------|-------------|
| Courses | A set of courses that need to be scheduled |
| Time Slots | A set of time slots available during the week |
| Classrooms | A limited number of classrooms |
| Instructors | Information about instructors assigned to each course |

### Constraints

1. A classroom can only host one course at the same time.
2. An instructor cannot teach two courses at the same time.
3. Each course must be assigned to exactly one time slot.

> If any of these constraints are violated, the schedule contains conflicts.

### Objective

Minimize the total number of conflicts in the schedule. A schedule with fewer conflicts is considered a better solution. Ideally, the algorithm should find a schedule with **zero conflicts**.

---

## Why Evolutionary Algorithms?

The course scheduling problem has a large search space because many possible combinations of course assignments exist. As the number of courses and time slots increases, the number of possible schedules grows very quickly. Traditional exhaustive search methods would be computationally expensive.

Evolutionary Algorithms are well suited for this type of combinatorial optimization problem. By representing schedules as individuals in a population and applying evolutionary operators such as mutation and recombination, the algorithm can explore many possible solutions and gradually improve the schedule over generations.
