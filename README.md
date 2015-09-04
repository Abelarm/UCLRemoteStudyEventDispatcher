# UCL Remote Study Event Dispatcher

The UCL Remote Study Event Dispatcher is a framework for handling events produced by data collection clients and
dispatching them to various computational algorithms on a server or HPC node. The dispatcher works in conjunction
with the [UCL Study Websites](https://launchpad.net/study.cs.ucl-websites/). It receives events from study websites
via a message broker (RabbitMQ), and then dispatches them to relevant algorithms. The dispatcher also has a logic
for storing and indexing computational results so they can be cached and deleted by clients in the future.

The dispatcher is currently being developed by Luigi Giugliano. The overall UCL Remote Study infrastructure is
designed and maintained by Steve Dodier-Lazaro. For any questions, please contact s.dodier-lazaro@cs.ucl.ac.uk.

