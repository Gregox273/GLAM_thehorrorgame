#ifndef CPP_PYTHON_WRAPPER_HPP
#define CPP_PYTHON_WRAPPER_HPP

#include <cstdlib>
#include <string>
#include <vector>

/* Calls a python program and runs it
 *
 * If you want to run 'python3 foo.py bar1 bar2'
 * run call_python_function("foo", {"bar1", "bar2"})
 * (that is, python3 is the default)
 *
 * If you want to run 'python2.7 foo.py bar1 bar2'
 * run call_python_function("foo", {"bar1", "bar2"}, "python2.7")
 *
 * Alternatively, create a vector of strings for arguments like:
 * std::vector<std::string> params;
 * params.push_back("arg1");
 * params.push_back("arg2");
 * call_python_function("foo", params);
 */
int call_python_function(std::string program,
                         std::vector<std::string> args,
                         std:: string python_version = "python")
{
    std::string cmd = python_version + " " + program + ".py";

    for (auto arg : args)
    {
        cmd += " " + arg;
    }
    system(cmd.c_str());
}

#endif //CPP_PYTHON_WRAPPER_HPP
