include buildconfig

.SUFFIXES: .cpp .cc .o .so .c .bundle 

.c.o:
	$(CC) -c $(INCLUDES) $(CFLAGS) $<
	
.cc.o:
	$(C++) -c $(INCLUDES) $(C++FLAGS) $<

.cpp.o:
	$(C++) -c $(INCLUDES) $(C++FLAGS) $<

.cc.i:
	$(C++) -E $(INCLUDES) $(C++FLAGS) $*.cc > $*.i

.cc.so:
	-rm -f $@
	$(LD) -o $@ $(INCLUDES) $< $(LIBS)

.cpp.so:
	-rm -f $@
	$(LD) -o $@ $(INCLUDES) $< $(LIBS)

.o.so:
	-rm -f $@
	$(LD) -o $@ $< $(LIBS)

.o.bundle:
	-rm -f $@
	$(LD) -o $@ $< $(LIBS)



plugins: \
		nurbsRivetNode.$(EXT)


depend:
	makedepend $(INCLUDES) -I/usr/include/CC *.cc

clean:
	-rm -f *.o

Clean:
	-rm -f *.o *.so *.lib *.bak *.bundle

##################
# Specific Rules #
##################





nurbsRivetNode.$(EXT): nurbsRivetNode.o pluginMain.o
	-rm -f $@
	$(LD) -o $@ $? $(LIBS) -lOpenMayaAnim -lOpenMayaUI 




