# pyRunBook

A simple tool to work with automatic or manual run-books from a Unix terminal.

## Description

pyRunBook allows DevOps / SRE engineers to create run-books as a code. Each run-book
is a list of steps. Steps can be manual or automatic - running shell command or Python
function. It's intended to support workflows when full automation is not possible or
requires a mixture of different tools.

pyRunBook is an interactive terminal application that you can use to:
- list run-book steps, see their detailed description
- run automatic steps
- set status of automatic or manual steps
- put comment on steps.

It will keep track of your runbook state, saving every change to JSON file. You can stop
the tool at any time and pickup later from the same state.

## Running

A standalone pyrunbook script can load run-book definition from a JSON file. This may be used
to create run-books with manual steps or steps that contain static scripts.

You can also import pyrunbook module into your Python script to run steps containing custom Python code.
