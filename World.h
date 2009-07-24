#ifndef WORLD_H
#define WORLD_H

#include <vector>
#include "State.h"

template <class S>
class World
{
public:
  virtual std::vector<StateCostPair<S> > succ(S) = 0;
  virtual std::vector<StateCostPair<S> > pred(S) = 0;
  virtual double c(S, S) = 0;
  virtual double h(S, S) = 0;
  virtual ~World() { }
};

#endif
