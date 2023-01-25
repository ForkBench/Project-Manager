CC=gcc
CFLAGS=-c -Wall -Wextra
LDFLAGS=

CORE_PATH=./src
SOURCES=$(CORE_PATH)/main.c #$(CORE_PATH)/other_files.c

OBJECTS=$(SOURCES:.c=.o)

EXECUTABLE=main

.PHONY : clean
MAIN: $(SOURCES)  $(EXECUTABLE)
$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -o $@
clean :
	rm -rf $(OBJECTS) $(EXECUTABLE)
