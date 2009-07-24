#ifndef WORLD2D_H
#define WORLD2D_H

#include "World.h"
#include "State.h"
#include "types.h"

template <class S>
class World2d : public World<S>
{
private:
  std::vector< std::vector<S> > world;
  S start;
  S goal;
  int run_num;
public:
  World2d();
  ~World2d();
  std::vector<StateCostPair<S> > succ();
  std::vector<StateCostPair<S> > pred();
  double c(S, S);
  double h(S, S);
};

#endif
