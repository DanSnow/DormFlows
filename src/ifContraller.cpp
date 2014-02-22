#include <iostream>
#include <string>
#include <cstdlib>

#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/range/algorithm.hpp>

using namespace std;

int main(int argc, char *argv[]) {
  if(argc != 3) {
    cerr << "Usage: " << argv[0] << " <interface> up|down" << endl;
    return 2;
  }
  if(geteuid() != 0) {
    cerr << "This program must need root privilege" << endl;
    return 1;
  }
  string interface(argv[1]);
  typedef const boost::iterator_range<std::string::const_iterator> StringRange;
  if(boost::find_if(StringRange(interface.begin(), interface.end()), boost::is_any_of(" |&;")) != interface.end()) {
    cerr << "Interface has illegal char" << endl;
    return 1;
  }
  string action(argv[2]);
  if(action != "up" && action != "down") {
    cerr << "Action must be up or down" << endl;
    return 2;
  }
  execlp("ifconfig", "ifconfig", interface.c_str(), action.c_str(), NULL);
  return 0;
}
