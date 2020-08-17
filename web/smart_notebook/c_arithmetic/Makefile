# Makefile for C++ shared library

CC = g++
CFLAGS = -c -fPIC
LDFLAGS = -shared
RM = rm -f
TARGET_LIB = arithmetic.so


SRCS = arithmetic.cpp  # source files
OBJS = $(SRCS:.cpp=.o)

.PHONY: all
all: ${TARGET_LIB}

$(TARGET_LIB): $(OBJS)
	$(CC) ${LDFLAGS} -Wl,-soname,${TARGET_LIB} -o $@ $^

$(OBJS): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) -o $(OBJS)

.PHONY: clean
clean:
	-${RM} ${TARGET_LIB} ${OBJS}