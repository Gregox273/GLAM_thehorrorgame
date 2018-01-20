#include "cpp_python_wrapper.hpp"
#include <string>
#include <vector>

using namespace std;
int main()
{
    call_python_function("temp/other", {"a", "b"});

    vector<string> params({"c", "d"});
    call_python_function("temp/other2", params, "python2.7");
}
