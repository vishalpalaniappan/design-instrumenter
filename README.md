# design-instrumenter
A tool to instrument a python program using the mapping contained in the DAL engine as specific in the design workbench.

This tool performs two operations:
- It parses the AST of a python program and identifies sections that can be used to map the design onto the implementation. This will be running on the server and in mapping mode, it will generate the relevant metadata needed to do the mapping visually in the front end. This mapped information will be saved in the engine.
- It accepts the mapping contained in the engine and instruments the program, producing an execution that can be transformed into the behavior of the design.

In my previous version of instrumenting programs, I built tools that can automatically instrument the dynamic trace. However, all data collection in this framework is motivated by semantic necessity. So there is no need fancy instrumentation, instead, it will work with the design workbench to identify the semantically relevant information that must be instrumented. Eventually, this will be extended to include the domain specific data specification so that CLP can apply domain specific compression to the data.

So my plan is to first implement the necessary code to enable the visual tool to do the mapping in the design workbench, then I will use the result of the mapping to instrument and execute. Then I will take the result and bring it back into design workbench where the execution will be transformed in the behavior of the design and then rest of the design feedback loop will take over.

This will be written in python and the server will invoke this program as needed. Eventually this will be extended for other languages and the same process will repeat.
