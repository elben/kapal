#ifndef STATEASTAR_H
#define STATEASTAR_H

#include "types.h"
#include "State.h"

class StateAStar : public State
{
private:
  double g;
  int prev_x;
  int prev_y;
public:
  StateAStar(const double, const int, const int);
  double get_h();
  double get_g();
  void set_g(double);
};

#endif
