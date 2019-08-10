all: functions

SRCS := $(wildcard deploy/*.sh)
FUNCS := $(SRCS:deploy/%.sh=%)

functions:
	for x in $(SRCS); do ./$$x; done