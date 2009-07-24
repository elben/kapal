#include "StateAStar.h"

StateAStar::StateAStar(const double _g = 0.0,
    const int _prev_x = 0, const int _prev_y = 0) :
  g(_g), prev_x(_prev_x), prev_y(_prev_y)
{
}
