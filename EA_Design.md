# Evolutionary Algorithm Design

## Representation (Genotype and Phenotype)

The genotype is encoded as a fixed-length integer array of size N, where N is the total number of courses. Each gene i stores the index of the time slot assigned to course i:

```
chromosome = [slot₀, slot₁, slot₂, ..., slot_{N-1}]
```

For example, with 6 courses and 5 available time slots, a chromosome might look like `[0, 2, 1, 3, 0, 4]`, meaning Course 1 is assigned to slot 0, Course 2 to slot 2, and so on.

The **phenotype** (the actual schedule) is obtained by decoding this chromosome. For each time slot, the set of courses assigned to that slot is collected, and classrooms are allocated greedily in order. This design choice deliberately separates time slot assignment (handled by the EA) from classroom assignment (handled deterministically at decode time), which reduces the search space significantly without sacrificing solution quality.

---

## Fitness Evaluation

The fitness function directly encodes the optimization objective: minimizing the total number of scheduling conflicts. Two types of conflict are counted:

- **Room conflict**: within a given time slot, the number of courses exceeds the number of available classrooms. Each excess course counts as one conflict.
- **Instructor conflict**: within a given time slot, the same instructor is assigned to more than one course. Each excess assignment counts as one conflict.

The fitness of a chromosome is defined as:

```
fitness(c) = −(room_conflicts + instructor_conflicts)
```

The negative sign transforms the minimization problem into a maximization problem, consistent with standard EA convention. A fitness of 0 corresponds to a conflict-free, optimal schedule.

---

## Variation Operators

### Recombination — Single-point Crossover

Given two parent chromosomes, a crossover point is chosen uniformly at random from positions 1 to N−1. The offspring inherit the first segment from one parent and the second segment from the other:

```
Parent A: [0, 2, 1, | 3, 0, 2]
Parent B: [1, 0, 3, | 1, 2, 0]
Child 1:  [0, 2, 1, | 1, 2, 0]
Child 2:  [1, 0, 3, | 3, 0, 2]
```

Crossover is applied with probability `p_c = 0.8`. This operator recombines partial schedules from two parents, allowing the offspring to inherit time slot patterns that worked well in different regions of the chromosome.

### Mutation — Two Strategies Applied Jointly

**Random Mutation**: each gene is independently reassigned to a uniformly random time slot with probability `p_m = 0.12`. This provides broad exploration and prevents premature convergence.

**Conflict-Guided Mutation (CGM)**: the decoder first identifies all courses currently involved in a conflict (room or instructor). Only those courses have their time slot randomly reassigned. This is a heuristic operator that focuses variation on the problematic parts of the schedule, accelerating convergence compared to purely random mutation.

In each generation, CGM is applied with probability 0.6; otherwise random mutation is applied. Using both strategies prevents over-reliance on the greedy heuristic, which could reduce diversity and cause stagnation.

---

## Selection and Population Management

### Selection — Tournament Selection (k = 3)

At each step, three individuals are drawn uniformly at random from the current population, and the one with the highest fitness is selected as a parent. This process is repeated independently to produce the second parent. Tournament selection provides controllable selection pressure (adjustable via k) and is robust to scaling issues in the fitness landscape, unlike fitness-proportional (roulette wheel) selection.

### Population Management — Generational with Elitism

The algorithm uses a generational replacement strategy: each generation, a full set of N offspring is produced from the selected parents, and the offspring replace the current population entirely. To prevent the loss of the best solution found so far, **elitism** is applied: the top 2 individuals from the current generation are copied directly into the next generation before offspring fill the remaining slots.

This ensures monotonic improvement in the best fitness over generations, while still allowing substantial turnover in the rest of the population to maintain diversity.

---

## Parameter Choices

| Parameter | Value | Rationale |
|---|---|---|
| Population size | 60 | Large enough for diversity; small enough for fast evaluation |
| Max generations | 500 | Sufficient for the problem scale; early termination if conflicts = 0 |
| Crossover rate (p_c) | 0.80 | Standard value; high enough to drive recombination |
| Mutation rate (p_m) | 0.12 | Slightly above typical 0.1 to compensate for discrete space |
| Tournament size (k) | 3 | Moderate selection pressure; avoids too-greedy selection |
| Elitism count | 2 | Preserves best solutions without dominating the population |
| CGM probability | 0.60 | Dominant strategy, mixed with random mutation for diversity |

Parameter values were chosen based on standard EA practice for combinatorial optimization problems of this scale. The mutation rate is intentionally slightly higher than the canonical `1/N` rule because the integer encoding benefits from more frequent perturbation in a discrete search space.
