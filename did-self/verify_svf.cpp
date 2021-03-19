/* g++ verify_svf.cpp -o ./verify.svf */
#include <iostream>
#include <string>

int main ()
{
  std::string path_to_verifier = " /home/mmlab/scn4ndn/did-self/verify_svf.py"; //!!!BE CAREFUL ADD SPACE AT THE BEGINING
  std::string path_to_file = " /home/mmlab/scn4ndn/did-self/GExt6UZsqMtIwYHaA2SCx7r5oSP0QSjIp2rTRUxuqYo.svf";//!!!BE CAREFUL ADD SPACE AT THE BEGINING
  std::string content_id   = " GExt6UZsqMtIwYHaA2SCx7r5oSP0QSjIp2rTRUxuqYo";//!!!BE CAREFUL ADD SPACE AT THE BEGINING
  std::string command = "python3 ";
  command+= path_to_verifier;
  command+= path_to_file;
  command+= content_id;
  int i = system (command.c_str());
  if (i == 0)
  {
     std::cout << "Success";
  }else
  {
     std::cout << "Failure " << i;
  }
  return 0;
}