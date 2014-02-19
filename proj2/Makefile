# Makefile for socket examples

CXX=			g++ $(CCFLAGS)
MSGD=			msgd.o server.o storage.o
OBJS =			$(MSGD)

LIBS=			-pthread

CCFLAGS= -g

all:	msgd

msgd:$(MSGD)
	$(CXX) -o msgd $(MSGD) $(LIBS)

clean:
	rm -f $(OBJS) $(OBJS:.o=.d)

realclean:
	rm -f $(OBJS) $(OBJS:.o=.d) msgd


# These lines ensure that dependencies are handled automatically.
%.d:	%.cc
	$(SHELL) -ec '$(CC) -M $(CPPFLAGS) $< \
		| sed '\''s/\($*\)\.o[ :]*/\1.o $@ : /g'\'' > $@; \
		[ -s $@ ] || rm -f $@'

include	$(OBJS:.o=.d)
