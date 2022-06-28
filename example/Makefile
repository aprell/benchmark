CFLAGS = -Wall -Wextra -fopenmp

all: O0/matmul O1/matmul O2/matmul

O0/matmul O1/matmul O2/matmul: CFLAGS += -$(@D)

O0/matmul O1/matmul O2/matmul: matmul.c
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $< $(LDLIBS) -o $@

clean:
	$(RM) -r O0 O1 O2

.PHONY: all clean
