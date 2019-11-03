CC=gcc
CFLAGS=-Wall

SOURCES=common.c random.c matrix.c

TASK_SOURCES=task.c
TASK_OUTPUT=task

SOLVER_SOURCES=solver.c matrixio.c chain.c
SOLVER_OUTPUT=solver


.PHONY: task solver


task:
	$(CC) $(CFLAGS) $(SOURCES) $(TASK_SOURCES) -o $(TASK_OUTPUT)

solver:
	$(CC) $(CFLAGS) $(SOURCES) $(SOLVER_SOURCES) -o $(SOLVER_OUTPUT)
