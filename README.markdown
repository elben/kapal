# Kapal #

Kapal is an path-planning learning tool and library written in Python. Its intended use is algorithms research and navigation tasks in games and robotics. Kapal aims to be:

* easy to use - Kapal helps you understand and use planning algorithms better.
* loaded - Kapal comes with many different world representations and algorithms.
* expendable - implement new world representation and algorithms with ease.

Kapal started as a summer project for comparing the performance of different planning algorithms. I decided to generalize it a bit and release it for public consumption. I then wrote Seaship to learn about GUI development. In other words, Kapal is a personal project.

But with that being said, Kapal is a great learning tool. If you wanted to use Kapal to learn about Dijkstra or A*, I encourage you to play around with Seaship to get a feel for the algorithm. Then, read through the algorithm code in Kapal to figure out what's going on under the hood. Enjoy yourself!

## Downloading

You can download kapal
[here](http://github.com/eshira/kapal/archives/master).

Or you can use git:

    $ git clone http://github.com/eshira/kapal.git

## Installing

Installing is easy:

    $ python setup.py

## Seaship

Seaship is a GUI-based tool to help you play around with Kapal. Seaship comes with Kapal (they're in the same git repository). It's still under development, but here's a screenshot:

![Screenshot of Seaship](http://elbenshira.com/images/kapal/seaship-screenshot.png)

## Getting Started

The best way to get started with Kapal is to start playing with Seaship. Also, check out the examples directory. Then, head over to the [API Overview](http://wiki.github.com/eshira/kapal/api-overview).

### Q: Why Python? Isn't Python too slow for path-planning?

I couldn't find a full-featured path-planning library for Python, so I decided to write my own. And yes, Python isn't as fast as compiled languages, but if you are already using Python for your game or robot, then you probably don't need the fastest path-planner. If you need a faster (and more complicated) path-planner, check out "OOPSMP":http://www.kavrakilab.org/software.

### Q: How do you pronounce "kapal"?

kah - pahl.

### Q: Where did  the word "kapal" come from?

Kapal is Indonesian for boat or ship. I chose this name because sea vessels require path-planning, especially away from pirates, maelstroms, and sea monsters.

