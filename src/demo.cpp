#include "cpp_python_wrapper.hpp"
#include <string>
#include <vector>

using namespace std;
int main()
{
    call_python_function("emotion_api", {"test", "7", "1"});

}
