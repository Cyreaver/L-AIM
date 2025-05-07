from ghidra.app.decompiler import DecompInterface
from java.io import File, FileWriter

def decompile_all(program, monitor):
    listing = program.getListing()
    functions = listing.getFunctions(True)
    decompiler = DecompInterface()
    decompiler.openProgram(program)

    executable_path = program.getExecutablePath()
    if executable_path is None:
        print("Error: Cannot determine executable path.")
        return

    binary_file = File(executable_path)
    binary_name = binary_file.getName()

    output_file_path = binary_file.getParent() + File.separator + binary_name + "_decom.txt"
    print("Output will be saved to: " + output_file_path)

    with FileWriter(output_file_path) as writer:
        for func in functions:
            if monitor.isCancelled():
                print("Decompilation canceled.")
                break
            res = decompiler.decompileFunction(func, 30, monitor)
            if res and res.getDecompiledFunction():
                writer.write("///////////// Function: {}\n\n".format(func.getName()))
                writer.write(res.getDecompiledFunction().getC())
                writer.write("\n\n\n")

    print("Decompilation complete. Output written to " + output_file_path)

# This part runs when the script is executed by Ghidra (GUI or headless)
decompile_all(currentProgram, monitor) 