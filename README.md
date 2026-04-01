# design-instrumenter
This tool instruments Python programs using the implementation mapping stored in the DAL engine, as defined by the Design Workbench.

This tool performs two primary operations:
- The tool parses the AST of a Python program and identifies implementation sections that can be mapped onto the design. This operation runs on the server and supports the visual mapping workflow in the front end.
- The tool also accepts the implementation mapping stored in the engine and uses it to instrument the Python program.

In my previous instrumentation programs (see [adli][adli]), I built tools that can automatically instrument the complete dynamic trace. However, all data collection in the design feedback loop is motivated by semantic necessity. So it is a much simpler process, it will work with the design workbench to identify the semantically relevant information that must be instrumented. Eventually, this will be extended to include the domain specification of the data so that CLP can apply domain specific compression and fully optimize the platform.

My plan is to first implement a solution that will enable the visual tool to do the mapping in the design workbench and save that in the engine. Then I will bring the engine into the instrumenter and use the mapping to instrument the program so it produces a trace that can be transforme into the behavior of the design. Then the rest of the design feedback loop will take over.

This will be written in python so that I can leverage its AST library and the server will invoke this program as needed. Eventually this will be extended for other languages and the same process will repeat.

[adli]: https://github.com/vishalpalaniappan/asp-adli-python
